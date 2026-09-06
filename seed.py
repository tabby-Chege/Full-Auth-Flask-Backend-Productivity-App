from app import app
from models import db, User, Note


def seed_database():
    with app.app_context():
        db.drop_all()
        db.create_all()

        tabby = User(username="Tabby")
        tabby.set_password("password123")

        prince = User(username="Prince")
        prince.set_password("password123")

        zakaria = User(username="Zakaria")
        zakaria.set_password("password123")

        wesley = User(username="Wesley")
        wesley.set_password("password123")

        db.session.add_all([
            tabby,
            prince,
            zakaria,
            wesley
        ])

        db.session.flush()

        notes = [
            Note(
                title="My First Note",
                content="Welcome to the productivity app.",
                user_id=tabby.id
            ),
            Note(
                title="Project Ideas",
                content="Work on the Flask authentication project.",
                user_id=prince.id
            ),
            Note(
                title="Study Plan",
                content="Review Flask, SQLAlchemy and JWT authentication.",
                user_id=zakaria.id
            ),
            Note(
                title="Weekly Goals",
                content="Complete this week's productivity goals.",
                user_id=wesley.id
            )
        ]

        db.session.add_all(notes)
        db.session.commit()

        print("Database seeded successfully!")


if __name__ == "__main__":
    seed_database()
