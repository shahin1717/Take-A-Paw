# app/routes/auth.py
from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template, flash
from ..db import db
from ..models import User
from app.routes.auth_utils import login_required

bp = Blueprint("auth", __name__)


def _normalize_username(u: str) -> str:
    """
    Take any username-like input and normalize it.

    - Handles None safely.
    - Strips leading/trailing spaces.
    - Converts to lowercase.
    """
    return (u or "").strip().lower()


@bp.get("/register")
def register_form():
    """
    Show the registration form (HTML view).
    """
    return render_template("register.html")


@bp.post("/register")
def register_submit():
    """
    Handle user registration from both JSON and regular form POST.

    Steps:
    - Read data from JSON body or form fields.
    - Normalize username and basic contact fields.
    - Validate required fields (username, password).
    - Check for duplicate username.
    - Create the user, hash the password, commit to DB.
    - Log the user in by setting session["user_id"].
    - Return JSON or redirect depending on the request type.
    """
    # support both API-style JSON and classic HTML form
    data = request.get_json(silent=True) or request.form

    username = _normalize_username(data.get("username"))
    password = data.get("password")
    display_name = data.get("display_name") or username
    email = (data.get("email") or "").strip() or None
    phone = (data.get("phone") or "").strip() or None
    public_contact = str(data.get("public_contact", "true")).lower() in ("1", "true", "yes", "on")

    if not username or not password:
        msg = "Username and password are required."
        if request.is_json:
            return jsonify({"ok": False, "error": msg}), 400
        flash(msg, "error")
        return redirect(url_for("auth.register_form"))

    # check if username is already taken
    if User.query.filter_by(username=username).first():
        msg = "Username already taken."
        if request.is_json:
            return jsonify({"ok": False, "error": msg}), 400
        flash(msg, "error")
        return redirect(url_for("auth.register_form"))

    # create and store the new user
    user = User(
        username=username,
        display_name=display_name,
        email=email,
        phone=phone,
        public_contact=public_contact,
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    # log them in after registration
    session["user_id"] = user.id

    next_url = url_for("pets.home_index")

    if request.is_json:
        return jsonify(
            {
                "ok": True,
                "user": {"id": user.id, "display_name": user.display_name},
                "next": next_url,
            }
        )

    flash(f"Welcome, {user.display_name}!", "success")
    return redirect(next_url)


@bp.get("/login")
def login_form():
    """
    Show the login form.

    - Keeps track of a 'next' URL so we can redirect the user
      back to where they were trying to go.
    """
    next_url = request.args.get("next") or "/"
    return render_template("login.html", next_url=next_url)


@bp.post("/login")
def login_submit():
    """
    Handle user login from JSON or form POST.

    Steps:
    - Read username/password from JSON or form.
    - Normalize username.
    - Validate presence of both fields.
    - Check credentials against DB using check_password().
    - On success: set session["user_id"] and return JSON or redirect.
    - On failure: show error via JSON or Flash + redirect.
    """
    data = request.get_json(silent=True) or request.form

    username = _normalize_username(data.get("username"))
    password = data.get("password")

    if not username or not password:
        msg = "Username and password are required."
        if request.is_json:
            return jsonify({"ok": False, "error": msg}), 400
        flash(msg, "error")
        return redirect(url_for("auth.login_form"))

    user = User.query.filter_by(username=username).first()

    # invalid username or wrong password
    if not user or not user.check_password(password):
        msg = "Invalid username or password."
        if request.is_json:
            return jsonify({"ok": False, "error": msg}), 400
        flash(msg, "error")
        return redirect(url_for("auth.login_form"))

    # successful login: remember the user in session
    session["user_id"] = user.id
    next_url = url_for("pets.home_index")

    if request.is_json:
        return jsonify(
            {
                "ok": True,
                "user": {"id": user.id, "display_name": user.display_name},
                "next": next_url,
            }
        )

    flash(f"Welcome back, {user.display_name}!", "success")
    return redirect(next_url)


@bp.get("/profile")
@login_required
def profile_form():
    """
    Show the current user's profile page.

    - Requires the user to be logged in.
    - Loads the user from the DB based on session["user_id"].
    """
    uid = session.get("user_id")
    user = User.query.get(uid)
    return render_template("profile.html", user=user)


@bp.post("/profile")
@login_required
def profile_submit():
    """
    Update the current user's profile from a form POST.

    - Updates display name, email, phone.
    - Updates the 'public_contact' flag based on checkbox presence.
    - Saves changes to the database and reloads the profile page.
    """
    uid = session.get("user_id")
    user = User.query.get(uid)
    data = request.form

    # only overwrite fields if a new value is provided
    user.display_name = data.get("display_name") or user.display_name
    user.email = data.get("email") or user.email
    user.phone = data.get("phone") or user.phone

    # checkbox: if key exists in form, it's checked
    user.public_contact = "public_contact" in data

    db.session.commit()
    flash("Profile updated successfully!", "success")
    return redirect(url_for("auth.profile_form"))


@bp.post("/profile/toggle-contact")
@login_required
def toggle_public_contact():
    """
    Toggle the 'public_contact' boolean for the current user.

    - Useful for AJAX calls from the profile page.
    - Returns JSON with the new value.
    """
    uid = session.get("user_id")
    user = User.query.get(uid)

    user.public_contact = not user.public_contact
    db.session.commit()

    return jsonify({"ok": True, "public_contact": user.public_contact})


@bp.post("/logout")
def logout():
    """
    Log out the current user.

    - Clears 'user_id' from the session.
    - Redirects to the main pets home page.
    """
    session.pop("user_id", None)
    flash("You are logged out.", "success")
    return redirect(url_for("pets.home_index"))


@bp.get("/me")
def me():
    """
    Return JSON with the current logged-in user's basic info.

    - If not logged in, returns {"ok": False, "user": None}.
    - If logged in, returns minimal user fields that are safe to expose.
    """
    uid = session.get("user_id")
    if not uid:
        return jsonify({"ok": False, "user": None})

    u = User.query.get(uid)
    return jsonify(
        {
            "ok": True,
            "user": {
                "id": u.id,
                "username": u.username,
                "display_name": u.display_name,
                "email": u.email,
                "phone": u.phone,
                "public_contact": u.public_contact,
            },
        }
    )
