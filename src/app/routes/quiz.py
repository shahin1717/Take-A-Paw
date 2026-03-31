from flask import Blueprint, jsonify, request, render_template
from ..models import Pet

bp = Blueprint("quiz", __name__)


@bp.get("/quiz/info")
def quiz_info():
    """
    Provide instructions for how to use the quiz API.

    - Useful for debugging or frontend developers.
    - Returns a JSON message describing the expected POST payload.
    """
    return jsonify({
        "ok": True,
        "message": (
            "Submit POST /quiz/results with JSON: "
            "{home_type, activity_level, experience, time_commitment, family_situation}"
        )
    })


@bp.post("/quiz/results")
def quiz_results():
    """
    Process quiz results and return matching pets.

    Expected JSON fields:
    - home_type
    - activity_level
    - experience
    - time_commitment
    - family_situation

    Steps:
    - Read JSON body.
    - Validate that data exists.
    - Build a dynamic query filtering only non-adopted pets.
    - Apply filters only for parameters the user actually provided.
    - Limit results to 10 newest pets.
    - Return match list (id, name, species, breed, location) or an error message.
    """
    data = request.get_json(silent=True) or {}
    print("Received data:", data)

    # basic validation
    if not data:
        return jsonify({
            "ok": False,
            "message": "Invalid data received"
        })

    # start with non-adopted pets
    query = Pet.query.filter_by(adopted=False)

    # apply optional filters
    if data.get("home_type"):
        query = query.filter(Pet.home_type == data["home_type"])

    if data.get("activity_level"):
        query = query.filter(Pet.activity_level == data["activity_level"])

    if data.get("experience"):
        query = query.filter(Pet.experience == data["experience"])

    if data.get("time_commitment"):
        query = query.filter(Pet.time_commitment == data["time_commitment"])

    if data.get("family_situation"):
        query = query.filter(Pet.family_situation == data["family_situation"])

    # attempt to retrieve matching pets
    try:
        pets = query.order_by(Pet.created_at.desc()).limit(10).all()
    except Exception as e:
        print("Error querying pets:", e)
        return jsonify({
            "ok": False,
            "message": "An error occurred while querying pets"
        })

    # no matches found
    if not pets:
        return jsonify({
            "ok": False,
            "message": "No pets match your criteria"
        })

    # return minimal pet info
    return jsonify({
        "ok": True,
        "criteria": data,
        "matches": [
            {
                "id": p.id,
                "name": p.name,
                "species": p.species,
                "breed": p.breed,
                "location": p.location
            }
            for p in pets
        ]
    })


@bp.get("/quiz")
def quiz_page():
    """
    Render the HTML quiz page.

    - Frontend page where the user answers questions.
    - Submits quiz answers to /quiz/results via JavaScript.
    """
    return render_template("quiz.html")
