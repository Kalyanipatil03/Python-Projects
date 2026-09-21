import uuid
from datetime import datetime
from database import db


class Form(db.Model):
  __tablename__ = "forms"

  id = db.Column(db.Integer, primary_key=True)
  share_code = db.Column(
      db.String(36),
      unique=True,
      nullable=False,
      default=lambda: str(uuid.uuid4())[:8],
  )
  title = db.Column(db.String(150), nullable=False)
  description = db.Column(db.Text, nullable=True)
  schema_json = db.Column(db.Text, nullable=False)  # JSON fields layout
  is_active = db.Column(db.Boolean, default=True)
  created_at = db.Column(db.DateTime, default=datetime.utcnow)

  responses = db.relationship(
      "FormResponse", backref="form", lazy=True, cascade="all, delete-orphan"
  )


class FormResponse(db.Model):
  __tablename__ = "form_responses"

  id = db.Column(db.Integer, primary_key=True)
  form_id = db.Column(db.Integer, db.ForeignKey("forms.id"), nullable=False)
  answers_json = db.Column(db.Text, nullable=False)
  submitted_at = db.Column(db.DateTime, default=datetime.utcnow)