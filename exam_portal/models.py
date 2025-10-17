# ============================================================================
# accounts/models.py - User Profile Models
# ============================================================================

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    """Base profile for all users"""
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('officer', 'Exam Officer'),
        ('lecturer', 'Lecturer'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.user_type}"
    
    class Meta:
        db_table = 'user_profiles'


# ============================================================================
# models.py - All Models in Single Application
# ============================================================================

class Student(models.Model):
    """Student profile with academic information"""
    SCHOOL_CHOICES = (
        ('SOB', 'School of Business'),
        ('SOE', 'School of Engineering'),
        ('SOS', 'School of Science'),
        ('SOH', 'School of Humanities'),
        ('SOCS', 'School of Computer Science'),
        ('SOL', 'School of Law'),
        ('SOM', 'School of Medicine'),
    )
    
    PROGRAM_CHOICES = (
        ('BSC_CS', 'BSc Computer Science'),
        ('BSC_IT', 'BSc Information Technology'),
        ('BBA', 'Bachelor of Business Administration'),
        ('BENG_CE', 'BEng Civil Engineering'),
        ('BENG_EE', 'BEng Electrical Engineering'),
        ('BSC_MATH', 'BSc Mathematics'),
        ('BSC_PHYS', 'BSc Physics'),
        ('BA_ECON', 'BA Economics'),
        ('LLB', 'Bachelor of Laws'),
        ('MBCHB', 'Bachelor of Medicine'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    registration_number = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    school = models.CharField(max_length=10, choices=SCHOOL_CHOICES, blank=True, null=True)
    program = models.CharField(max_length=20, choices=PROGRAM_CHOICES, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.registration_number} - {self.first_name} {self.last_name}"
    
    class Meta:
        db_table = 'students'
        ordering = ['-created_at']


class ExamOfficer(models.Model):
    """Exam officer profile"""
    DEPARTMENT_CHOICES = (
        ('SOB', 'School of Business'),
        ('SOE', 'School of Engineering'),
        ('SOS', 'School of Science'),
        ('SOH', 'School of Humanities'),
        ('SOCS', 'School of Computer Science'),
        ('SOL', 'School of Law'),
        ('SOM', 'School of Medicine'),
        ('GENERAL', 'General Office'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='officer_profile')
    officer_id = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    department = models.CharField(max_length=10, choices=DEPARTMENT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.officer_id} - {self.first_name} {self.last_name}"
    
    class Meta:
        db_table = 'exam_officers'


class Lecturer(models.Model):
    """Lecturer profile"""
    DEPARTMENT_CHOICES = (
        ('SOB', 'School of Business'),
        ('SOE', 'School of Engineering'),
        ('SOS', 'School of Science'),
        ('SOH', 'School of Humanities'),
        ('SOCS', 'School of Computer Science'),
        ('SOL', 'School of Law'),
        ('SOM', 'School of Medicine'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='lecturer_profile')
    lecturer_id = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    department = models.CharField(max_length=10, choices=DEPARTMENT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.lecturer_id} - {self.first_name} {self.last_name}"
    
    class Meta:
        db_table = 'lecturers'


class UnitAssignment(models.Model):
    """Units assigned to lecturers"""
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE, related_name='unit_assignments')
    unit_code = models.CharField(max_length=50)
    unit_name = models.CharField(max_length=200)
    program = models.CharField(max_length=20)
    year = models.IntegerField()
    semester = models.CharField(max_length=1)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.lecturer.lecturer_id} - {self.unit_code}"
    
    class Meta:
        db_table = 'unit_assignments'
        unique_together = ['lecturer', 'unit_code', 'year', 'semester']


class ExamApplication(models.Model):
    """Student exam applications"""
    EXAM_TYPE_CHOICES = (
        ('resit', 'Resit'),
        ('retake', 'Retake'),
        ('special', 'Special'),
    )
    
    STATUS_CHOICES = (
        ('submitted', 'Submitted - Pending Officer Review'),
        ('under_review', 'Under Review by Officer'),
        ('approved', 'Approved - Forwarded to Lecturer'),
        ('rejected', 'Rejected by Officer'),
        ('exam_received', 'Exam Script Received by Lecturer'),
        ('marking_complete', 'Marking Complete'),
        ('submitted_to_officer', 'Submitted to Exam Officer'),
        ('uploaded_to_portal', 'Uploaded to Portal'),
    )
    
    YEAR_OF_STUDY_CHOICES = (
        ('1', 'Year 1'),
        ('2', 'Year 2'),
        ('3', 'Year 3'),
        ('4', 'Year 4'),
        ('5', 'Year 5'),
    )
    
    SEMESTER_CHOICES = (
        ('1', 'Semester 1'),
        ('2', 'Semester 2'),
    )
    
    application_id = models.CharField(max_length=20, unique=True, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='applications')
    
    # Academic details
    year_of_study = models.CharField(max_length=1, choices=YEAR_OF_STUDY_CHOICES)
    exam_type = models.CharField(max_length=10, choices=EXAM_TYPE_CHOICES)
    unit_name = models.CharField(max_length=200)
    unit_code = models.CharField(max_length=50)
    year_taken = models.IntegerField()
    semester_taken = models.CharField(max_length=1, choices=SEMESTER_CHOICES)
    
    # Document and verification
    supporting_document = models.FileField(upload_to='documents/%Y/%m/%d/')
    declaration_accepted = models.BooleanField(default=False)
    
    # Status tracking
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='submitted')
    auto_verified = models.BooleanField(default=False)
    
    # Assignment
    assigned_lecturer = models.ForeignKey(Lecturer, on_delete=models.SET_NULL, 
                                         null=True, blank=True, related_name='assigned_applications')
    
    # Timestamps
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.application_id:
            # Generate unique application ID
            import random
            import string
            from datetime import datetime
            year = datetime.now().year
            random_str = ''.join(random.choices(string.digits, k=4))
            self.application_id = f"APP{year}{random_str}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.application_id} - {self.student.registration_number} - {self.unit_code}"
    
    class Meta:
        db_table = 'exam_applications'
        ordering = ['-submitted_at']


class OCRResult(models.Model):
    """OCR verification results for uploaded documents"""
    application = models.OneToOneField(ExamApplication, on_delete=models.CASCADE, 
                                      related_name='ocr_result')
    extracted_text = models.TextField()
    ocr_summary = models.TextField()
    confidence_score = models.FloatField(default=0.0)
    keywords_found = models.JSONField(default=list, blank=True)
    verified = models.BooleanField(default=False)
    processed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"OCR - {self.application.application_id}"
    
    class Meta:
        db_table = 'ocr_results'


class ApplicationReview(models.Model):
    """Track officer reviews of applications"""
    DECISION_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    application = models.ForeignKey(ExamApplication, on_delete=models.CASCADE, 
                                   related_name='reviews')
    reviewed_by = models.ForeignKey(ExamOfficer, on_delete=models.CASCADE, 
                                   related_name='reviews')
    decision = models.CharField(max_length=10, choices=DECISION_CHOICES, default='pending')
    comments = models.TextField(blank=True, null=True)
    reviewed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.application.application_id} - {self.decision}"
    
    class Meta:
        db_table = 'application_reviews'
        ordering = ['-reviewed_at']


class ExamMarking(models.Model):
    """Lecturer marking records for exam applications"""
    application = models.OneToOneField(ExamApplication, on_delete=models.CASCADE, 
                                      related_name='marking')
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE, related_name='markings')
    marks = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    comments = models.TextField(blank=True, null=True)
    marked_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.application.application_id} - {self.marks}"
    
    class Meta:
        db_table = 'exam_markings'


class Notification(models.Model):
    """Notifications for students"""
    NOTIFICATION_TYPE_CHOICES = (
        ('status_update', 'Status Update'),
        ('officer_message', 'Message from Officer'),
        ('lecturer_message', 'Message from Lecturer'),
        ('general', 'General'),
    )
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='notifications')
    application = models.ForeignKey(ExamApplication, on_delete=models.CASCADE, 
                                   related_name='notifications', null=True, blank=True)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.registration_number} - {self.title}"
    
    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']


# ============================================================================
# SIGNALS - Auto-create profiles and notifications
# ============================================================================

@receiver(post_save, sender=Student)
def create_student_notifications(sender, instance, created, **kwargs):
    """Create welcome notification for new students"""
    if created:
        Notification.objects.create(
            student=instance,
            notification_type='general',
            title='Welcome to Exam Tracking System',
            message=f'Welcome {instance.first_name}! Your account has been created successfully.'
        )