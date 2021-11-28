from django.db import models
from django.contrib.auth.models import User
from django.utils import tree


class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=20)
    higher_education = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.user.first_name+ " "+ self.user.last_name + " " + self.user.username
    


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=20)
    
    def __str__(self):
        return self.user.first_name+ " "+ self.user.last_name + " " + self.user.username


class Subject(models.Model):
    name =  models.CharField(max_length=50)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL,null=True, blank=True)
    status = models.CharField(max_length=10, default="0")

    def __str__(self):
        return self.name

class SubjectRequest(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Enroll(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    status = models.IntegerField(default=0,null=True)


class Assignment(models.Model):
    name = models.CharField(max_length=100, null=True)
    file_assign = models.FileField(upload_to="assignment")
    max_marks = models.IntegerField(default=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    due_date = models.DateField(null=True)

class AssignmentSubmit(models.Model):
    file_submit = models.FileField(upload_to="assignment/submission/")
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    get_marks = models.IntegerField(default=0)