import base64
import os
import secrets
import sqlite3
from functools import wraps
from pathlib import Path

from cryptography.fernet import Fernet, InvalidToken
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import pbkdf2_hmac

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "vault.db"
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", secrets.token_hex(32))
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

ITERATIONS = 600_000
VERIFIER = b"PASSWORD_VAULT_VERIFIER_V1"

def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS vault_meta (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            salt BLOB NOT NULL,
            verifier TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            website TEXT DEFAULT '',
            notes TEXT DEFAULT '',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def derive_key(master_password, salt):
    key = pbkdf2_hmac(
        "sha256",
        master_password.encode("utf-8"),
        salt,
        ITERATIONS,
        dklen=32,
    )
    return base64.urlsafe_b64encode(key)

def get_fernet():
    salt = session.get("vault_salt")
    if not salt:
        return None
    return Fernet(derive_key(session["master_password"], base64.b64decode(salt)))

def encrypt(value):
    return get_fernet().encrypt(value.encode()).decode()

def decrypt(value):
    return get_fernet().decrypt(value.encode()).decode()

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "master_password" not in session:
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped

@app.context_processor
def inject_globals():
    return {"vault_initialized": db_has_meta()}

def db_has_meta():
    conn = db()
    row = conn.execute("SELECT id FROM vault_meta WHERE id=1").fetchone()
    conn.close()
    return row is not None

@app.route("/")
def index():
    if "master_password" not in session:
        return redirect(url_for("login" if db_has_meta() else "setup"))
    return redirect(url_for("dashboard"))

@app.route("/setup", methods=["GET", "POST"])
def setup():
    if db_has_meta():
        return redirect(url_for("login"))
    if request.method == "POST":
        master = request.form.get("master_password", "")
        confirm = request.form.get("confirm_password", "")
        if len(master) < 8:
            flash("Master password must be at least 8 characters.", "danger")
        elif master != confirm:
            flash("Master passwords do not match.", "danger")
        else:
            salt = os.urandom(16)
            f = Fernet(derive_key(master, salt))
            verifier = f.encrypt(VERIFIER).decode()
            conn = db()
            conn.execute(
                "INSERT INTO vault_meta (id, salt, verifier) VALUES (1, ?, ?)",
                (salt, verifier),
            )
            conn.commit()
            conn.close()
            session["master_password"] = master
            session["vault_salt"] = base64.b64encode(salt).decode()
            flash("Vault created successfully.", "success")
            return redirect(url_for("dashboard"))
    return render_template("setup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if not db_has_meta():
        return redirect(url_for("setup"))
    if request.method == "POST":
        master = request.form.get("master_password", "")
        conn = db()
        row = conn.execute("SELECT salt, verifier FROM vault_meta WHERE id=1").fetchone()
        conn.close()
        salt = row["salt"]
        try:
            Fernet(derive_key(master, salt)).decrypt(row["verifier"].encode())
            session.clear()
            session["master_password"] = master
            session["vault_salt"] = base64.b64encode(salt).decode()
            return redirect(url_for("dashboard"))
        except InvalidToken:
            flash("Incorrect master password.", "danger")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/dashboard")
@login_required
def dashboard():
    conn = db()
    rows = conn.execute("SELECT id, title, username, website, notes, created_at, updated_at FROM entries ORDER BY updated_at DESC").fetchall()
    conn.close()
    entries = []
    for row in rows:
        entries.append({
            "id": row["id"],
            "title": decrypt(row["title"]),
            "username": decrypt(row["username"]),
            "website": decrypt(row["website"]) if row["website"] else "",
            "notes": decrypt(row["notes"]) if row["notes"] else "",
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
        })
    return render_template("dashboard.html", entries=entries)

@app.route("/entry/add", methods=["GET", "POST"])
@login_required
def add_entry():
    if request.method == "POST":
        data = {k: request.form.get(k, "").strip() for k in ["title", "username", "password", "website", "notes"]}
        if not data["title"] or not data["username"] or not data["password"]:
            flash("Title, username and password are required.", "danger")
            return render_template("entry_form.html", entry=data, mode="Add")
        conn = db()
        conn.execute(
            "INSERT INTO entries (title, username, password, website, notes) VALUES (?, ?, ?, ?, ?)",
            tuple(encrypt(data[k]) for k in ["title", "username", "password", "website", "notes"])
        )
        conn.commit()
        conn.close()
        flash("Password saved securely.", "success")
        return redirect(url_for("dashboard"))
    return render_template("entry_form.html", entry={}, mode="Add")

@app.route("/entry/<int:entry_id>/edit", methods=["GET", "POST"])
@login_required
def edit_entry(entry_id):
    conn = db()
    row = conn.execute("SELECT * FROM entries WHERE id=?", (entry_id,)).fetchone()
    conn.close()
    if not row:
        flash("Entry not found.", "danger")
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        data = {k: request.form.get(k, "").strip() for k in ["title", "username", "password", "website", "notes"]}
        if not data["title"] or not data["username"] or not data["password"]:
            flash("Title, username and password are required.", "danger")
            return render_template("entry_form.html", entry=data, mode="Edit")
        conn = db()
        conn.execute(
            """UPDATE entries SET title=?, username=?, password=?, website=?, notes=?,
               updated_at=CURRENT_TIMESTAMP WHERE id=?""",
            (*[encrypt(data[k]) for k in ["title", "username", "password", "website", "notes"]], entry_id)
        )
        conn.commit()
        conn.close()
        flash("Entry updated.", "success")
        return redirect(url_for("dashboard"))
    entry = {k: decrypt(row[k]) if row[k] else "" for k in ["title", "username", "password", "website", "notes"]}
    return render_template("entry_form.html", entry=entry, mode="Edit")

@app.post("/entry/<int:entry_id>/delete")
@login_required
def delete_entry(entry_id):
    conn = db()
    conn.execute("DELETE FROM entries WHERE id=?", (entry_id,))
    conn.commit()
    conn.close()
    flash("Entry deleted.", "success")
    return redirect(url_for("dashboard"))

@app.get("/api/password")
@login_required
def api_password():
    length = min(max(int(request.args.get("length", 16)), 8), 64)
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+"
    password = "".join(secrets.choice(alphabet) for _ in range(length))
    return jsonify(password=password)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
