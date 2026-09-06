from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required

from models import db, Note


class Notes(Resource):

    @jwt_required()
    def get(self):
        user_id = int(get_jwt_identity())

        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)

        if page < 1:
            page = 1

        if per_page < 1:
            per_page = 10

        if per_page > 100:
            per_page = 100

        pagination = Note.query.filter_by(
            user_id=user_id
        ).order_by(
            Note.id.desc()
        ).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        return {
            "notes": [note.to_dict() for note in pagination.items],
            "pagination": {
                "page": pagination.page,
                "per_page": pagination.per_page,
                "total": pagination.total,
                "pages": pagination.pages,
                "has_next": pagination.has_next,
                "has_prev": pagination.has_prev
            }
        }, 200

    @jwt_required()
    def post(self):
        data = request.get_json()

        if not data:
            return {"error": "Request body is required"}, 400

        title = data.get("title")
        content = data.get("content")

        if not title or not content:
            return {
                "error": "Title and content are required"
            }, 400

        title = title.strip()
        content = content.strip()

        if not title or not content:
            return {
                "error": "Title and content cannot be empty"
            }, 400

        user_id = int(get_jwt_identity())

        note = Note(
            title=title,
            content=content,
            user_id=user_id
        )

        db.session.add(note)
        db.session.commit()

        return {
            "message": "Note created successfully",
            "note": note.to_dict()
        }, 201


class NoteDetail(Resource):

    @jwt_required()
    def get(self, note_id):
        user_id = int(get_jwt_identity())

        note = db.session.get(Note, note_id)

        if not note:
            return {"error": "Note not found"}, 404

        if note.user_id != user_id:
            return {"error": "You do not have access to this note"}, 403

        return {
            "note": note.to_dict()
        }, 200

    @jwt_required()
    def patch(self, note_id):
        user_id = int(get_jwt_identity())

        note = db.session.get(Note, note_id)

        if not note:
            return {"error": "Note not found"}, 404

        if note.user_id != user_id:
            return {"error": "You do not have access to this note"}, 403

        data = request.get_json()

        if not data:
            return {"error": "Request body is required"}, 400

        if "title" in data:
            title = data["title"]

            if not isinstance(title, str) or not title.strip():
                return {
                    "error": "Title cannot be empty"
                }, 400

            note.title = title.strip()

        if "content" in data:
            content = data["content"]

            if not isinstance(content, str) or not content.strip():
                return {
                    "error": "Content cannot be empty"
                }, 400

            note.content = content.strip()

        db.session.commit()

        return {
            "message": "Note updated successfully",
            "note": note.to_dict()
        }, 200

    @jwt_required()
    def delete(self, note_id):
        user_id = int(get_jwt_identity())

        note = db.session.get(Note, note_id)

        if not note:
            return {"error": "Note not found"}, 404

        if note.user_id != user_id:
            return {"error": "You do not have access to this note"}, 403

        db.session.delete(note)
        db.session.commit()

        return {
            "message": "Note deleted successfully"
        }, 200
