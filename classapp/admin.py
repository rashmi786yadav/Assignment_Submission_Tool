from django.contrib import admin
from classapp.models import Assignment, AssignmentSubmit,Teacher, Student, Subject,Enroll

# Register your models here.

admin.site.register([Assignment, AssignmentSubmit,Teacher, Student,Subject,Enroll])
