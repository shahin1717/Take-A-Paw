# app/routes/pets.py
from flask import Blueprint, flash, jsonify, redirect, request, session, render_template, url_for, abort
from sqlalchemy.sql import func

from app.routes.auth_utils import login_required
from ..db import db
from ..models import Favorite, Pet, User

bp = Blueprint("pets", __name__)


def _resolve_contact(p: Pet):
    """
    Decide which contact details to show for a given pet.

    Rules:
    - Prefer per-listing overrides (contact_email_override / contact_phone_override).
    - Otherwise, use the owner's email/phone.
    - Only show contact info if the owner allowed public_contact AND at least one
      of email/phone exists.
    - If not visible, return (None, None, False).
    """
    owner = p.owner
    owner_public = owner.public_contact if owner else False

    email = p.contact_email_override or (owner.email if owner else None)
    phone = p.contact_phone_override or (owner.phone if owner else None)

    visible = bool(owner_public and (email or phone))

    if not visible:
        email = None
        phone = None

    return email, phone, visible


def serialize_pet(p: Pet):
    """
    Convert a Pet ORM object into a dict suitable for JSON/API responses.

    Includes:
    - Basic pet info (name, species, age, etc.)
    - Contact info (resolved via _resolve_contact)
    - Flags like adopted, public_contact, and contact_visible.
    """
    email, phone, contact_visible = _resolve_contact(p)
    return {
        "id": p.id,
        "name": p.name,
        "species": p.species,
        "breed": p.breed,
        "age": p.age,
        "gender": p.gender,
        "location": p.location,
        "description": p.description,
        "image": p.image,
        "adopted": p.adopted,
        "source": p.source,
        "owner_id": p.owner_id,
        "public_contact": p.public_contact,
        "contact_email": email,
        "contact_phone": phone,
        "contact_visible": contact_visible,
        "created_at": p.created_at.isoformat() if p.created_at else None,
    }

@bp.get("/pets")
def list_pets():
    """
    Return a JSON list of all non-adopted pets in random order.
    """
    pets = Pet.query.filter_by(adopted=False).order_by(Pet.created_at.desc()).all()
    return jsonify([serialize_pet(p) for p in pets])

@bp.get("/pets/<int:pet_id>")
def pet_detail(pet_id: int):
    """
    Return JSON details for a single pet by id.

    - If the pet does not exist or is adopted, return 404 JSON.
    """
    p = Pet.query.get(pet_id)
    if not p or p.adopted:
        return jsonify({"error": "not found"}), 404
    return jsonify(serialize_pet(p))


@bp.get("/pets/search")
def search():
    """
    JSON API search for pets.

    Filters:
    - species: exact match (case-insensitive).
    - breed: contains substring (case-insensitive).
    - location: contains substring (case-insensitive).

    Only returns non-adopted pets.
    """
    species = (request.args.get("species") or "").strip().lower()
    breed = (request.args.get("breed") or "").strip().lower()
    location = (request.args.get("location") or "").strip().lower()

    q = Pet.query.filter_by(adopted=False)

    if species:
        q = q.filter(Pet.species.ilike(species))
    if breed:
        q = q.filter(Pet.breed.ilike(f"%{breed}%"))
    if location:
        q = q.filter(Pet.location.ilike(f"%{location}%"))

    pets = q.order_by(Pet.created_at.desc()).all()
    return jsonify([serialize_pet(p) for p in pets])


@bp.post("/pets")
def create_listing():
    """
    Create a new pet listing (HTML form POST).

    Flow:
    - Require logged-in user; otherwise redirect to login.
    - Validate required fields + image.
    - Upload image to Cloudinary.
    - Create Pet row with extra adoption fields (home_type, activity_level, etc.).
    - Redirect to the newly created pet detail page (or provided 'next' URL).
    """
    import cloudinary.uploader

    user_id = session.get("user_id")
    if not user_id:
        flash("Please log in to add a pet.", "error")
        return redirect(url_for("auth.login_form", next=url_for("pets.add_pet_form")))

    data = request.form
    image_file = request.files.get("image")

    required = ["name", "species", "breed", "age", "gender", "location", "description"]
    missing = [k for k in required if not (data.get(k) or "").strip()]

    if not image_file or image_file.filename == "":
        missing.append("image")

    if missing:
        flash(f"Missing fields: {', '.join(missing)}", "error")
        return redirect(url_for("pets.add_pet_form"))

    def clean(key):
        """
        Helper for optional text fields:
        - Strip whitespace and convert empty string to None.
        """
        value = (data.get(key) or "").strip()
        return value or None

    try:
        uploaded = cloudinary.uploader.upload(
            image_file,
            folder="take-a-paw/pets",
        )
        image_url = uploaded["secure_url"]
    except Exception as e:
        print("Cloudinary upload error:", e)
        flash("Image upload failed. Please try again.", "error")
        return redirect(url_for("pets.add_pet_form"))

    pet = Pet(
        name=data["name"].strip(),
        species=data["species"].strip().capitalize(),
        breed=data["breed"].strip(),
        age=data["age"].strip(),
        gender=data["gender"].strip(),
        location=data["location"].strip(),
        description=data["description"].strip(),
        image=image_url,
        adopted=False,
        source="user",
        owner_id=user_id,
        contact_email_override=clean("contact_email"),
        contact_phone_override=clean("contact_phone"),
        public_contact=bool(data.get("public_contact", True)),
        home_type=clean("home_type"),
        activity_level=clean("activity_level"),
        experience=clean("experience"),
        time_commitment=clean("time_commitment"),
        family_situation=clean("family_situation"),
    )

    db.session.add(pet)
    db.session.commit()

    flash(f"Your listing “{pet.name}” is live!", "success")
    next_url = request.form.get("next")
    return redirect(next_url or url_for("pets.home_pet_detail", pet_id=pet.id))


@bp.get("/me/listings")
@login_required
def my_listings_page():
    """
    Show the HTML page with all pets listed by the current user.

    - Requires login.
    - Uses serialize_pet so that templates can rely on a consistent structure.
    """
    user_id = session.get("user_id")
    if not user_id:
        flash("Please log in to view your listings.")
        return redirect(url_for("pets.home_index"))

    pets = Pet.query.filter_by(owner_id=user_id).order_by(Pet.created_at.desc()).all()
    return render_template("my_listings.html", pets=[serialize_pet(p) for p in pets])


@bp.post("/pets/<int:pet_id>/favorite")
def toggle_favorite(pet_id: int):
    """
    Add or remove a pet from the current user's favorites.

    Behavior:
    - Require login; otherwise redirect to login.
    - If user record is missing for some reason, create a basic one (fallback).
    - If pet is invalid or adopted, show error and redirect.
    - If a Favorite exists, delete it; otherwise create one.
    - Flash success or error and redirect back to 'next' or Referer or home.
    """
    user_id = session.get("user_id")
    if not user_id:
        flash("Please log in to use favorites.", "error")
        return redirect(url_for("auth.login_form", next=request.path))

    user = User.query.get(user_id)
    if not user:
        user = User(id=user_id, display_name=user_id)
        db.session.add(user)
        db.session.commit()
        flash(f"Welcome, {user_id}! Your profile has been created.", "success")

    pet = Pet.query.get(pet_id)
    if not pet or pet.adopted:
        flash("Pet not found or already adopted.", "error")
        next_url = request.form.get("next") or url_for("pets.home_index")
        return redirect(next_url)

    fav = Favorite.query.filter_by(user_id=user_id, pet_id=pet_id).first()

    if fav:
        db.session.delete(fav)
        action = "removed from"
    else:
        db.session.add(Favorite(user_id=user_id, pet_id=pet_id))
        action = "added to"

    try:
        db.session.commit()
        flash(f"Pet {action} favorites.", "success")
    except Exception as e:
        db.session.rollback()
        flash("Error updating favorites. Please try again.", "error")
        print(f"Favorite error: {e}")

    next_url = (
        request.form.get("next")
        or request.headers.get("Referer")
        or url_for("pets.home_index")
    )
    return redirect(next_url)


@bp.post("/pets/<int:pet_id>/delete")
def delete_pet(pet_id: int):
    """
    Allow the owner of a pet to delete their listing.

    Steps:
    - Require login; otherwise redirect to login.
    - Check that the pet exists.
    - Check that the current user is the owner (403 if not).
    - Delete the pet and redirect to the "my listings" page.
    """
    user_id = session.get("user_id")
    if not user_id:
        flash("Please log in to delete a pet.", "error")
        return redirect(url_for("auth.login_form", next=request.path))

    pet = Pet.query.get(pet_id)
    if not pet:
        flash("Pet not found.", "error")
        return redirect(url_for("pets.home_index"))

    if pet.owner_id != user_id:
        abort(403)

    try:
        db.session.delete(pet)
        db.session.commit()
        flash(f"Pet '{pet.name}' has been deleted.", "success")
    except Exception as e:
        db.session.rollback()
        flash("Error deleting pet. Please try again.", "error")
        print(f"Delete error: {e}")

    return redirect(url_for("pets.my_listings_page"))


@bp.get("/me/favorites")
def my_favorites_json():
    """
    Return a JSON list of the current user's favorite pets (non-adopted only).

    - If the user is not logged in or has no favorites, returns an empty list.
    """
    user_id = session.get("user_id")
    if not user_id:
        return jsonify([])

    favs = Favorite.query.filter_by(user_id=user_id).all()
    pet_ids = [f.pet_id for f in favs]
    if not pet_ids:
        return jsonify([])

    pets = Pet.query.filter(Pet.id.in_(pet_ids), Pet.adopted == False).all()
    return jsonify([serialize_pet(p) for p in pets])


@bp.get("/favorites")
def favorites_page():
    """
    Render an HTML page with the current user's favorite pets.

    - Requires login; otherwise redirect to home with a flash message.
    """
    user_id = session.get("user_id")
    if not user_id:
        flash("Please log in to see favorites.")
        return redirect(url_for("pets.home_index"))

    favs = Favorite.query.filter_by(user_id=user_id).all()
    ids = [f.pet_id for f in favs]
    pets = Pet.query.filter(Pet.id.in_(ids), Pet.adopted == False).all() if ids else []
    return render_template("favorites.html", pets=[serialize_pet(p) for p in pets])


@bp.get("/")
def home_index():
    pets = Pet.query.filter_by(adopted=False).order_by(func.random()).all()

    return render_template("index.html", pets=pets)


@bp.get("/search")
def home_search():
    """
    HTML search version for the homepage.

    - Same filters as /pets/search but renders index.html instead of JSON.
    """
    species = (request.args.get("species") or "").strip()
    breed = (request.args.get("breed") or "").strip()
    location = (request.args.get("location") or "").strip()

    q = Pet.query.filter_by(adopted=False)

    if species:
        q = q.filter(Pet.species.ilike(f"%{species}%"))
    if breed:
        q = q.filter(Pet.breed.ilike(f"%{breed}%"))
    if location:
        q = q.filter(Pet.location.ilike(f"%{location}%"))

    pets = q.order_by(Pet.created_at.desc()).all()
    return render_template("index.html", pets=[serialize_pet(p) for p in pets])


@bp.get("/pet/<int:pet_id>")
def home_pet_detail(pet_id: int):
    p = Pet.query.get(pet_id)
    if not p or p.adopted:
        return render_template("404.html"), 404

    user_id = session.get("user_id")
    is_favorited = False
    if user_id:
        is_favorited = Favorite.query.filter_by(
            user_id=user_id, pet_id=pet_id
        ).first() is not None

    email, phone, contact_visible = _resolve_contact(p)

    return render_template(
        "pet_detail.html",
        pet=p,
        contact_email=email,
        contact_phone=phone,
        contact_visible=contact_visible,
        is_favorited=is_favorited,
    )

@bp.get("/add-pet")
@login_required
def add_pet_form():
    """
    Show the form for creating a new pet listing.

    - Requires login; otherwise redirects to home.
    """
    if not session.get("user_id"):
        flash("Please log in to add a pet.")
        return redirect(url_for("pets.home_index"))
    return render_template("add_pet.html")
