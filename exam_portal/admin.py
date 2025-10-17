# ============================================================================
# exam_portal/admin.py - Django Admin Configuration
# ============================================================================

from django.contrib import admin
from django.utils.html import format_html
from .models import (
    UserProfile, Student, ExamOfficer, Lecturer, UnitAssignment,
    ExamApplication, OCRResult, ApplicationReview, ExamMarking, Notification
)


# ============================================================================
# User Profile Admin
# ============================================================================

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'phone_number', 'created_at')
    list_filter = ('user_type', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone_number')
    readonly_fields = ('created_at', 'updated_at')


# ============================================================================
# Student Admin
# ============================================================================

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('registration_number', 'full_name', 'email', 'school', 'program', 'created_at')
    list_filter = ('school', 'program', 'created_at')
    search_fields = ('registration_number', 'first_name', 'last_name', 'email')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'registration_number')
        }),
        ('Personal Details', {
            'fields': ('first_name', 'last_name', 'email', 'phone_number')
        }),
        ('Academic Information', {
            'fields': ('school', 'program')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Full Name'


# ============================================================================
# Exam Officer Admin
# ============================================================================

@admin.register(ExamOfficer)
class ExamOfficerAdmin(admin.ModelAdmin):
    list_display = ('officer_id', 'full_name', 'email', 'department', 'created_at')
    list_filter = ('department', 'created_at')
    search_fields = ('officer_id', 'first_name', 'last_name', 'email')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'officer_id')
        }),
        ('Personal Details', {
            'fields': ('first_name', 'last_name', 'email', 'phone_number')
        }),
        ('Department', {
            'fields': ('department',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Full Name'


# ============================================================================
# Lecturer Admin
# ============================================================================

class UnitAssignmentInline(admin.TabularInline):
    model = UnitAssignment
    extra = 1
    fields = ('unit_code', 'unit_name', 'program', 'year', 'semester', 'active')


@admin.register(Lecturer)
class LecturerAdmin(admin.ModelAdmin):
    list_display = ('lecturer_id', 'full_name', 'email', 'department', 'unit_count', 'created_at')
    list_filter = ('department', 'created_at')
    search_fields = ('lecturer_id', 'first_name', 'last_name', 'email')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [UnitAssignmentInline]
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'lecturer_id')
        }),
        ('Personal Details', {
            'fields': ('first_name', 'last_name', 'email', 'phone_number')
        }),
        ('Department', {
            'fields': ('department',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Full Name'
    
    def unit_count(self, obj):
        return obj.unit_assignments.filter(active=True).count()
    unit_count.short_description = 'Active Units'


# ============================================================================
# Unit Assignment Admin
# ============================================================================

@admin.register(UnitAssignment)
class UnitAssignmentAdmin(admin.ModelAdmin):
    list_display = ('unit_code', 'unit_name', 'lecturer_name', 'program', 'year', 'semester', 'active')
    list_filter = ('active', 'program', 'year', 'semester', 'created_at')
    search_fields = ('unit_code', 'unit_name', 'lecturer__first_name', 'lecturer__last_name')
    readonly_fields = ('created_at',)
    
    def lecturer_name(self, obj):
        return f"{obj.lecturer.first_name} {obj.lecturer.last_name}"
    lecturer_name.short_description = 'Lecturer'


# ============================================================================
# Exam Application Admin
# ============================================================================

class OCRResultInline(admin.StackedInline):
    model = OCRResult
    extra = 0
    readonly_fields = ('extracted_text', 'ocr_summary', 'confidence_score', 'keywords_found', 'processed_at')
    can_delete = False


class ApplicationReviewInline(admin.TabularInline):
    model = ApplicationReview
    extra = 0
    readonly_fields = ('reviewed_by', 'decision', 'reviewed_at')
    can_delete = False


class ExamMarkingInline(admin.StackedInline):
    model = ExamMarking
    extra = 0
    readonly_fields = ('lecturer', 'marked_at', 'updated_at')
    can_delete = False


@admin.register(ExamApplication)
class ExamApplicationAdmin(admin.ModelAdmin):
    list_display = ('application_id', 'student_name', 'unit_code', 'exam_type', 
                   'status_badge', 'auto_verified', 'submitted_at')
    list_filter = ('status', 'exam_type', 'auto_verified', 'year_of_study', 'semester_taken', 'submitted_at')
    search_fields = ('application_id', 'student__registration_number', 'student__first_name', 
                    'student__last_name', 'unit_code', 'unit_name')
    readonly_fields = ('application_id', 'submitted_at', 'updated_at')
    inlines = [OCRResultInline, ApplicationReviewInline, ExamMarkingInline]
    
    fieldsets = (
        ('Application Details', {
            'fields': ('application_id', 'student', 'status', 'auto_verified')
        }),
        ('Academic Information', {
            'fields': ('year_of_study', 'exam_type', 'unit_code', 'unit_name', 
                      'year_taken', 'semester_taken')
        }),
        ('Document & Declaration', {
            'fields': ('supporting_document', 'declaration_accepted')
        }),
        ('Assignment', {
            'fields': ('assigned_lecturer',)
        }),
        ('Timestamps', {
            'fields': ('submitted_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def student_name(self, obj):
        return f"{obj.student.first_name} {obj.student.last_name}"
    student_name.short_description = 'Student'
    
    def status_badge(self, obj):
        colors = {
            'submitted': '#FFA500',
            'under_review': '#1E90FF',
            'approved': '#32CD32',
            'rejected': '#DC143C',
            'exam_received': '#9370DB',
            'marking_complete': '#20B2AA',
            'submitted_to_officer': '#FFD700',
            'uploaded_to_portal': '#228B22',
        }
        color = colors.get(obj.status, '#808080')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-weight: bold;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'


# ============================================================================
# OCR Result Admin
# ============================================================================

@admin.register(OCRResult)
class OCRResultAdmin(admin.ModelAdmin):
    list_display = ('application_id', 'confidence_score', 'verified', 'processed_at')
    list_filter = ('verified', 'processed_at')
    search_fields = ('application__application_id', 'extracted_text')
    readonly_fields = ('application', 'extracted_text', 'ocr_summary', 'confidence_score', 
                      'keywords_found', 'processed_at')
    
    def application_id(self, obj):
        return obj.application.application_id
    application_id.short_description = 'Application ID'


# ============================================================================
# Application Review Admin
# ============================================================================

@admin.register(ApplicationReview)
class ApplicationReviewAdmin(admin.ModelAdmin):
    list_display = ('application_id', 'reviewer_name', 'decision_badge', 'reviewed_at')
    list_filter = ('decision', 'reviewed_at')
    search_fields = ('application__application_id', 'reviewed_by__first_name', 
                    'reviewed_by__last_name', 'comments')
    readonly_fields = ('reviewed_at',)
    
    def application_id(self, obj):
        return obj.application.application_id
    application_id.short_description = 'Application ID'
    
    def reviewer_name(self, obj):
        return f"{obj.reviewed_by.first_name} {obj.reviewed_by.last_name}"
    reviewer_name.short_description = 'Reviewed By'
    
    def decision_badge(self, obj):
        colors = {
            'pending': '#FFA500',
            'approved': '#32CD32',
            'rejected': '#DC143C',
        }
        color = colors.get(obj.decision, '#808080')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-weight: bold;">{}</span>',
            color, obj.get_decision_display()
        )
    decision_badge.short_description = 'Decision'


# ============================================================================
# Exam Marking Admin
# ============================================================================

@admin.register(ExamMarking)
class ExamMarkingAdmin(admin.ModelAdmin):
    list_display = ('application_id', 'lecturer_name', 'marks', 'marked_at')
    list_filter = ('marked_at', 'updated_at')
    search_fields = ('application__application_id', 'lecturer__first_name', 
                    'lecturer__last_name', 'comments')
    readonly_fields = ('marked_at', 'updated_at')
    
    def application_id(self, obj):
        return obj.application.application_id
    application_id.short_description = 'Application ID'
    
    def lecturer_name(self, obj):
        return f"{obj.lecturer.first_name} {obj.lecturer.last_name}"
    lecturer_name.short_description = 'Lecturer'


# ============================================================================
# Notification Admin
# ============================================================================

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('student_reg', 'title', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('student__registration_number', 'title', 'message')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Notification Details', {
            'fields': ('student', 'application', 'notification_type')
        }),
        ('Content', {
            'fields': ('title', 'message')
        }),
        ('Status', {
            'fields': ('is_read', 'created_at')
        }),
    )
    
    def student_reg(self, obj):
        return obj.student.registration_number
    student_reg.short_description = 'Student Reg No.'