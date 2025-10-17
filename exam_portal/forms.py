# ============================================================================
# forms.py - All Forms for Exam Tracking System
# ============================================================================

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import *
import random
import string


# ============================================================================
# STUDENT FORMS
# ============================================================================

class StudentCreationForm(forms.ModelForm):
    """Form for creating a new student"""
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)
    
    class Meta:
        model = Student
        fields = ['registration_number', 'first_name', 'last_name', 'email', 
                  'phone_number', 'school', 'program']
        widgets = {
            'registration_number': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'school': forms.Select(attrs={'class': 'form-control'}),
            'program': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})
        self.fields['confirm_password'].widget.attrs.update({'class': 'form-control'})
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Username already exists.')
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Student.objects.filter(email=email).exists():
            raise ValidationError('Email already exists.')
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            raise ValidationError('Passwords do not match.')
        
        return cleaned_data
    
    def save(self, commit=True):
        # Create User
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name']
        )
        
        # Create UserProfile
        UserProfile.objects.create(
            user=user,
            user_type='student',
            phone_number=self.cleaned_data.get('phone_number', '')
        )
        
        # Create Student
        student = super().save(commit=False)
        student.user = user
        if commit:
            student.save()
        
        return student


class StudentEditForm(forms.ModelForm):
    """Form for editing student details"""
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'school', 'program']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'school': forms.Select(attrs={'class': 'form-control'}),
            'program': forms.Select(attrs={'class': 'form-control'}),
        }


# ============================================================================
# EXAM OFFICER FORMS
# ============================================================================

class OfficerCreationForm(forms.ModelForm):
    """Form for creating a new exam officer"""
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)
    
    class Meta:
        model = ExamOfficer
        fields = ['officer_id', 'first_name', 'last_name', 'email', 
                  'phone_number', 'department']
        widgets = {
            'officer_id': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})
        self.fields['confirm_password'].widget.attrs.update({'class': 'form-control'})
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Username already exists.')
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if ExamOfficer.objects.filter(email=email).exists():
            raise ValidationError('Email already exists.')
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            raise ValidationError('Passwords do not match.')
        
        return cleaned_data
    
    def save(self, commit=True):
        # Create User
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name']
        )
        
        # Create UserProfile
        UserProfile.objects.create(
            user=user,
            user_type='officer',
            phone_number=self.cleaned_data.get('phone_number', '')
        )
        
        # Create ExamOfficer
        officer = super().save(commit=False)
        officer.user = user
        if commit:
            officer.save()
        
        return officer


# ============================================================================
# LECTURER FORMS
# ============================================================================

class LecturerCreationForm(forms.ModelForm):
    """Form for creating a new lecturer"""
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)
    
    class Meta:
        model = Lecturer
        fields = ['lecturer_id', 'first_name', 'last_name', 'email', 
                  'phone_number', 'department']
        widgets = {
            'lecturer_id': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})
        self.fields['confirm_password'].widget.attrs.update({'class': 'form-control'})
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Username already exists.')
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Lecturer.objects.filter(email=email).exists():
            raise ValidationError('Email already exists.')
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            raise ValidationError('Passwords do not match.')
        
        return cleaned_data
    
    def save(self, commit=True):
        # Create User
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name']
        )
        
        # Create UserProfile
        UserProfile.objects.create(
            user=user,
            user_type='lecturer',
            phone_number=self.cleaned_data.get('phone_number', '')
        )
        
        # Create Lecturer
        lecturer = super().save(commit=False)
        lecturer.user = user
        if commit:
            lecturer.save()
        
        return lecturer


# ============================================================================
# EXAM APPLICATION FORMS
# ============================================================================

class ExamApplicationForm(forms.ModelForm):
    """Form for students to submit exam applications"""
    class Meta:
        model = ExamApplication
        fields = ['year_of_study', 'exam_type', 'unit_name', 'unit_code',
                  'year_taken', 'semester_taken', 'supporting_document', 
                  'declaration_accepted']
        widgets = {
            'year_of_study': forms.Select(attrs={'class': 'form-control'}),
            'exam_type': forms.Select(attrs={'class': 'form-control'}),
            'unit_name': forms.TextInput(attrs={'class': 'form-control'}),
            'unit_code': forms.TextInput(attrs={'class': 'form-control'}),
            'year_taken': forms.NumberInput(attrs={'class': 'form-control', 'min': '2015', 'max': '2025'}),
            'semester_taken': forms.Select(attrs={'class': 'form-control'}),
            'supporting_document': forms.FileInput(attrs={'class': 'form-control'}),
            'declaration_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'declaration_accepted': 'I declare that the information provided is true and correct',
        }
    
    def clean_declaration_accepted(self):
        accepted = self.cleaned_data.get('declaration_accepted')
        if not accepted:
            raise ValidationError('You must accept the declaration to submit the application.')
        return accepted
    
    def clean_supporting_document(self):
        document = self.cleaned_data.get('supporting_document')
        if document:
            # Validate file size (max 5MB)
            if document.size > 5 * 1024 * 1024:
                raise ValidationError('File size must not exceed 5MB.')
            
            # Validate file type
            allowed_types = ['application/pdf', 'image/jpeg', 'image/png', 'image/jpg']
            if document.content_type not in allowed_types:
                raise ValidationError('Only PDF and image files (JPG, PNG) are allowed.')
        
        return document


class ApplicationReviewForm(forms.ModelForm):
    """Form for exam officers to review applications"""
    class Meta:
        model = ApplicationReview
        fields = ['decision', 'comments']
        widgets = {
            'decision': forms.Select(attrs={'class': 'form-control'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        decision = cleaned_data.get('decision')
        comments = cleaned_data.get('comments')
        
        if decision == 'rejected' and not comments:
            raise ValidationError('Comments are required when rejecting an application.')
        
        return cleaned_data


class ExamMarkingForm(forms.ModelForm):
    """Form for lecturers to mark exams"""
    class Meta:
        model = ExamMarking
        fields = ['marks', 'comments']
        widgets = {
            'marks': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '100',
                'step': '0.01'
            }),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
    
    def clean_marks(self):
        marks = self.cleaned_data.get('marks')
        if marks is not None:
            if marks < 0 or marks > 100:
                raise ValidationError('Marks must be between 0 and 100.')
        return marks


class UnitAssignmentForm(forms.ModelForm):
    """Form for assigning units to lecturers"""
    class Meta:
        model = UnitAssignment
        fields = ['lecturer', 'unit_code', 'unit_name', 'program', 'year', 'semester', 'active']
        widgets = {
            'lecturer': forms.Select(attrs={'class': 'form-control'}),
            'unit_code': forms.TextInput(attrs={'class': 'form-control'}),
            'unit_name': forms.TextInput(attrs={'class': 'form-control'}),
            'program': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'semester': forms.Select(attrs={'class': 'form-control'}, choices=[('1', 'Semester 1'), ('2', 'Semester 2')]),
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }