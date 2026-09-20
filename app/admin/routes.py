from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.extensions import db
from app.models.user import User, StudentProfile, FacultyProfile
from app.models.academic import Department, Course, Subject, Enrollment

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'admin':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.index'))

    total_students = StudentProfile.query.count()
    total_faculty = FacultyProfile.query.count()
    total_depts = Department.query.count()
    total_courses = Course.query.count()

    students = StudentProfile.query.all()
    faculty = FacultyProfile.query.all()
    departments = Department.query.all()
    courses = Course.query.all()

    return render_template(
        'admin/dashboard.html',
        total_students=total_students,
        total_faculty=total_faculty,
        total_depts=total_depts,
        total_courses=total_courses,
        students=students,
        faculty=faculty,
        departments=departments,
        courses=courses
    )

@admin_bp.route('/add-user', methods=['POST'])
@login_required
def add_user():
    if current_user.role != 'admin':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.index'))

    role = request.form.get('role')
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')

    # Check existing user
    if User.query.filter((User.username == username) | (User.email == email)).first():
        flash('Username or Email already exists.', 'danger')
        return redirect(url_for('admin.dashboard'))

    new_user = User(username=username, email=email, role=role)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.flush()

    if role == 'student':
        roll_number = request.form.get('roll_number')
        dept_id = request.form.get('department_id')
        course_id = request.form.get('course_id')
        semester = request.form.get('semester', 1)

        student_profile = StudentProfile(
            user_id=new_user.id,
            roll_number=roll_number,
            first_name=first_name,
            last_name=last_name,
            department_id=dept_id,
            course_id=course_id,
            semester=semester
        )
        db.session.add(student_profile)

    elif role == 'faculty':
        employee_id = request.form.get('employee_id')
        dept_id = request.form.get('department_id')

        faculty_profile = FacultyProfile(
            user_id=new_user.id,
            employee_id=employee_id,
            first_name=first_name,
            last_name=last_name,
            department_id=dept_id
        )
        db.session.add(faculty_profile)

    db.session.commit()
    flash(f'{role.capitalize()} account created successfully!', 'success')
    return redirect(url_for('admin.dashboard'))