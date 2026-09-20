import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

def calculate_attendance_insights(total_classes, attended_classes, target_pct=75.0):
    if total_classes == 0:
        return {
            'pct': 100.0,
            'status': 'success',
            'message': 'No classes recorded yet.',
            'classes_needed': 0
        }

    current_pct = round((attended_classes / total_classes) * 100, 1)

    if current_pct >= target_pct:
        # Calculate how many classes student can safely skip
        # (attended) / (total + skip) >= 0.75
        max_total = int(attended_classes / (target_pct / 100))
        bunkable = max_total - total_classes
        return {
            'pct': current_pct,
            'status': 'success',
            'message': f'Safe! You can miss up to {bunkable} upcoming class(es) and remain above {int(target_pct)}%.',
            'classes_needed': 0
        }
    else:
        # Calculate how many consecutive classes student MUST attend
        # (attended + x) / (total + x) >= 0.75
        # x = (0.75 * total - attended) / (1 - 0.75)
        needed = int(((target_pct / 100 * total_classes) - attended_classes) / (1 - (target_pct / 100))) + 1
        return {
            'pct': current_pct,
            'status': 'danger',
            'message': f'Warning! You must attend the next {needed} consecutive class(es) to reach {int(target_pct)}%.',
            'classes_needed': needed
        }

def generate_hall_ticket_pdf(student_profile, attendance_pct):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Title
    p.setFont("Helvetica-Bold", 20)
    p.setFillColor(colors.HexColor("#0d6efd"))
    p.drawString(180, 750, "CAMPUSCONNECT ADMIT CARD")
    
    p.setStrokeColor(colors.gray)
    p.line(50, 735, 560, 735)

    # Details
    p.setFont("Helvetica", 12)
    p.setFillColor(colors.black)
    p.drawString(50, 690, f"Student Name: {student_profile.first_name} {student_profile.last_name}")
    p.drawString(50, 665, f"Roll Number:  {student_profile.roll_number}")
    p.drawString(50, 640, f"Semester:     Semester {student_profile.semester}")
    p.drawString(50, 615, f"Attendance Status: {attendance_pct}% (Eligible)")

    # Box for signature
    p.rect(380, 580, 170, 70)
    p.setFont("Helvetica-Oblique", 9)
    p.drawString(400, 590, "Authorized Controller Seal")

    # Exam Notice
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, 550, "Instructions for Candidate:")
    p.setFont("Helvetica", 9)
    p.drawString(50, 535, "1. Please carry this admit card along with your Institute ID card.")
    p.drawString(50, 520, "2. Electronic devices are strictly prohibited inside the examination hall.")

    p.showPage()
    p.save()
    
    buffer.seek(0)
    return buffer