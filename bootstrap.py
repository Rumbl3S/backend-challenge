import json
from app import app
from models import db, Club, Tag, User

def create_user():
    # create Josh
    josh = User(username="josh", email="josh@example.com")
    db.session.add(josh)
    db.session.commit()

def load_json():
    with open("clubs.json") as f:
        clubs_data = json.load(f)

    for club_json in clubs_data:
        club = Club(
            name=club_json.get("name"),
            description=club_json.get("description"),
            website=club_json.get("website"),
            email=club_json.get("email"),
        )

        # handle tags
        for tag_name in club_json.get("tags", []):
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.session.add(tag)
            club.tags.append(tag)

        db.session.add(club)

    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()
        create_user()
        load_json()
        print("Database bootstrapped with user + clubs")
