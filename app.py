from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_restful import Api

from config import Config
from models import db, bcrypt
from resources.auth import Signup, Login, Me
from resources.notes import Notes, NoteDetail


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    Migrate(app, db)
    JWTManager(app)

    api = Api(app)

    api.add_resource(Signup, "/signup")
    api.add_resource(Login, "/login")
    api.add_resource(Me, "/me")
    api.add_resource(Notes, "/notes")
    api.add_resource(NoteDetail, "/notes/<int:note_id>")

    return app


app = create_app()


@app.route("/")
def index():
    return {
        "message": "Full Auth Flask Backend API is running"
    }


if __name__ == "__main__":
    app.run(debug=True)
