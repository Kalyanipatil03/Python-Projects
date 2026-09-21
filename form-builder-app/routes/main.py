import json
from database import db
from flask import Blueprint, redirect, render_template, request, url_for
from models import Form, FormResponse

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def dashboard():
  forms = Form.query.order_by(Form.created_at.desc()).all()
  return render_template("dashboard.html", forms=forms)


@main_bp.route("/builder")
def builder():
  return render_template("builder.html")


@main_bp.route("/form/<share_code>/responses")
def view_responses(share_code):
  form = Form.query.filter_by(share_code=share_code).first_or_404()
  responses = FormResponse.query.filter_by(form_id=form.id).all()

  parsed_responses = []
  for r in responses:
    parsed_responses.append({
        "id": r.id,
        "submitted_at": r.submitted_at.strftime("%b %d, %Y %H:%M"),
        "answers": json.loads(r.answers_json),
    })

  fields = json.loads(form.schema_json)
  return render_template(
      "responses.html", form=form, fields=fields, responses=parsed_responses
  )


@main_bp.route("/form/<share_code>/toggle", methods=["POST"])
def toggle_status(share_code):
  form = Form.query.filter_by(share_code=share_code).first_or_404()
  form.is_active = not form.is_active
  db.session.commit()
  return redirect(url_for("main.dashboard"))