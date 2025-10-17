# ============================================================================
# exam_portal/management/commands/seed_data.py
# Django Management Command to Seed Database with Realistic Kenyan Data
# ============================================================================

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from exam_portal.models import (
    UserProfile, Student, ExamOfficer, Lecturer, UnitAssignment,
    ExamApplication, OCRResult, ApplicationReview, ExamMarking, Notification
)
from django.core.files.base import ContentFile
import random
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Seeds the database with realistic Kenyan university data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting data seeding...'))
        
        # Clear existing data (optional - comment out if you want to keep existing data)
        self.stdout.write('Clearing existing data...')
        ExamMarking.objects.all().delete()
        ApplicationReview.objects.all().delete()
        OCRResult.objects.all().delete()
        ExamApplication.objects.all().delete()
        Notification.objects.all().delete()
        UnitAssignment.objects.all().delete()
        Student.objects.all().delete()
        ExamOfficer.objects.all().delete()
        Lecturer.objects.all().delete()
        UserProfile.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        
        # Seed data
        self.create_students()
        self.create_exam_officers()
        self.create_lecturers()
        self.create_unit_assignments()
        self.create_exam_applications()
        
        self.stdout.write(self.style.SUCCESS('✅ Database seeding completed successfully!'))

    def create_students(self):
        """Create student accounts with realistic Kenyan data"""
        self.stdout.write('Creating students...')
        
        kenyan_first_names = [
            'Wanjiru', 'Kamau', 'Otieno', 'Achieng', 'Kipchoge', 'Wambui',
            'Mwangi', 'Nyambura', 'Omondi', 'Akinyi', 'Kariuki', 'Njeri',
            'Mutua', 'Wanjiku', 'Kimani', 'Wairimu', 'Ouma', 'Adhiambo',
            'Kibet', 'Chebet', 'Maina', 'Mumbi', 'Onyango', 'Awino',
            'Kiplagat', 'Jeptoo', 'Njoroge', 'Wangari', 'Owino', 'Atieno'
        ]
        
        kenyan_last_names = [
            'Mwangi', 'Kamau', 'Otieno', 'Omondi', 'Kipchoge', 'Wanjiru',
            'Kimani', 'Kariuki', 'Mutua', 'Ouma', 'Kibet', 'Njoroge',
            'Maina', 'Onyango', 'Kiplagat', 'Owino', 'Wambua', 'Njeri',
            'Chebet', 'Achieng', 'Wangari', 'Akinyi', 'Nyambura', 'Adhiambo'
        ]
        
        schools = ['SOB', 'SOE', 'SOS', 'SOH', 'SOCS', 'SOL', 'SOM']
        programs_by_school = {
            'SOCS': ['BSC_CS', 'BSC_IT'],
            'SOB': ['BBA', 'BA_ECON'],
            'SOE': ['BENG_CE', 'BENG_EE'],
            'SOS': ['BSC_MATH', 'BSC_PHYS'],
            'SOH': ['BA_ECON'],
            'SOL': ['LLB'],
            'SOM': ['MBCHB']
        }
        
        kenyan_phone_prefixes = ['0710', '0720', '0730', '0740', '0750', '0768', '0769', '0798', '0799']
        
        for i in range(50):
            first_name = random.choice(kenyan_first_names)
            last_name = random.choice(kenyan_last_names)
            username = f"student{i+1}"
            
            # Create User
            user = User.objects.create_user(
                username=username,
                email=f"{first_name.lower()}.{last_name.lower()}{i+1}@student.mu.ac.ke",
                password='student123',
                first_name=first_name,
                last_name=last_name
            )
            
            # Create UserProfile
            UserProfile.objects.create(
                user=user,
                user_type='student',
                phone_number=f"{random.choice(kenyan_phone_prefixes)}{random.randint(100000, 999999)}"
            )
            
            # Generate registration number (Kenyan university format)
            year = random.randint(2020, 2024)
            school = random.choice(schools)
            program = random.choice(programs_by_school.get(school, ['BSC_CS']))
            reg_number = f"{school}/{year}/{random.randint(1000, 9999)}"
            
            # Create Student
            Student.objects.create(
                user=user,
                registration_number=reg_number,
                first_name=first_name,
                last_name=last_name,
                email=f"{first_name.lower()}.{last_name.lower()}{i+1}@student.mu.ac.ke",
                phone_number=f"{random.choice(kenyan_phone_prefixes)}{random.randint(100000, 999999)}",
                school=school,
                program=program
            )
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Created 50 students'))

    def create_exam_officers(self):
        """Create exam officer accounts"""
        self.stdout.write('Creating exam officers...')
        
        officers_data = [
            ('Dr.', 'Peter', 'Kimani', 'SOCS'),
            ('Mrs.', 'Grace', 'Wanjiru', 'SOB'),
            ('Mr.', 'James', 'Otieno', 'SOE'),
            ('Dr.', 'Mary', 'Mwangi', 'SOS'),
            ('Mrs.', 'Ruth', 'Achieng', 'SOH'),
            ('Mr.', 'John', 'Kariuki', 'SOL'),
            ('Dr.', 'Elizabeth', 'Njeri', 'SOM'),
            ('Mr.', 'David', 'Omondi', 'GENERAL'),
        ]
        
        for i, (title, first_name, last_name, dept) in enumerate(officers_data):
            username = f"officer{i+1}"
            
            user = User.objects.create_user(
                username=username,
                email=f"{first_name.lower()}.{last_name.lower()}@mu.ac.ke",
                password='officer123',
                first_name=f"{title} {first_name}",
                last_name=last_name
            )
            
            UserProfile.objects.create(
                user=user,
                user_type='officer',
                phone_number=f"0{random.choice([710, 720, 730])}{random.randint(100000, 999999)}"
            )
            
            ExamOfficer.objects.create(
                user=user,
                officer_id=f"EO{2024}{str(i+1).zfill(3)}",
                first_name=f"{title} {first_name}",
                last_name=last_name,
                email=f"{first_name.lower()}.{last_name.lower()}@mu.ac.ke",
                phone_number=f"0{random.choice([710, 720, 730])}{random.randint(100000, 999999)}",
                department=dept
            )
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {len(officers_data)} exam officers'))

    def create_lecturers(self):
        """Create lecturer accounts"""
        self.stdout.write('Creating lecturers...')
        
        lecturers_data = [
            ('Dr.', 'Joseph', 'Mwangi', 'SOCS'),
            ('Prof.', 'Anne', 'Wanjiru', 'SOCS'),
            ('Dr.', 'Michael', 'Otieno', 'SOCS'),
            ('Mr.', 'Patrick', 'Kamau', 'SOCS'),
            ('Dr.', 'Susan', 'Achieng', 'SOB'),
            ('Prof.', 'Robert', 'Kariuki', 'SOB'),
            ('Dr.', 'Jane', 'Nyambura', 'SOB'),
            ('Eng.', 'Samuel', 'Kipchoge', 'SOE'),
            ('Dr.', 'Lucy', 'Wambui', 'SOE'),
            ('Prof.', 'Daniel', 'Ouma', 'SOE'),
            ('Dr.', 'Sarah', 'Njeri', 'SOS'),
            ('Prof.', 'Martin', 'Mutua', 'SOS'),
            ('Dr.', 'Catherine', 'Akinyi', 'SOH'),
            ('Prof.', 'George', 'Maina', 'SOH'),
            ('Dr.', 'Esther', 'Chebet', 'SOL'),
            ('Prof.', 'William', 'Onyango', 'SOM'),
        ]
        
        for i, (title, first_name, last_name, dept) in enumerate(lecturers_data):
            username = f"lecturer{i+1}"
            
            user = User.objects.create_user(
                username=username,
                email=f"{first_name.lower()}.{last_name.lower()}@mu.ac.ke",
                password='lecturer123',
                first_name=f"{title} {first_name}",
                last_name=last_name
            )
            
            UserProfile.objects.create(
                user=user,
                user_type='lecturer',
                phone_number=f"0{random.choice([710, 720, 730])}{random.randint(100000, 999999)}"
            )
            
            Lecturer.objects.create(
                user=user,
                lecturer_id=f"LEC{2024}{str(i+1).zfill(3)}",
                first_name=f"{title} {first_name}",
                last_name=last_name,
                email=f"{first_name.lower()}.{last_name.lower()}@mu.ac.ke",
                phone_number=f"0{random.choice([710, 720, 730])}{random.randint(100000, 999999)}",
                department=dept
            )
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {len(lecturers_data)} lecturers'))

    def create_unit_assignments(self):
        """Create unit assignments for lecturers"""
        self.stdout.write('Creating unit assignments...')
        
        units_by_department = {
            'SOCS': [
                ('CSC101', 'Introduction to Programming', 'BSC_CS'),
                ('CSC201', 'Data Structures and Algorithms', 'BSC_CS'),
                ('CSC301', 'Database Systems', 'BSC_CS'),
                ('CSC401', 'Software Engineering', 'BSC_CS'),
                ('IT102', 'Web Development', 'BSC_IT'),
                ('IT202', 'Network Administration', 'BSC_IT'),
                ('IT302', 'Cyber Security', 'BSC_IT'),
            ],
            'SOB': [
                ('BUS101', 'Principles of Management', 'BBA'),
                ('BUS201', 'Financial Accounting', 'BBA'),
                ('BUS301', 'Marketing Management', 'BBA'),
                ('ECO101', 'Microeconomics', 'BA_ECON'),
                ('ECO201', 'Macroeconomics', 'BA_ECON'),
            ],
            'SOE': [
                ('ENG101', 'Engineering Mathematics I', 'BENG_CE'),
                ('ENG201', 'Mechanics of Materials', 'BENG_CE'),
                ('EE101', 'Circuit Analysis', 'BENG_EE'),
                ('EE201', 'Electromagnetic Fields', 'BENG_EE'),
            ],
            'SOS': [
                ('MAT101', 'Calculus I', 'BSC_MATH'),
                ('MAT201', 'Linear Algebra', 'BSC_MATH'),
                ('PHY101', 'General Physics I', 'BSC_PHYS'),
                ('PHY201', 'Quantum Mechanics', 'BSC_PHYS'),
            ],
            'SOH': [
                ('HIS101', 'World History', 'BA_ECON'),
                ('LIT101', 'English Literature', 'BA_ECON'),
            ],
            'SOL': [
                ('LAW101', 'Constitutional Law', 'LLB'),
                ('LAW201', 'Criminal Law', 'LLB'),
            ],
            'SOM': [
                ('MED101', 'Anatomy', 'MBCHB'),
                ('MED201', 'Physiology', 'MBCHB'),
            ],
        }
        
        lecturers = Lecturer.objects.all()
        count = 0
        
        for lecturer in lecturers:
            units = units_by_department.get(lecturer.department, [])
            # Assign 2-4 random units to each lecturer
            assigned_units = random.sample(units, min(random.randint(2, 4), len(units))) if units else []
            
            for unit_code, unit_name, program in assigned_units:
                UnitAssignment.objects.create(
                    lecturer=lecturer,
                    unit_code=unit_code,
                    unit_name=unit_name,
                    program=program,
                    year=random.randint(2023, 2024),
                    semester=random.choice(['1', '2']),
                    active=True
                )
                count += 1
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {count} unit assignments'))

    def create_exam_applications(self):
        """Create exam applications with reviews and markings"""
        self.stdout.write('Creating exam applications...')
        
        students = list(Student.objects.all())
        lecturers = list(Lecturer.objects.all())
        officers = list(ExamOfficer.objects.all())
        unit_assignments = list(UnitAssignment.objects.all())
        
        statuses = [
            'submitted', 'under_review', 'approved', 'rejected',
            'exam_received', 'marking_complete', 'submitted_to_officer', 'uploaded_to_portal'
        ]
        
        exam_types = ['resit', 'retake', 'special']
        
        # Create 80-100 applications
        for i in range(random.randint(80, 100)):
            student = random.choice(students)
            status = random.choice(statuses)
            exam_type = random.choice(exam_types)
            
            # Pick a random unit assignment
            unit_assignment = random.choice(unit_assignments)
            
            # Create application
            application = ExamApplication.objects.create(
                student=student,
                year_of_study=random.choice(['1', '2', '3', '4']),
                exam_type=exam_type,
                unit_name=unit_assignment.unit_name,
                unit_code=unit_assignment.unit_code,
                year_taken=random.randint(2022, 2024),
                semester_taken=random.choice(['1', '2']),
                supporting_document='documents/sample_document.pdf',
                declaration_accepted=True,
                status=status,
                auto_verified=random.choice([True, False]),
                assigned_lecturer=unit_assignment.lecturer if status in ['approved', 'exam_received', 'marking_complete', 'submitted_to_officer', 'uploaded_to_portal'] else None,
            )
            
            # Create OCR Result
            confidence = random.uniform(0.7, 0.99)
            OCRResult.objects.create(
                application=application,
                extracted_text=f"Student Name: {student.first_name} {student.last_name}\nReg No: {student.registration_number}\nUnit: {unit_assignment.unit_code}\nReason: {exam_type.capitalize()} examination required due to medical reasons.",
                ocr_summary=f"Document verified for {exam_type} exam application",
                confidence_score=confidence,
                keywords_found=['student', 'exam', exam_type, unit_assignment.unit_code],
                verified=confidence > 0.85
            )
            
            # Create Application Review for reviewed applications
            if status in ['approved', 'rejected', 'exam_received', 'marking_complete', 'submitted_to_officer', 'uploaded_to_portal']:
                officer = random.choice(officers)
                ApplicationReview.objects.create(
                    application=application,
                    reviewed_by=officer,
                    decision='approved' if status != 'rejected' else 'rejected',
                    comments=random.choice([
                        'Documents verified and approved',
                        'Application meets all requirements',
                        'Valid reason provided with supporting documents',
                        'Approved for examination',
                        'Rejected - insufficient documentation' if status == 'rejected' else 'All criteria met'
                    ])
                )
            
            # Create Exam Marking for marked applications
            if status in ['marking_complete', 'submitted_to_officer', 'uploaded_to_portal'] and application.assigned_lecturer:
                marks = random.uniform(40.0, 85.0)
                ExamMarking.objects.create(
                    application=application,
                    lecturer=application.assigned_lecturer,
                    marks=round(marks, 2),
                    comments=random.choice([
                        'Good performance',
                        'Satisfactory work',
                        'Excellent understanding of concepts',
                        'Needs improvement in certain areas',
                        'Well done'
                    ])
                )
            
            # Create notifications
            notification_messages = {
                'submitted': 'Your exam application has been submitted successfully',
                'under_review': 'Your application is currently under review by the exam officer',
                'approved': 'Congratulations! Your application has been approved',
                'rejected': 'Your application has been rejected. Please contact the exam office',
                'exam_received': 'Your exam script has been received by the lecturer',
                'marking_complete': 'Marking has been completed for your exam',
                'submitted_to_officer': 'Your marks have been submitted to the exam officer',
                'uploaded_to_portal': 'Your results have been uploaded to the student portal'
            }
            
            Notification.objects.create(
                student=student,
                application=application,
                notification_type='status_update',
                title=f'Application {application.application_id} - Status Update',
                message=notification_messages.get(status, 'Your application status has been updated'),
                is_read=random.choice([True, False])
            )
        
        app_count = ExamApplication.objects.count()
        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {app_count} exam applications with reviews and markings'))