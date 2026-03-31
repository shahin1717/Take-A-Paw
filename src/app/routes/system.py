from flask import Blueprint, jsonify
from ..models import Pet, User

bp = Blueprint("system", __name__)

@bp.get("/health")
def health():
    """
    Simple ping endpoint used by CI/CD or uptime monitors.
    Returns a minimal OK payload.
    """
    return jsonify({"status": "ok", "service": "take-a-paw"}), 200


@bp.get("/api/status")
def api_status():
    """
    Returns a more detailed status including stub API checks.
    Later, we can extend this to verify Cat/Dog API connectivity.
    """
    try:
        pets_count = Pet.query.count()
        users_count = User.query.count()
    except Exception:
        pets_count = None
        users_count = None

    return jsonify({
        "status": "ok",
        "cat_api_working": True,
        "dog_api_working": True,
        "pets_in_db": pets_count,
        "users_in_db": users_count,
        "note": "system operational"
    }), 200


@bp.get("/debug")
def debug():
    """
    Lightweight internal debug info.
    Avoid exposing secrets or environment variables here.
    """
    try:
        total_pets = Pet.query.count()
        adopted = Pet.query.filter_by(adopted=True).count()
        available = Pet.query.filter_by(adopted=False).count()
    except Exception:
        total_pets = adopted = available = 0

    return jsonify({
        "ok": True,
        "stats": {
            "total_pets": total_pets,
            "available": available,
            "adopted": adopted
        },
        "note": "debug endpoint for developers"
    }), 200


@bp.get("/health/db")
def health_db():
    """
    Returns counts of key entities to confirm DB connectivity.
    """
    try:
        from ..models import Favorite 
        fav_count = Favorite.query.count()
    except Exception:
        fav_count = 0

    return jsonify({
        "status": "ok",
        "pets_total": Pet.query.count(),
        "pets_available": Pet.query.filter_by(adopted=False).count(),
        "users": User.query.count(),
        "favorites": fav_count,
    }), 200
