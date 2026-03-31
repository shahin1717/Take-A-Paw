# seed.py
from app import create_app
from app.db import db
from app.models import Pet

SEED = [
    # Dogs
    {
        "name": "Buddy", "species": "Dog", "breed": "Golden Retriever", "age": "2 years",
        "gender": "Male", "location": "Hope Animal Shelter, New York, NY",
        "description": "Friendly and energetic. Loves playing fetch! Great with kids and pets.",
        "image": "https://images.unsplash.com/photo-1552053831-71594a27632d?w=900&h=600&fit=crop",
        "adopted": False, "source": "catalog", "owner_id": None,
        "home_type": "apartment", "activity_level": "low", "experience": "some",
        "time_commitment": "1_3_hours", "family_situation": "yes",
        "contact_email_override": "shelter@example.com",
        "contact_phone_override": "+1 555 0100", "public_contact": True
    },
    {
        "name": "Max", "species": "Dog", "breed": "Beagle", "age": "3 years",
        "gender": "Male", "location": "Happy Tails Sanctuary, Chicago, IL",
        "description": "Curious, friendly explorer who loves long walks.",
        "image": "https://images.pexels.com/photos/46505/swiss-shepherd-dog-dog-pet-portrait-46505.jpeg",
        "adopted": False, "source": "catalog", "owner_id": None,
        "home_type": "apartment", "activity_level": "high", "experience": "a_lot",
        "time_commitment": "more_than_3_hours", "family_situation": "yes",
        "contact_email_override": "shelter@example.com",
        "contact_phone_override": "+1 555 0102", "public_contact": True
    },
    {
        "name": "Rocky", "species": "Dog", "breed": "German Shepherd", "age": "4 years",
        "gender": "Male", "location": "Guardian Angels Shelter, Austin, TX",
        "description": "Loyal and protective. Great with families, needs daily exercise.",
        "image": "https://images.unsplash.com/photo-1568572933382-74d440642117?w=900&h=600&fit=crop",
        "adopted": False, "source": "catalog", "owner_id": None,
        "home_type": "house", "activity_level": "high", "experience": "a_lot",
        "time_commitment": "more_than_3_hours", "family_situation": "yes",
        "contact_email_override": "shelter@example.com",
        "contact_phone_override": "+1 555 0104", "public_contact": True
    },
    {
        "name": "Duke", "species": "Dog", "breed": "Labrador Retriever", "age": "5 years",
        "gender": "Male", "location": "Happy Tails, Boston, MA",
        "description": "Gentle giant who loves water and kids. Very well-trained.",
        "image": "https://images.unsplash.com/photo-1529429617124-95b109e86bb8?w=900&h=600&fit=crop",
        "adopted": False, "source": "catalog", "owner_id": None,
        "home_type": "house", "activity_level": "medium", "experience": "some",
        "time_commitment": "1_3_hours", "family_situation": "yes",
        "contact_email_override": "shelter@example.com",
        "contact_phone_override": "+1 555 0106", "public_contact": True
    },
    {
        "name": "Charlie", "species": "Dog", "breed": "French Bulldog", "age": "1 year",
        "gender": "Male", "location": "City Paws Rescue, San Francisco, CA",
        "description": "Adorable and low-energy companion. Perfect for apartments.",
        "image": "https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?w=900&h=600&fit=crop",
        "adopted": False, "source": "catalog", "owner_id": None,
        "home_type": "apartment", "activity_level": "low", "experience": "none",
        "time_commitment": "less_than_1_hour", "family_situation": "no",
        "contact_email_override": "shelter@example.com",
        "contact_phone_override": "+1 555 0107", "public_contact": True
    },
    
    # Cats
    {
        "name": "Luna", "species": "Cat", "breed": "Siamese", "age": "1 year",
        "gender": "Female", "location": "Paws Rescue Center, Los Angeles, CA",
        "description": "Affectionate and cuddly; prefers a calm home.",
        "image": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=900&h=600&fit=crop",
        "adopted": False, "source": "catalog", "owner_id": None,
        "home_type": "house", "activity_level": "medium", "experience": "some",
        "time_commitment": "1_3_hours", "family_situation": "no",
        "contact_email_override": "shelter@example.com",
        "contact_phone_override": "+1 555 0101", "public_contact": True
    },
    {
        "name": "Whiskers", "species": "Cat", "breed": "Persian", "age": "3 years",
        "gender": "Female", "location": "Cozy Paws Rescue, Seattle, WA",
        "description": "Calm and affectionate. Perfect lap cat who loves gentle pets.",
        "image": "https://images.unsplash.com/photo-1574158622682-e40e69881006?w=900&h=600&fit=crop",
        "adopted": False, "source": "catalog", "owner_id": None,
        "home_type": "apartment", "activity_level": "low", "experience": "none",
        "time_commitment": "1_3_hours", "family_situation": "no",
        "contact_email_override": "shelter@example.com",
        "contact_phone_override": "+1 555 0103", "public_contact": True
    },
    {
        "name": "Mittens", "species": "Cat", "breed": "Tabby", "age": "6 months",
        "gender": "Female", "location": "Little Paws Haven, Portland, OR",
        "description": "Playful kitten full of energy. Loves toys and climbing.",
        "image": "https://images.unsplash.com/photo-1495360010541-f48722b34f7d?w=900&h=600&fit=crop",
        "adopted": False, "source": "catalog", "owner_id": None,
        "home_type": "apartment", "activity_level": "medium", "experience": "some",
        "time_commitment": "1_3_hours", "family_situation": "yes",
        "contact_email_override": "shelter@example.com",
        "contact_phone_override": "+1 555 0105", "public_contact": True
    },
    {
        "name": "Shadow", "species": "Cat", "breed": "Black Shorthair", "age": "2 years",
        "gender": "Male", "location": "Midnight Rescue, Denver, CO",
        "description": "Independent but loving. Great mouser and loves windowsills.",
        "image": "https://images.unsplash.com/photo-1529778873920-4da4926a72c2?w=900&h=600&fit=crop",
        "adopted": False, "source": "catalog", "owner_id": None,
        "home_type": "house", "activity_level": "low", "experience": "some",
        "time_commitment": "less_than_1_hour", "family_situation": "no",
        "contact_email_override": "shelter@example.com",
        "contact_phone_override": "+1 555 0108", "public_contact": True
    },
    {
        "name": "Ginger", "species": "Cat", "breed": "Orange Tabby", "age": "4 years",
        "gender": "Female", "location": "Sunny Days Shelter, Miami, FL",
        "description": "Sweet and social. Loves attention and sunny spots.",
        "image": "https://images.unsplash.com/photo-1574158622682-e40e69881006?w=900&h=600&fit=crop",
        "adopted": False, "source": "catalog", "owner_id": None,
        "home_type": "apartment", "activity_level": "low", "experience": "none",
        "time_commitment": "1_3_hours", "family_situation": "yes",
        "contact_email_override": "shelter@example.com",
        "contact_phone_override": "+1 555 0109", "public_contact": True
    }
]


def main():
    app = create_app()
    with app.app_context():
        print("DB URI:", app.config["SQLALCHEMY_DATABASE_URI"])
        
        db.create_all()

        current = Pet.query.count()
        print("Existing pets:", current)

        added_count = 0
        for row in SEED:
            existing = Pet.query.filter_by(name=row["name"], species=row["species"]).first()
            if not existing:
                db.session.add(Pet(**row))
                added_count += 1
                print(f"Added {row['name']} the {row['species']}")

        if added_count > 0:
            db.session.commit()
            print(f"Seeded {added_count} new pets.")
        else:
            print("All pets already exist in database.")

        # current state
        total_pets = Pet.query.count()
        adopted_count = Pet.query.filter_by(adopted=True).count()
        available_count = Pet.query.filter_by(adopted=False).count()
        
        print(f"\n Database Summary:")
        print(f"   Total pets: {total_pets}")
        print(f"   Available: {available_count}")
        print(f"   Adopted: {adopted_count}")

        print(f"\n🐾 All pets in database:")
        pets = Pet.query.order_by(Pet.id).all()
        for p in pets:
            status = "ADOPTED" if p.adopted else "AVAILABLE"
            print(f"   {p.id:2d}. {p.name:10} ({p.species:5}) - {p.breed:20} - {status}")

if __name__ == "__main__":
    main()

