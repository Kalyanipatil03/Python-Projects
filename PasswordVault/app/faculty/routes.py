from datetime import datetime, date
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.extensions import db
from app.models.academic import Subject, Enrollment
from app.models.modules import Attendance, Notice, LeaveApplication

faculty_bp = Blueprint('faculty', __name__)


@faculty_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'faculty':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.index'))

    profile = current_user.faculty_profile
    if not profile:
        flash('Faculty profile not found.', 'danger')
        return redirect(url_for('main.index'))

    subjects = Subject.query.filter_by(faculty_id=profile.id).all()
    notices = Notice.query.order_by(Notice.created_at.desc()).limit(5).all()

    return render_template(
        'faculty/dashboard.html',
        profile=profile,
        subjects=subjects,
        notices=notices
    )


@faculty_bp.route('/attendance/mark/<int:subject_id>', methods=['GET', 'POST'])
@login_required
def mark_attendance(subject_id):
    if current_user.role != 'faculty':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.index'))

    profile = current_user.faculty_profile
    subject = Subject.query.get_or_404(subject_id)

    if subject.faculty_id != profile.id:
        flash('You are not authorized to mark attendance for this subject.', 'danger')
        return redirect(url_for('faculty.dashboard'))

    enrollments = Enrollment.query.filter_by(subject_id=subject.id).all()
    students = [e.student for e in enrollments]

    selected_date_str = request.args.get('date', date.today().strftime('%Y-%m-%d'))
    try:
        selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
    except ValueError:
        selected_date = date.today()

    if request.method == 'POST':
        selected_date = datetime.strptime(request.form.get('attendance_date'), '%Y-%m-%d').date()
        present_student_ids = request.form.getlist('present_students')

        for student in students:
            is_present = str(student.id) in present_student_ids

            existing_record = Attendance.query.filter_by(
                student_id=student.id,
                subject_id=subject.id,
                date=selected_date
            ).first()

            if existing_record:
                existing_record.is_present = is_present
            else:
                new_record = Attendance(
                    student_id=student.id,
                    subject_id=subject.id,
                    date=selected_date,
                    is_present=is_present
                )
                db.session.add(new_record)

        db.session.commit()
        flash(f'Attendance successfully saved for {subject.name} on {selected_date}!', 'success')
        return redirect(url_for('faculty.dashboard'))

    existing_attendance = {
        att.student_id: att.is_present
        for att in Attendance.query.filter_by(subject_id=subject.id, date=selected_date).all()
    }

    return render_template(
        'faculty/mark_attendance.html',
        subject=subject,
        students=students,
        selected_date=selected_date.strftime('%Y-%m-%d'),
        existing_attendance=existing_attendance
    )


@faculty_bp.route('/leaves')
@login_required
def manage_leaves():
    if current_user.role != 'faculty':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.index'))

    applications = LeaveApplication.query.order_by(LeaveApplication.applied_on.desc()).all()
    return render_template('faculty/manage_leaves.html', applications=applications)


@faculty_bp.route('/leaves/<int:leave_id>/<string:action>')
@login_required
def process_leave(leave_id, action):
    if current_user.role != 'faculty':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.index'))

    leave = LeaveApplication.query.get_or_404(leave_id)
    if action == 'approve':
        leave.status = 'Approved'
        flash('Leave application approved.', 'success')
    elif action == 'reject':
        leave.status = 'Rejected'
        flash('Leave application rejected.', 'danger')

    db.session.commit()
    return redirect(url_for('faculty.manage_leaves'))