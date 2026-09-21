from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-task-manager-2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task_manager_v2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    tasks = db.relationship('Task', backref='owner', lazy=True)

# Task Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    priority = db.Column(db.String(20), default='Medium')  # Low, Medium, High
    status = db.Column(db.String(20), default='Pending')    # Pending, In Progress, Completed
    due_date = db.Column(db.String(20), nullable=True)
    assigned_to = db.Column(db.String(100), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Auth Routes ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        user_exists = User.query.filter((User.username == username) | (User.email == email)).first()
        if user_exists:
            flash('Username or Email already exists.', 'danger')
            return redirect(url_for('register'))
            
        hashed_password = generate_password_hash(password, method='scrypt')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully! Please log in.', 'success')
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
        else:
            flash('Invalid email or password.', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# --- Dashboard Route ---
@app.route('/')
@login_required
def dashboard():
    user_tasks = Task.query.filter_by(user_id=current_user.id).all()
    
    total_tasks = len(user_tasks)
    completed_tasks = sum(1 for t in user_tasks if t.status == 'Completed')
    in_progress = sum(1 for t in user_tasks if t.status == 'In Progress')
    high_priority = sum(1 for t in user_tasks if t.priority == 'High')
    progress_percentage = int((completed_tasks / total_tasks * 100)) if total_tasks > 0 else 0

    return render_template(
        'index.html', 
        tasks=user_tasks, 
        total=total_tasks, 
        completed=completed_tasks, 
        in_progress=in_progress,
        high_prio=high_priority,
        progress=progress_percentage
    )

# --- Dedicated Filter Routes (Redirect to separate page) ---
@app.route('/filter/<filter_type>')
@login_required
def filter_tasks(filter_type):
    query = Task.query.filter_by(user_id=current_user.id)
    
    if filter_type == 'completed':
        filtered_tasks = query.filter_by(status='Completed').all()
        title = "Completed Tasks"
        badge_color = "bg-emerald-500"
    elif filter_type == 'in_progress':
        filtered_tasks = query.filter_by(status='In Progress').all()
        title = "In Progress Tasks"
        badge_color = "bg-amber-500"
    elif filter_type == 'high_priority':
        filtered_tasks = query.filter_by(priority='High').all()
        title = "High Priority Tasks"
        badge_color = "bg-rose-500"
    else:  # 'all'
        filtered_tasks = query.all()
        title = "All Registered Tasks"
        badge_color = "bg-indigo-500"

    return render_template('filter_tasks.html', tasks=filtered_tasks, title=title, filter_type=filter_type, badge_color=badge_color)

# --- Dedicated Principle Detail Routes (Redirect to separate page) ---
@app.route('/principle/<int:principle_id>')
@login_required
def principle_detail(principle_id):
    principles_data = {
        1: {
            "title": "01. Prioritization Framework",
            "tag": "Focus Management",
            "color": "from-amber-500 to-orange-600",
            "description": "Rank your tasks by urgency and importance (High, Medium, Low) to maximize focus on key objectives.",
            "action_filter": "high_priority",
            "filter_label": "View All High Priority Tasks"
        },
        2: {
            "title": "02. Milestone Tracking",
            "tag": "Goal Progress",
            "color": "from-rose-500 to-pink-600",
            "description": "Break down large goals into measurable milestones and track percentage metrics in real time.",
            "action_filter": "completed",
            "filter_label": "View Completed Milestones"
        },
        3: {
            "title": "03. Schedule Management",
            "tag": "Time Boxing",
            "color": "from-emerald-500 to-teal-600",
            "description": "Set clear deadlines and target execution dates to avoid bottlenecks and deliver work on time.",
            "action_filter": "all",
            "filter_label": "View All Scheduled Tasks"
        },
        4: {
            "title": "04. Resource Allocation",
            "tag": "Team Delegation",
            "color": "from-sky-500 to-blue-600",
            "description": "Assign specific tasks to individual team members or dedicated resources for clear accountability.",
            "action_filter": "in_progress",
            "filter_label": "View Active Allocated Tasks"
        },
        5: {
            "title": "05. Collaboration & Workspaces",
            "tag": "Multi-user Access",
            "color": "from-purple-500 to-indigo-600",
            "description": "Maintain secure isolated workspaces for individual users with session protection and password hashing.",
            "action_filter": "all",
            "filter_label": "Return to Main Dashboard"
        }
    }
    
    data = principles_data.get(principle_id, principles_data[1])
    return render_template('principle.html', p=data, pid=principle_id)

# --- CRUD Operations ---
@app.route('/add_task', methods=['POST'])
@login_required
def add_task():
    title = request.form.get('title')
    description = request.form.get('description')
    priority = request.form.get('priority')
    due_date = request.form.get('due_date')
    assigned_to = request.form.get('assigned_to')

    if title:
        task = Task(
            title=title, 
            description=description, 
            priority=priority, 
            due_date=due_date, 
            assigned_to=assigned_to,
            user_id=current_user.id
        )
        db.session.add(task)
        db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/update/<int:id>/<string:status>')
@login_required
def update_status(id, status):
    task = Task.query.get_or_404(id)
    if task.user_id == current_user.id:
        task.status = status
        db.session.commit()
    return redirect(request.referrer or url_for('dashboard'))

@app.route('/delete/<int:id>')
@login_required
def delete_task(id):
    task = Task.query.get_or_404(id)
    if task.user_id == current_user.id:
        db.session.delete(task)
        db.session.commit()
    return redirect(request.referrer or url_for('dashboard'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)