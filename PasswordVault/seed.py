from datetime import date, timedelta
from app import create_app
from app.extensions import db
from app.models.user import User, StudentProfile, FacultyProfile
from app.models.academic import Department, Course, Subject, Enrollment
from app.models.modules import Attendance, Notice

app = create_app()

def seed_database():
    with app.app_context():
        db.drop_all()
        db.create_all()

        print("Seeding departments and courses...")
        cs_dept = Department(name="Computer Science & Engineering", code="CSE")
        ee_dept = Department(name="Electrical Engineering", code="EE")
        db.session.add_all([cs_dept, ee_dept])
        db.session.commit()

        btech_cs = Course(name="B.Tech Computer Science", code="CS101", department_id=cs_dept.id)
        btech_ee = Course(name="B.Tech Electrical Engg", code="EE101", department_id=ee_dept.id)
        db.session.add_all([btech_cs, btech_ee])
        db.session.commit()

        print("Creating Admins...")
        admin1 = User(username="admin", email="admin@campusconnect.edu", role="admin")
        admin1.set_password("admin123")
        
        admin2 = User(username="superadmin", email="superadmin@campusconnect.edu", role="admin")
        admin2.set_password("admin123")
        db.session.add_all([admin1, admin2])

        print("Creating Faculty...")
        # Faculty 1 - CSE
        fac1_user = User(username="faculty1", email="john.doe@campusconnect.edu", role="faculty")
        fac1_user.set_password("faculty123")
        db.session.add(fac1_user)
        db.session.flush()

        fac1_prof = FacultyProfile(
            user_id=fac1_user.id,
            employee_id="FAC001",
            first_name="John",
            last_name="Doe",
            department_id=cs_dept.id
        )
        db.session.add(fac1_prof)
        db.session.flush()

        # Faculty 2 - EE
        fac2_user = User(username="faculty2", email="sarah.connor@campusconnect.edu", role="faculty")
        fac2_user.set_password("faculty123")
        db.session.add(fac2_user)
        db.session.flush()

        fac2_prof = FacultyProfile(
            user_id=fac2_user.id,
            employee_id="FAC002",
            first_name="Sarah",
            last_name="Connor",
            department_id=ee_dept.id
        )
        db.session.add(fac2_prof)
        db.session.flush()

        print("Creating Subjects...")
        sub_python = Subject(name="Python Programming", code="CS201", semester=1, course_id=btech_cs.id, faculty_id=fac1_prof.id)
        sub_circuits = Subject(name="Circuit Theory", code="EE201", semester=1, course_id=btech_ee.id, faculty_id=fac2_prof.id)
        db.session.add_all([sub_python, sub_circuits])
        db.session.commit()

        print("Creating Multiple Students...")
        students_data = [
            ("student1", "Jane", "Smith", "STU2024001", btech_cs.id, cs_dept.id),
            ("student2", "Alex", "Mercer", "STU2024002", btech_cs.id, cs_dept.id),
            ("student3", "Emily", "Watson", "STU2024003", btech_cs.id, cs_dept.id),
            ("student4", "Michael", "Brown", "STU2024004", btech_ee.id, ee_dept.id),
        ]

        for username, fname, lname, roll, course_id, dept_id in students_data:
            s_user = User(username=username, email=f"{username}@campusconnect.edu", role="student")
            s_user.set_password("student123")
            db.session.add(s_user)
            db.session.flush()

            s_prof = StudentProfile(
                user_id=s_user.id,
                roll_number=roll,
                first_name=fname,
                last_name=lname,
                department_id=dept_id,
                course_id=course_id,
                semester=1
            )
            db.session.add(s_prof)
            db.session.flush()

            # Assign CS students to Python, EE students to Circuits
            sub_id = sub_python.id if dept_id == cs_dept.id else sub_circuits.id
            enrollment = Enrollment(student_id=s_prof.id, subject_id=sub_id)
            db.session.add(enrollment)

            # Add attendance logs
            for i in range(10):
                is_p = True if i < 7 else False # 70% attendance
                att = Attendance(student_id=s_prof.id, subject_id=sub_id, date=date.today() - timedelta(days=i), is_present=is_p)
                db.session.add(att)

        sample_notice = Notice(
            title="Mid-Term Examination Schedule",
            description="Mid-term exams for Semester 1 start next month.",
            category="Academic",
            author_id=admin1.id
        )
        db.session.add(sample_notice)

        db.session.commit()
        print("--------------------------------------------------")
        print("Database successfully seeded with multiple users!")
        print("--------------------------------------------------")

if __name__ == '__main__':
    seed_database()