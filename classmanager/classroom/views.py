from django.shortcuts import render,get_object_or_404,redirect
from django.views import generic
from django.views.generic import  (View,TemplateView,
                                  ListView,DetailView,
                                  CreateView,UpdateView,
                                  DeleteView)
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from classroom.forms import UserForm,TeacherProfileForm,StudentProfileForm,TeacherProfileUpdateForm,StudentProfileUpdateForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from django.http import HttpResponseRedirect,HttpResponse
from classroom import models
from classroom.models import StudentsInClass, Student, Teacher, CreditClass, ClassActivity
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q


# For Teacher Sign Up
def TeacherSignUp(request):
    user_type = 'teacher'
    registered = False

    if request.method == "POST":
        user_form = UserForm(data = request.POST)
        teacher_profile_form = TeacherProfileForm(data = request.POST)

        if user_form.is_valid() and teacher_profile_form.is_valid():

            user = user_form.save()
            user.is_teacher = True
            user.save()

            profile = teacher_profile_form.save(commit=False)
            profile.user = user
            profile.save()

            registered = True
        else:
            print(user_form.errors,teacher_profile_form.errors)
    else:
        user_form = UserForm()
        teacher_profile_form = TeacherProfileForm()

    return render(request,'classroom/teacher_signup.html',{'user_form':user_form,'teacher_profile_form':teacher_profile_form,'registered':registered,'user_type':user_type})


###  For Student Sign Up
def StudentSignUp(request):
    user_type = 'student'
    registered = False

    if request.method == "POST":
        user_form = UserForm(data = request.POST)
        student_profile_form = StudentProfileForm(data = request.POST)

        if user_form.is_valid() and student_profile_form.is_valid():

            user = user_form.save()
            user.is_student = True
            user.save()

            profile = student_profile_form.save(commit=False)
            profile.user = user
            profile.save()

            registered = True
        else:
            print(user_form.errors,student_profile_form.errors)
    else:
        user_form = UserForm()
        student_profile_form = StudentProfileForm()

    return render(request,'classroom/student_signup.html',{'user_form':user_form,'student_profile_form':student_profile_form,'registered':registered,'user_type':user_type})

## Sign Up page which will ask whether you are teacher or student.
def SignUp(request):
    return render(request,'classroom/signup.html',{})

## login view.
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('home'))

            else:
                return HttpResponse("Account not active")

        else:
            messages.error(request, "Invalid Details")
            return redirect('classroom:login')
    else:
        return render(request,'classroom/login.html',{})

## logout view.
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

## User Profile of student.
class StudentDetailView(LoginRequiredMixin,DetailView):
    context_object_name = "student"
    model = models.Student
    template_name = 'classroom/student_detail_page.html'

## User Profile for teacher.
class TeacherDetailView(LoginRequiredMixin,DetailView):
    context_object_name = "teacher"
    model = models.Teacher
    template_name = 'classroom/teacher_detail_page.html'

## Profile update for students.
@login_required
def StudentUpdateView(request,pk):
    profile_updated = False
    student = get_object_or_404(models.Student,pk=pk)
    if request.method == "POST":
        form = StudentProfileUpdateForm(request.POST,instance=student)
        if form.is_valid():
            profile = form.save(commit=False)
            if 'student_profile_pic' in request.FILES:
                profile.student_profile_pic = request.FILES['student_profile_pic']
            profile.save()
            profile_updated = True
    else:
        form = StudentProfileUpdateForm(request.POST or None,instance=student)
    return render(request,'classroom/student_update_page.html',{'profile_updated':profile_updated,'form':form})

## Profile update for teachers.
@login_required
def TeacherUpdateView(request,pk):
    profile_updated = False
    teacher = get_object_or_404(models.Teacher,pk=pk)
    if request.method == "POST":
        form = TeacherProfileUpdateForm(request.POST,instance=teacher)
        if form.is_valid():
            profile = form.save(commit=False)
            if 'teacher_profile_pic' in request.FILES:
                profile.teacher_profile_pic = request.FILES['teacher_profile_pic']
            profile.save()
            profile_updated = True
    else:
        form = TeacherProfileUpdateForm(request.POST or None,instance=teacher)
    return render(request,'classroom/teacher_update_page.html',{'profile_updated':profile_updated,'form':form})

class ClassStudentsListView(LoginRequiredMixin,DetailView):
    model = models.Teacher
    template_name = "classroom/class_students_list.html"
    context_object_name = "teacher"

## To add student in the class.
class add_student(LoginRequiredMixin,generic.RedirectView):

    def get_redirect_url(self,*args,**kwargs):
        return reverse('classroom:students_list')

    def get(self,request,*args,**kwargs):
        student = get_object_or_404(models.Student,pk=self.kwargs.get('pk'))

        try:
            StudentsInClass.objects.create(teacher=self.request.user.Teacher,student=student)
        except:
            messages.warning(self.request,'warning, Student already in class!')
        else:
            messages.success(self.request,'{} successfully added!'.format(student.name))

        return super().get(request,*args,**kwargs)

@login_required
def student_added(request):
    return render(request,'classroom/student_added.html',{})

## List of students which are not added by teacher in their class.
def students_list(request):
    query = request.GET.get("q", None)
    students = StudentsInClass.objects.filter(teacher=request.user.Teacher)
    students_list = [x.student for x in students]
    qs = Student.objects.all()
    if query is not None:
        qs = qs.filter(
                Q(name__icontains=query)
                )
    qs_one = []
    for x in qs:
        if x in students_list:
            pass
        else:
            qs_one.append(x)

    context = {
        "students_list": qs_one,
    }
    template = "classroom/students_list.html"
    return render(request, template, context)

## List of all the teacher present in the portal.
def teachers_list(request):
    query = request.GET.get("q", None)
    qs = Teacher.objects.all()
    if query is not None:
        qs = qs.filter(
                Q(name__icontains=query)
                )

    context = {
        "teachers_list": qs,
    }
    template = "classroom/teachers_list.html"
    return render(request, template, context)


####################################################
## For changing password.
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST , user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Password changed")
            return redirect('home')
        else:
            return redirect('classroom:change_password')
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form':form}
        return render(request,'classroom/change_password.html',args)
    
def class_list(request):
    context = {
        'credit_class': CreditClass.objects.all()
    }
    return render(request, 'classroom/class_list.html', context)

## List of all students that teacher has added in their class.
def class_details(request, pk):
    # query = request.GET.get("q", None)
    students = StudentsInClass.objects.filter(credit_class=pk)
    activities = ClassActivity.objects.filter(credit_class=pk)
    activities_list = [x for x in activities]
    students_list = [x.student for x in students]
    
    context = {
        "class_students_list": students_list,
        "activities": activities_list,
    }
    template = "classroom/class_students_list.html"
    return render(request, template, context)
