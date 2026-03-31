from functools import wraps
from flask import session, redirect, url_for, request, flash, jsonify


def login_required(view):
    """
    Decorator to protect routes that require a logged-in user.

    - If there is no 'user_id' in the session, redirects to the login page.
    - Passes the original path in the 'next' parameter so we can come back
      to the same page after a successful login.
    """
    @wraps(view)
    def wrapper(*args, **kwargs):
        # if user is not logged in, send them to the login form
        if not session.get("user_id"):
            flash("Please log in first.", "error")
            return redirect(url_for("auth.login_form", next=request.path))
        # otherwise, continue to the original view
        return view(*args, **kwargs)

    return wrapper


def admin_required(f):
    """
    Decorator to restrict access to admin-only routes (JSON API style).

    - Checks that the current session has role == 'admin'.
    - If not, returns a 403 JSON response instead of redirecting.
      (useful for API endpoints or AJAX requests).
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        # only allow access if the session indicates an admin role
        if session.get("role") != "admin":
            return jsonify({"ok": False, "error": "admin access required"}), 403
        # user is admin, proceed with the original function
        return f(*args, **kwargs)

    return decorated
