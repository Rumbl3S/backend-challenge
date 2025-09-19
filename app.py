from flask import Flask, request, jsonify
from models import db, Club, User, Comment

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///clubs.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

@app.route("/api/clubs", methods=["GET"])
def get_clubs():
    clubs = Club.query.all()
    return jsonify([c.to_dict() for c in clubs])

@app.route("/api/clubs/<int:club_id>", methods=["GET"])
def get_club(club_id):
    club = Club.query.get_or_404(club_id)
    return jsonify(club.to_dict())

@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.get_json()
    user = User(username=data["username"], email=data.get("email"))
    db.session.add(user)
    db.session.commit()
    return jsonify({"id": user.id, "username": user.username}), 201

@app.route("/api/clubs/<int:club_id>/comments", methods=["POST"])
def post_comment(club_id):
    data = request.get_json()
    comment = Comment(
        content=data["content"],
        club_id=club_id,
        user_id=data["user_id"],
        parent_id=data.get("parent_id")
    )
    db.session.add(comment)
    db.session.commit()
    return jsonify({"id": comment.id, "content": comment.content}), 201

@app.route("/api/clubs/<int:club_id>/comments", methods=["GET"])
def get_comments(club_id):
    comments = Comment.query.filter_by(club_id=club_id, parent_id=None).all()
    def serialize(comment):
        return {
            "id": comment.id,
            "user": comment.user.username,
            "content": comment.content,
            "replies": [serialize(r) for r in comment.replies]
        }
    return jsonify([serialize(c) for c in comments])

if __name__ == "__main__":
    app.run(debug=True)
