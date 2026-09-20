from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file
from flask_login import login_required, current_user
from app.extensions import db
from app.models.academic import Enrollment
from app.models.modules import Attendance, Notice, LeaveApplication
from app.student.utils import calculate_attendance_insights, generate_hall_ticket_pdf

student_bp = Blueprint('student', __name__)


@student_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'student':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.index'))

    profile = current_user.student_profile
    if not profile:
        flash('Student profile not found.', 'danger')
        return redirect(url_for('main.index'))

    enrollments = Enrollment.query.filter_by(student_id=profile.id).all()

    # Calculate Attendance and Smart Insights
    total_classes = Attendance.query.filter_by(student_id=profile.id).count()
    attended_classes = Attendance.query.filter_by(student_id=profile.id, is_present=True).count()

    attendance_data = calculate_attendance_insights(total_classes, attended_classes)
    notices = Notice.query.order_by(Notice.created_at.desc()).limit(5).all()

    return render_template(
        'student/dashboard.html',
        profile=profile,
        enrollments=enrollments,
        attendance=attendance_data,
        notices=notices
    )


@student_bp.route('/download-hall-ticket')
@login_required
def download_hall_ticket():
    if current_user.role != 'student':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.index'))

    profile = current_user.student_profile
    total_classes = Attendance.query.filter_by(student_id=profile.id).count()
    attended_classes = Attendance.query.filter_by(student_id=profile.id, is_present=True).count()

    pct = round((attended_classes / total_classes * 100), 1) if total_classes > 0 else 100.0

    if pct < 75.0:
        flash('Hall ticket blocked due to low attendance (<75%).', 'danger')
        return redirect(url_for('student.dashboard'))

    pdf_buffer = generate_hall_ticket_pdf(profile, pct)
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"Hall_Ticket_{profile.roll_number}.pdf",
        mimetype='application/pdf'
    )


@student_bp.route('/leaves', methods=['GET', 'POST'])
@login_required
def leave_requests():
    if current_user.role != 'student':
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.index'))

    profile = current_user.student_profile

    if request.method == 'POST':
        reason = request.form.get('reason')
        start_date_str = request.form.get('start_date')
        end_date_str = request.form.get('end_date')

        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

        new_leave = LeaveApplication(
            student_id=profile.id,
            reason=reason,
            start_date=start_date,
            end_date=end_date
        )
        db.session.add(new_leave)
        db.session.commit()

        flash('Leave application submitted successfully!', 'success')
        return redirect(url_for('student.leave_requests'))

    applications = LeaveApplication.query.filter_by(student_id=profile.id).order_by(LeaveApplication.applied_on.desc()).all()
    return render_template('student/leaves.html', applications=applications)