from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Student,Teacher,StudentsInClass, CreditClass, ClassActivity
# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(StudentsInClass)
admin.site.register(CreditClass)
admin.site.register(ClassActivity)