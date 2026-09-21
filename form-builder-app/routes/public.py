import json
from database import db
from flask import Blueprint, render_template, request
from models import Form, FormResponse

public_bp = Blueprint("public", __name__)


@public_bp.route("/s/<share_code>")
def render_public_form(share_code):
  form = Form.query.filter_by(
      share_code=share_code, is_active=True
  ).first_or_404()
  fields = json.loads(form.schema_json)
  return render_template("public_form.html", form=form, fields=fields)


@public_bp.route("/s/<share_code>/submit", methods=["POST"])
def submit_form(share_code):
  form = Form.query.filter_by(
      share_code=share_code, is_active=True
  ).first_or_404()
  fields = json.loads(form.schema_json)

  answers = {}
  for field in fields:
    field_id = field["id"]
    if field["type"] == "checkbox":
      answers[field["label"]] = request.form.getlist(field_id)
    else:
      answers[field["label"]] = request.form.get(field_id, "").strip()

  new_response = FormResponse(
      form_id=form.id, answers_json=json.dumps(answers)
  )

  db.session.add(new_response)
  db.session.commit()

  return render_template("public_form.html", form=form, submitted=True)