# ============================================================================
# views.py - All Views for Exam Tracking System
# ============================================================================

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import datetime, timedelta
import json

from .models import *
from .forms import *


# ============================================================================
# AUTHENTICATION VIEWS
# ============================================================================

def login_view(request):
    """Login view that redirects to appropriate dashboard"""
    if request.user.is_authenticated:
        return redirect('dashboard_redirect')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard_redirect')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'accounts/login.html')


@login_required
def dashboard_redirect(request):
    """Redirect users to their specific dashboard based on user type"""
    user = request.user
    
    # Check if user is superuser/admin
    if user.is_superuser or user.is_staff:
        return redirect('admin_dashboard')
    
    # Check user profile type
    try:
        profile = user.profile
        if profile.user_type == 'student':
            return redirect('student_dashboard')
        elif profile.user_type == 'officer':
            return redirect('officer_dashboard')
        elif profile.user_type == 'lecturer':
            return redirect('lecturer_dashboard')
    except:
        pass
    
    messages.error(request, 'User profile not found. Please contact administrator.')
    return redirect('login')


def logout_view(request):
    """Logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


# ============================================================================
# ADMIN DASHBOARD & VIEWS
# ============================================================================

@login_required
def admin_dashboard(request):
    """Admin dashboard with system overview"""
    if not (request.user.is_superuser or request.user.is_staff):
        messages.error(request, 'Access denied.')
        return redirect('dashboard_redirect')
    
    # Statistics
    total_students = Student.objects.count()
    total_officers = ExamOfficer.objects.count()
    total_lecturers = Lecturer.objects.count()
    total_applications = ExamApplication.objects.count()
    
    # Recent applications
    recent_applications = ExamApplication.objects.select_related('student').order_by('-submitted_at')[:10]
    
    # Applications by status
    status_stats = ExamApplication.objects.values('status').annotate(count=Count('id'))
    
    # Applications by exam type
    exam_type_stats = ExamApplication.objects.values('exam_type').annotate(count=Count('id'))
    
    # Monthly application trends (last 6 months)
    six_months_ago = timezone.now() - timedelta(days=180)
    monthly_apps = ExamApplication.objects.filter(
        submitted_at__gte=six_months_ago
    ).extra(
        select={'month': 'EXTRACT(month FROM submitted_at)'}
    ).values('month').annotate(count=Count('id')).order_by('month')
    
    context = {
        'total_students': total_students,
        'total_officers': total_officers,
        'total_lecturers': total_lecturers,
        'total_applications': total_applications,
        'recent_applications': recent_applications,
        'status_stats': status_stats,
        'exam_type_stats': exam_type_stats,
        'monthly_apps': monthly_apps,
    }
    
    return render(request, 'admin/dashboard.html', context)


@login_required
def admin_students_list(request):
    """Admin view to manage students"""
    if not (request.user.is_superuser or request.user.is_staff):
        messages.error(request, 'Access denied.')
        return redirect('dashboard_redirect')
    
    students = Student.objects.all().order_by('-created_at')
    
    # Search and filter
    search_query = request.GET.get('search', '')
    school_filter = request.GET.get('school', '')
    program_filter = request.GET.get('program', '')
    
    if search_query:
        students = students.filter(
            Q(registration_number__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    if school_filter:
        students = students.filter(school=school_filter)
    
    if program_filter:
        students = students.filter(program=program_filter)
    
    # Pagination
    paginator = Paginator(students, 20)
    page_number = request.GET.get('page')
    students_page = paginator.get_page(page_number)
    
    context = {
        'students': students_page,
        'search_query': search_query,
        'school_filter': school_filter,
        'program_filter': program_filter,
        'school_choices': Student.SCHOOL_CHOICES,
        'program_choices': Student.PROGRAM_CHOICES,
    }
    
    return render(request, 'admin/students_list.html', context)


@login_required
def admin_student_create(request):
    """Admin creates a new student"""
    if not (request.user.is_superuser or request.user.is_staff):
        messages.error(request, 'Access denied.')
        return redirect('dashboard_redirect')
    
    if request.method == 'POST':
        form = StudentCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student created successfully!')
            return redirect('admin_students_list')
    else:
        form = StudentCreationForm()
    
    return render(request, 'admin/student_form.html', {'form': form, 'action': 'Create'})


@login_required
def admin_student_edit(request, student_id):
    """Admin edits student details"""
    if not (request.user.is_superuser or request.user.is_staff):
        messages.error(request, 'Access denied.')
        return redirect('dashboard_redirect')
    
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        form = StudentEditForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully!')
            return redirect('admin_students_list')
    else:
        form = StudentEditForm(instance=student)
    
    return render(request, 'admin/student_form.html', {'form': form, 'action': 'Edit', 'student': student})


@login_required
def admin_student_delete(request, student_id):
    """Admin deletes a student"""
    if not (request.user.is_superuser or request.user.is_staff):
        messages.error(request, 'Access denied.')
        return redirect('dashboard_redirect')
    
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        student.user.delete()  # This will cascade delete the student
        messages.success(request, 'Student deleted successfully!')
        return redirect('admin_students_list')
    
    return render(request, 'admin/student_confirm_delete.html', {'student': student})


@login_required
def admin_officers_list(request):
    """Admin view to manage exam officers"""
    if not (request.user.is_superuser or request.user.is_staff):
        messages.error(request, 'Access denied.')
        return redirect('dashboard_redirect')
    
    officers = ExamOfficer.objects.all().order_by('-created_at')
    
    # Search and filter
    search_query = request.GET.get('search', '')
    dept_filter = request.GET.get('department', '')
    
    if search_query:
        officers = officers.filter(
            Q(officer_id__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    if dept_filter:
        officers = officers.filter(department=dept_filter)
    
    paginator = Paginator(officers, 20)
    page_number = request.GET.get('page')
    officers_page = paginator.get_page(page_number)
    
    context = {
        'officers': officers_page,
        'search_query': search_query,
        'dept_filter': dept_filter,
        'dept_choices': ExamOfficer.DEPARTMENT_CHOICES,
    }
    
    return render(request, 'admin/officers_list.html', context)


@login_required
def admin_officer_create(request):
    """Admin creates a new exam officer"""
    if not (request.user.is_superuser or request.user.is_staff):
        messages.error(request, 'Access denied.')
        return redirect('dashboard_redirect')
    
    if request.method == 'POST':
        form = OfficerCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Exam Officer created successfully!')
            return redirect('admin_officers_list')
    else:
        form = OfficerCreationForm()
    
    return render(request, 'admin/officer_form.html', {'form': form, 'action': 'Create'})


@login_required
def admin_lecturers_list(request):
    """Admin view to manage lecturers"""
    if not (request.user.is_superuser or request.user.is_staff):
        messages.error(request, 'Access denied.')
        return redirect('dashboard_redirect')
    
    lecturers = Lecturer.objects.all().order_by('-created_at')
    
    # Search and filter
    search_query = request.GET.get('search', '')
    dept_filter = request.GET.get('department', '')
    
    if search_query:
        lecturers = lecturers.filter(
            Q(lecturer_id__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    if dept_filter:
        lecturers = lecturers.filter(department=dept_filter)
    
    paginator = Paginator(lecturers, 20)
    page_number = request.GET.get('page')
    lecturers_page = paginator.get_page(page_number)
    
    context = {
        'lecturers': lecturers_page,
        'search_query': search_query,
        'dept_filter': dept_filter,
        'dept_choices': Lecturer.DEPARTMENT_CHOICES,
    }
    
    return render(request, 'admin/lecturers_list.html', context)


@login_required
def admin_lecturer_create(request):
    """Admin creates a new lecturer"""
    if not (request.user.is_superuser or request.user.is_staff):
        messages.error(request, 'Access denied.')
        return redirect('dashboard_redirect')
    
    if request.method == 'POST':
        form = LecturerCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lecturer created successfully!')
            return redirect('admin_lecturers_list')
    else:
        form = LecturerCreationForm()
    
    return render(request, 'admin/lecturer_form.html', {'form': form, 'action': 'Create'})


@login_required
def admin_applications_list(request):
    """Admin view to see all applications"""
    if not (request.user.is_superuser or request.user.is_staff):
        messages.error(request, 'Access denied.')
        return redirect('dashboard_redirect')
    
    applications = ExamApplication.objects.select_related('student', 'assigned_lecturer').order_by('-submitted_at')
    
    # Filters
    status_filter = request.GET.get('status', '')
    exam_type_filter = request.GET.get('exam_type', '')
    search_query = request.GET.get('search', '')
    
    if status_filter:
        applications = applications.filter(status=status_filter)
    
    if exam_type_filter:
        applications = applications.filter(exam_type=exam_type_filter)
    
    if search_query:
        applications = applications.filter(
            Q(application_id__icontains=search_query) |
            Q(student__registration_number__icontains=search_query) |
            Q(unit_code__icontains=search_query)
        )
    
    paginator = Paginator(applications, 25)
    page_number = request.GET.get('page')
    applications_page = paginator.get_page(page_number)
    
    context = {
        'applications': applications_page,
        'status_filter': status_filter,
        'exam_type_filter': exam_type_filter,
        'search_query': search_query,
        'status_choices': ExamApplication.STATUS_CHOICES,
        'exam_type_choices': ExamApplication.EXAM_TYPE_CHOICES,
    }
    
    return render(request, 'admin/applications_list.html', context)


@login_required
def admin_application_detail(request, app_id):
    """Admin views application details"""
    if not (request.user.is_superuser or request.user.is_staff):
        messages.error(request, 'Access denied.')
        return redirect('dashboard_redirect')
    
    application = get_object_or_404(
        ExamApplication.objects.select_related('student', 'assigned_lecturer'),
        application_id=app_id
    )
    
    try:
        ocr_result = application.ocr_result
    except:
        ocr_result = None
    
    reviews = application.reviews.all()
    
    try:
        marking = application.marking
    except:
        marking = None
    
    context = {
        'application': application,
        'ocr_result': ocr_result,
        'reviews': reviews,
        'marking': marking,
    }
    
    return render(request, 'admin/application_detail.html', context)


# ============================================================================
# STUDENT VIEWS
# ============================================================================

@login_required
def student_dashboard(request):
    """Student dashboard"""
    try:
        student = request.user.student_profile
    except:
        messages.error(request, 'Student profile not found.')
        return redirect('login')
    
    # Get applications
    applications = student.applications.all().order_by('-submitted_at')[:5]
    
    # Get unread notifications
    unread_notifications = student.notifications.filter(is_read=False).count()
    
    # Statistics
    total_applications = student.applications.count()
    approved_applications = student.applications.filter(status='approved').count()
    pending_applications = student.applications.filter(status__in=['submitted', 'under_review']).count()
    
    context = {
        'student': student,
        'applications': applications,
        'unread_notifications': unread_notifications,
        'total_applications': total_applications,
        'approved_applications': approved_applications,
        'pending_applications': pending_applications,
    }
    
    return render(request, 'student/dashboard.html', context)


@login_required
def student_apply_exam(request):
    """Student submits exam application"""
    try:
        student = request.user.student_profile
    except:
        messages.error(request, 'Student profile not found.')
        return redirect('login')
    
    if request.method == 'POST':
        form = ExamApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.student = student
            application.save()
            
            # Create notification
            Notification.objects.create(
                student=student,
                application=application,
                notification_type='status_update',
                title='Application Submitted',
                message=f'Your exam application {application.application_id} has been submitted successfully.'
            )
            
            messages.success(request, f'Application {application.application_id} submitted successfully!')
            return redirect('student_applications')
    else:
        form = ExamApplicationForm()
    
    return render(request, 'student/apply_exam.html', {'form': form})


@login_required
def student_applications(request):
    """Student views all their applications"""
    try:
        student = request.user.student_profile
    except:
        messages.error(request, 'Student profile not found.')
        return redirect('login')
    
    applications = student.applications.all().order_by('-submitted_at')
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        applications = applications.filter(status=status_filter)
    
    paginator = Paginator(applications, 10)
    page_number = request.GET.get('page')
    applications_page = paginator.get_page(page_number)
    
    context = {
        'applications': applications_page,
        'status_filter': status_filter,
        'status_choices': ExamApplication.STATUS_CHOICES,
    }
    
    return render(request, 'student/applications.html', context)


@login_required
def student_application_detail(request, app_id):
    """Student views application detail"""
    try:
        student = request.user.student_profile
    except:
        messages.error(request, 'Student profile not found.')
        return redirect('login')
    
    application = get_object_or_404(
        ExamApplication.objects.select_related('assigned_lecturer'),
        application_id=app_id,
        student=student
    )
    
    try:
        marking = application.marking
    except:
        marking = None
    
    context = {
        'application': application,
        'marking': marking,
    }
    
    return render(request, 'student/application_detail.html', context)


@login_required
def student_notifications(request):
    """Student views notifications"""
    try:
        student = request.user.student_profile
    except:
        messages.error(request, 'Student profile not found.')
        return redirect('login')
    
    notifications = student.notifications.all().order_by('-created_at')
    
    # Mark as read if requested
    mark_as_read = request.GET.get('mark_read')
    if mark_as_read:
        notifications.update(is_read=True)
    
    paginator = Paginator(notifications, 15)
    page_number = request.GET.get('page')
    notifications_page = paginator.get_page(page_number)
    
    context = {
        'notifications': notifications_page,
    }
    
    return render(request, 'student/notifications.html', context)


# ============================================================================
# EXAM OFFICER VIEWS
# ============================================================================

@login_required
def officer_dashboard(request):
    """Exam officer dashboard"""
    try:
        officer = request.user.officer_profile
    except:
        messages.error(request, 'Officer profile not found.')
        return redirect('login')
    
    # Get applications for review
    pending_applications = ExamApplication.objects.filter(
        status__in=['submitted', 'under_review']
    ).select_related('student').order_by('-submitted_at')[:10]
    
    # Statistics
    total_pending = ExamApplication.objects.filter(status='submitted').count()
    under_review = ExamApplication.objects.filter(status='under_review').count()
    approved_today = ExamApplication.objects.filter(
        status='approved',
        updated_at__date=timezone.now().date()
    ).count()
    
    context = {
        'officer': officer,
        'pending_applications': pending_applications,
        'total_pending': total_pending,
        'under_review': under_review,
        'approved_today': approved_today,
    }
    
    return render(request, 'officer/dashboard.html', context)


@login_required
def officer_review_applications(request):
    """Officer reviews applications"""
    try:
        officer = request.user.officer_profile
    except:
        messages.error(request, 'Officer profile not found.')
        return redirect('login')
    
    applications = ExamApplication.objects.filter(
        status__in=['submitted', 'under_review']
    ).select_related('student').order_by('-submitted_at')
    
    # Filters
    status_filter = request.GET.get('status', '')
    exam_type_filter = request.GET.get('exam_type', '')
    
    if status_filter:
        applications = applications.filter(status=status_filter)
    
    if exam_type_filter:
        applications = applications.filter(exam_type=exam_type_filter)
    
    paginator = Paginator(applications, 20)
    page_number = request.GET.get('page')
    applications_page = paginator.get_page(page_number)
    
    context = {
        'applications': applications_page,
        'status_filter': status_filter,
        'exam_type_filter': exam_type_filter,
    }
    
    return render(request, 'officer/review_applications.html', context)


@login_required
def officer_application_review(request, app_id):
    """Officer reviews a specific application"""
    try:
        officer = request.user.officer_profile
    except:
        messages.error(request, 'Officer profile not found.')
        return redirect('login')
    
    application = get_object_or_404(
        ExamApplication.objects.select_related('student'),
        application_id=app_id
    )
    
    if request.method == 'POST':
        form = ApplicationReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.application = application
            review.reviewed_by = officer
            review.save()
            
            # Update application status
            if review.decision == 'approved':
                application.status = 'approved'
                # Find and assign lecturer
                lecturers = Lecturer.objects.filter(
                    unit_assignments__unit_code=application.unit_code,
                    unit_assignments__active=True
                )
                if lecturers.exists():
                    application.assigned_lecturer = lecturers.first()
                
                # Create notification
                Notification.objects.create(
                    student=application.student,
                    application=application,
                    notification_type='status_update',
                    title='Application Approved',
                    message=f'Your application {application.application_id} has been approved.'
                )
            elif review.decision == 'rejected':
                application.status = 'rejected'
                # Create notification
                Notification.objects.create(
                    student=application.student,
                    application=application,
                    notification_type='officer_message',
                    title='Application Rejected',
                    message=f'Your application {application.application_id} has been rejected. Reason: {review.comments}'
                )
            
            application.save()
            messages.success(request, 'Review submitted successfully!')
            return redirect('officer_review_applications')
    else:
        form = ApplicationReviewForm()
    
    try:
        ocr_result = application.ocr_result
    except:
        ocr_result = None
    
    context = {
        'application': application,
        'form': form,
        'ocr_result': ocr_result,
    }
    
    return render(request, 'officer/application_review.html', context)


# ============================================================================
# LECTURER VIEWS
# ============================================================================

@login_required
def lecturer_dashboard(request):
    """Lecturer dashboard"""
    try:
        lecturer = request.user.lecturer_profile
    except:
        messages.error(request, 'Lecturer profile not found.')
        return redirect('login')
    
    # Get assigned applications
    assigned_applications = lecturer.assigned_applications.filter(
        status__in=['approved', 'exam_received']
    ).select_related('student').order_by('-updated_at')[:10]
    
    # Statistics
    total_assigned = lecturer.assigned_applications.count()
    pending_marking = lecturer.assigned_applications.filter(
        status__in=['approved', 'exam_received']
    ).count()
    completed_marking = lecturer.markings.count()
    
    # Unit assignments
    unit_assignments = lecturer.unit_assignments.filter(active=True)
    
    context = {
        'lecturer': lecturer,
        'assigned_applications': assigned_applications,
        'total_assigned': total_assigned,
        'pending_marking': pending_marking,
        'completed_marking': completed_marking,
        'unit_assignments': unit_assignments,
    }
    
    return render(request, 'lecturer/dashboard.html', context)


@login_required
def lecturer_assignments(request):
    """Lecturer views all assigned applications"""
    try:
        lecturer = request.user.lecturer_profile
    except:
        messages.error(request, 'Lecturer profile not found.')
        return redirect('login')
    
    applications = lecturer.assigned_applications.select_related('student').order_by('-updated_at')
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        applications = applications.filter(status=status_filter)
    
    paginator = Paginator(applications, 15)
    page_number = request.GET.get('page')
    applications_page = paginator.get_page(page_number)
    
    context = {
        'applications': applications_page,
        'status_filter': status_filter,
    }
    
    return render(request, 'lecturer/assignments.html', context)


@login_required
def lecturer_mark_exam(request, app_id):
    """Lecturer marks exam"""
    try:
        lecturer = request.user.lecturer_profile
    except:
        messages.error(request, 'Lecturer profile not found.')
        return redirect('login')
    
    application = get_object_or_404(
        ExamApplication.objects.select_related('student'),
        application_id=app_id,
        assigned_lecturer=lecturer
    )
    
    try:
        marking = application.marking
    except:
        marking = None
    
    if request.method == 'POST':
        form = ExamMarkingForm(request.POST, instance=marking)
        if form.is_valid():
            marking = form.save(commit=False)
            marking.application = application
            marking.lecturer = lecturer
            marking.save()
            
            # Update application status
            application.status = 'marking_complete'
            application.save()
            
            # Create notification
            Notification.objects.create(
                student=application.student,
                application=application,
                notification_type='status_update',
                title='Marking Complete',
                message=f'Your exam for {application.unit_code} has been marked.'
            )
            
            messages.success(request, 'Marks submitted successfully!')
            return redirect('lecturer_assignments')
    else:
        form = ExamMarkingForm(instance=marking)
    
    context = {
        'application': application,
        'form': form,
        'marking': marking,
    }
    
    return render(request, 'lecturer/mark_exam.html', context)


@login_required
def lecturer_unit_assignments(request):
    """Lecturer manages unit assignments"""
    try:
        lecturer = request.user.lecturer_profile
    except:
        messages.error(request, 'Lecturer profile not found.')
        return redirect('login')
    
    assignments = lecturer.unit_assignments.all().order_by('-created_at')
    
    context = {
        'assignments': assignments,
    }
    
    return render(request, 'lecturer/unit_assignments.html', context)