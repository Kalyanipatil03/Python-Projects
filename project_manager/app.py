from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'project-flow-pro-2026-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project_manager.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# --- Models ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    projects = db.relationship('Project', backref='owner', lazy=True, cascade="all, delete-orphan")

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(100), default='Engineering')
    phase = db.Column(db.String(50), default='Initiation')  # Initiation, Planning, Execution, Closure
    budget = db.Column(db.Float, default=0.0)
    spent = db.Column(db.Float, default=0.0)
    start_date = db.Column(db.String(20), nullable=True)
    due_date = db.Column(db.String(20), nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tasks = db.relationship('Task', backref='project', lazy=True, cascade="all, delete-orphan")
    risks = db.relationship('Risk', backref='project', lazy=True, cascade="all, delete-orphan")

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    priority = db.Column(db.String(20), default='Medium')  # Low, Medium, High
    status = db.Column(db.String(20), default='To Do')     # To Do, In Progress, Completed
    assigned_to = db.Column(db.String(100), nullable=True)
    due_date = db.Column(db.String(20), nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

class Risk(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    severity = db.Column(db.String(20), default='Medium')  # Low, Medium, High
    mitigation = db.Column(db.Text, nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Routes ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash('Account already exists.', 'danger')
            return redirect(url_for('register'))
        hashed_password = generate_password_hash(password, method='scrypt')
        db.session.add(User(username=username, email=email, password=hashed_password))
        db.session.commit()
        flash('Account created! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid credentials.', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def dashboard():
    user_projects = Project.query.filter_by(owner_id=current_user.id).all()
    project_stats = []
    for proj in user_projects:
        total_tasks = len(proj.tasks)
        completed_tasks = sum(1 for t in proj.tasks if t.status == 'Completed')
        progress = int((completed_tasks / total_tasks * 100)) if total_tasks > 0 else 0
        budget_percent = int((proj.spent / proj.budget * 100)) if proj.budget > 0 else 0
        project_stats.append({
            'data': proj,
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'progress': progress,
            'budget_percent': budget_percent
        })
    return render_template('index.html', projects=project_stats)

@app.route('/create_project', methods=['POST'])
@login_required
def create_project():
    title = request.form.get('title')
    description = request.form.get('description')
    category = request.form.get('category')
    phase = request.form.get('phase')
    budget = float(request.form.get('budget') or 0.0)
    spent = float(request.form.get('spent') or 0.0)
    start_date = request.form.get('start_date')
    due_date = request.form.get('due_date')

    if title:
        new_proj = Project(
            title=title, description=description, category=category,
            phase=phase, budget=budget, spent=spent,
            start_date=start_date, due_date=due_date, owner_id=current_user.id
        )
        db.session.add(new_proj)
        db.session.commit()
        flash('New Project Initiated!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/delete_project/<int:id>')
@login_required
def delete_project(id):
    proj = Project.query.get_or_404(id)
    if proj.owner_id == current_user.id:
        db.session.delete(proj)
        db.session.commit()
        flash('Project archived.', 'info')
    return redirect(url_for('dashboard'))

@app.route('/project/<int:project_id>')
@login_required
def project_detail(project_id):
    project = Project.query.get_or_404(project_id)
    if project.owner_id != current_user.id:
        flash('Unauthorized.', 'danger')
        return redirect(url_for('dashboard'))

    todo_tasks = [t for t in project.tasks if t.status == 'To Do']
    in_progress_tasks = [t for t in project.tasks if t.status == 'In Progress']
    completed_tasks = [t for t in project.tasks if t.status == 'Completed']
    total = len(project.tasks)
    progress = int((len(completed_tasks) / total * 100)) if total > 0 else 0

    return render_template(
        'project_detail.html',
        project=project,
        todo_tasks=todo_tasks,
        in_progress_tasks=in_progress_tasks,
        completed_tasks=completed_tasks,
        progress=progress
    )

@app.route('/project/<int:project_id>/update_phase', methods=['POST'])
@login_required
def update_phase(project_id):
    project = Project.query.get_or_404(project_id)
    if project.owner_id == current_user.id:
        project.phase = request.form.get('phase')
        db.session.commit()
    return redirect(url_for('project_detail', project_id=project_id))

@app.route('/project/<int:project_id>/add_task', methods=['POST'])
@login_required
def add_task(project_id):
    project = Project.query.get_or_404(project_id)
    if project.owner_id == current_user.id:
        title = request.form.get('title')
        description = request.form.get('description')
        priority = request.form.get('priority')
        assigned_to = request.form.get('assigned_to')
        due_date = request.form.get('due_date')
        if title:
            db.session.add(Task(
                title=title, description=description, priority=priority,
                assigned_to=assigned_to, due_date=due_date, project_id=project.id
            ))
            db.session.commit()
    return redirect(url_for('project_detail', project_id=project_id))

@app.route('/task/<int:task_id>/move/<string:new_status>')
@login_required
def move_task(task_id, new_status):
    task = Task.query.get_or_404(task_id)
    if task.project.owner_id == current_user.id:
        task.status = new_status
        db.session.commit()
    return redirect(url_for('project_detail', project_id=task.project_id))

@app.route('/project/<int:project_id>/add_risk', methods=['POST'])
@login_required
def add_risk(project_id):
    project = Project.query.get_or_404(project_id)
    if project.owner_id == current_user.id:
        title = request.form.get('title')
        severity = request.form.get('severity')
        mitigation = request.form.get('mitigation')
        if title:
            db.session.add(Risk(title=title, severity=severity, mitigation=mitigation, project_id=project.id))
            db.session.commit()
    return redirect(url_for('project_detail', project_id=project_id))

@app.route('/risk/<int:risk_id>/delete')
@login_required
def delete_risk(risk_id):
    risk = Risk.query.get_or_404(risk_id)
    project_id = risk.project_id
    if risk.project.owner_id == current_user.id:
        db.session.delete(risk)
        db.session.commit()
    return redirect(url_for('project_detail', project_id=project_id))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)