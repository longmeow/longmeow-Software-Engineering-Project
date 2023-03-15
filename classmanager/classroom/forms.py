from django import forms
from django.contrib.auth.forms import UserCreationForm
from classroom.models import User, Teacher, Student
from django.db import transaction

# User Login Form (Applied in both student and teacher login)


class UserForm(UserCreationForm):
    class Meta():
        model = User
        fields = ['username', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'answer'}),
            'password1': forms.PasswordInput(attrs={'class': 'answer'}),
            'password2': forms.PasswordInput(attrs={'class': 'answer'}),
        }

# Teacher Registration Form


class TeacherProfileForm(forms.ModelForm):
    class Meta():
        model = Teacher
        fields = ['name', 'phone', 'email', 'department']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'answer'}),
            'phone': forms.NumberInput(attrs={'class': 'answer'}),
            'email': forms.EmailInput(attrs={'class': 'answer'}),
            'department': forms.TextInput(attrs={'class': 'answer'})
        }

# Teacher Profile Update Form


class TeacherProfileUpdateForm(forms.ModelForm):
    class Meta():
        model = Teacher
        fields = ['name', 'email', 'phone',
                  'department', 'teacher_profile_pic']

# Student Registration Form


class StudentProfileForm(forms.ModelForm):
    class Meta():
        model = Student
        fields = ['name', 'student_id', 'phone', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'answer'}),
            'student_id': forms.NumberInput(attrs={'class': 'answer'}),
            'phone': forms.NumberInput(attrs={'class': 'answer'}),
            'email': forms.EmailInput(attrs={'class': 'answer'}),
        }

# Student profile update form


class StudentProfileUpdateForm(forms.ModelForm):
    class Meta():
        model = Student
        fields = ['name', 'student_id', 'email', 'phone', 'student_profile_pic']
