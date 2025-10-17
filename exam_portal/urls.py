
from django.urls import path
from . import views

urlpatterns = [
    # ========================================================================
    # AUTHENTICATION URLS
    # ========================================================================
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),
    
    # ========================================================================
    # ADMIN URLS
    # ========================================================================
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # Students Management
    path('admin/students/', views.admin_students_list, name='admin_students_list'),
    path('admin/students/create/', views.admin_student_create, name='admin_student_create'),
    path('admin/students/<int:student_id>/edit/', views.admin_student_edit, name='admin_student_edit'),
    path('admin/students/<int:student_id>/delete/', views.admin_student_delete, name='admin_student_delete'),
    
    # Officers Management
    path('admin/officers/', views.admin_officers_list, name='admin_officers_list'),
    path('admin/officers/create/', views.admin_officer_create, name='admin_officer_create'),
    
    # Lecturers Management
    path('admin/lecturers/', views.admin_lecturers_list, name='admin_lecturers_list'),
    path('admin/lecturers/create/', views.admin_lecturer_create, name='admin_lecturer_create'),
    
    # Applications Management
    path('admin/applications/', views.admin_applications_list, name='admin_applications_list'),
    path('admin/applications/<str:app_id>/', views.admin_application_detail, name='admin_application_detail'),
    
    # ========================================================================
    # STUDENT URLS
    # ========================================================================
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/apply/', views.student_apply_exam, name='student_apply_exam'),
    path('student/applications/', views.student_applications, name='student_applications'),
    path('student/applications/<str:app_id>/', views.student_application_detail, name='student_application_detail'),
    path('student/notifications/', views.student_notifications, name='student_notifications'),
    
    # ========================================================================
    # EXAM OFFICER URLS
    # ========================================================================
    path('officer/dashboard/', views.officer_dashboard, name='officer_dashboard'),
    path('officer/applications/', views.officer_review_applications, name='officer_review_applications'),
    path('officer/applications/<str:app_id>/review/', views.officer_application_review, name='officer_application_review'),
    
    # ========================================================================
    # LECTURER URLS
    # ========================================================================
    path('lecturer/dashboard/', views.lecturer_dashboard, name='lecturer_dashboard'),
    path('lecturer/assignments/', views.lecturer_assignments, name='lecturer_assignments'),
    path('lecturer/assignments/<str:app_id>/mark/', views.lecturer_mark_exam, name='lecturer_mark_exam'),
    path('lecturer/units/', views.lecturer_unit_assignments, name='lecturer_unit_assignments'),
]