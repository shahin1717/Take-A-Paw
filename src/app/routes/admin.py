from flask import Blueprint, render_template, session, redirect, url_for, flash, request, jsonify
from functools import wraps
from ..models import Pet, User
from sqlalchemy import func
from datetime import date
from ..db import db  

# blueprint for all admin-related routes, mounted under /admin
bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required(f):
    """
    Decorator to restrict access to admin-only routes.

    - Checks the session for role == "admin".
    - If not admin, flashes an error and redirects to the admin login form.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        # if current user is not marked as admin in the session, deny access
        if session.get("role") != "admin":
            flash("Admin access required", "error")
            return redirect(url_for("admin.admin_login_form"))
        return f(*args, **kwargs)
    return wrapper


@bp.get("/")
def admin_home():
    """
    Entry point for /admin.

    - If already logged in as admin, send them to the dashboard.
    - Otherwise, show the admin login page.
    """
    if session.get("role") == "admin":
        return redirect(url_for("admin.admin_dashboard"))
    return redirect(url_for("admin.admin_login_form"))


@bp.get("/login")
def admin_login_form():
    """
    Render the admin login page.
    """
    return render_template("admin_login.html")


@bp.post("/login")
def admin_login_submit():
    """
    Handle admin login form submission.

    - For now, uses a hardcoded username and password.
    - On success, sets admin info in the session and redirects to dashboard.
    - On failure, shows an error and reloads the login form.
    """
    username = "admin"
    password = "supersecret"

    # get username and password from form
    form_user = request.form.get("username")
    form_pass = request.form.get("password")

    # simple credentials check
    if form_user == username and form_pass == password:
        session["user_id"] = 0  # special id for admin (not a real user in db)
        session["role"] = "admin"
        flash("Logged in as admin", "success")
        return redirect(url_for("admin.admin_dashboard"))

    flash("Invalid admin credentials", "error")
    return redirect(url_for("admin.admin_login_form"))


@bp.post("/logout")
def admin_logout():
    """
    Log out the current admin.

    - Clears user_id and role from the session.
    - Redirects back to the admin login page.
    """
    session.pop("user_id", None)
    session.pop("role", None)
    flash("Logged out", "success")
    return redirect(url_for("admin.admin_login_form"))


@bp.get("/dashboard")
@admin_required
def admin_dashboard():
    """
    Show the main admin dashboard.

    - Pet stats: how many pets are available vs adopted.
    - User stats: total users, users created today, active users today.
    """
    # pet statistics
    stats = {
        "available": Pet.query.filter_by(adopted=False).count(),
        "adopted": Pet.query.filter_by(adopted=True).count()
    }

    today = date.today()

    # user statistics
    user_stats = {
        "total_users": User.query.count(),
        "created_today": User.query.filter(func.date(User.created_at) == today).count(),
        "active_today": User.query.filter(func.date(User.created_at) == today).count()
    }

    return render_template(
        "admin_dashboard.html",
        stats=stats,
        user_stats=user_stats,
        active="dashboard"
    )


@bp.get("/charts")
@admin_required
def admin_charts():
    """
    Render the charts page for admin.

    - species_counts: how many pets per species.
    - age_counts: how many pets per age.
    - users_counts: number of users created per day over the last 7 days.
    """
    # number of pets by species
    species_counts = {
        row[0]: row[1]
        for row in Pet.query.with_entities(Pet.species, func.count(Pet.id))
        .group_by(Pet.species)
        .all()
    }

    # number of pets by age
    age_counts = {
        row[0]: row[1]
        for row in Pet.query.with_entities(Pet.age, func.count(Pet.id))
        .group_by(Pet.age)
        .all()
    }

    # users created per day for the last 7 days (including today)
    from datetime import timedelta
    users_counts = {}
    for i in range(7):
        day = date.today() - timedelta(days=i)
        count = User.query.filter(func.date(User.created_at) == day).count()
        users_counts[str(day)] = count

    return render_template(
        "admin_charts.html",
        species_counts=species_counts,
        age_counts=age_counts,
        users_counts=users_counts,
        active="charts"
    )


@bp.get("/users")
@admin_required
def admin_users():
    """
    Show the list of all users in the system, ordered by newest first.
    """
    users = User.query.order_by(User.id.desc()).all()
    return render_template("admin_users.html", users=users, active="users")


@bp.get("/pets")
@admin_required
def admin_pets():
    """
    Show the list of all pets, ordered by creation date (newest first).
    """
    pets = Pet.query.order_by(Pet.created_at.desc()).all()
    return render_template("admin_pets.html", pets=pets, active="pets")


@bp.post("/users/delete/<int:user_id>")
@admin_required
def admin_delete_user(user_id):
    """
    Delete a user by id.

    - Only accessible to admins.
    - If user is not found, returns 404.
    """
    # find user or return 404
    user = User.query.get_or_404(user_id)

    # delete user from db
    db.session.delete(user)
    db.session.commit()

    flash(f"User {user.username} deleted.", "success")
    return redirect(url_for("admin.admin_users"))


@bp.post("/pets/delete/<int:pet_id>")
@admin_required
def admin_delete_pet(pet_id):
    """
    Delete a pet by id.

    - Only accessible to admins.
    - If pet is not found, returns 404.
    """
    # find pet or return 404
    pet = Pet.query.get_or_404(pet_id)

    # delete pet from db
    db.session.delete(pet)
    db.session.commit()

    flash(f"Pet {pet.name} deleted.", "success")
    return redirect(url_for("admin.admin_pets"))
