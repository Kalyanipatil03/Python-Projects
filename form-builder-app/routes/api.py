import json
from database import db
from flask import Blueprint, jsonify, request
from models import Form

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/forms/create", methods=["POST"])
def create_form():
  data = request.get_json()

  if not data or "title" not in data or "fields" not in data:
    return jsonify({"error": "Title and fields are required"}), 400

  new_form = Form(
      title=data["title"],
      description=data.get("description", ""),
      schema_json=json.dumps(data["fields"]),
  )

  db.session.add(new_form)
  db.session.commit()

  return (
      jsonify({
          "success": True,
          "share_code": new_form.share_code,
          "redirect_url": f"/form/{new_form.share_code}/responses",
      }),
      201,
  )