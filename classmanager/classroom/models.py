from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.conf import settings
import misaka
# Create your models here.

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)


class Student(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,related_name='Student')
    name=models.CharField(max_length=250)
    email = models.EmailField(max_length=254)
    roll_no = models.CharField(max_length=50)
    department = models.CharField(max_length=54)
    phone = models.IntegerField()
    student_profile_pic = models.ImageField(upload_to="classroom/student_profile_pic",blank=True)

    def get_absolute_url(self):
        return reverse('classroom:student_detail',kwargs={'pk':self.pk})

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['roll_no']

class Teacher(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,related_name='Teacher')
    name = models.CharField(max_length=32)
    email = models.EmailField(max_length=254)
    department = models.CharField(max_length=54)
    phone = models.IntegerField()
    teacher_profile_pic = models.ImageField(upload_to="classroom/teacher_profile_pic",blank=True)

    def get_absolute_url(self):
        return reverse('classroom:teacher_detail',kwargs={'pk':self.pk})

    def __str__(self):
        return self.name

class CreditClass(models.Model):
    class_id = models.IntegerField(primary_key=True)
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject_name = models.CharField(max_length=32)
    subject_id = models.CharField(max_length=32)
    number_of_credits = models.IntegerField()
    
    def __str__(self):
        return f"{self.class_id} by {self.teacher_id}"

    
class StudentsInClass(models.Model):
    credit_class = models.ForeignKey(CreditClass, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    midterm_grade = models.FloatField()
    final_grade = models.FloatField()

    def __str__(self):
        return self.student.name

   
class ClassActivity(models.Model):
    credit_class = models.ForeignKey(CreditClass, on_delete=models.CASCADE)  
    week_id = models.IntegerField()
    tracking_video = models.CharField(max_length=1024)

    def __str__(self):
        return f"Class {self.credit_class.class_id} Week {self.week_id}"