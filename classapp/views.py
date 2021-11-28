from django.db.models.query_utils import select_related_descend
from django.shortcuts import render, redirect
from django.http import HttpResponse,FileResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from classapp.models import *
from datetime import datetime

# Create your views here.
def login_page(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    else:
        return render(request, 'login.html')

def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            u = User.objects.get(username=email)
            if u.is_active==False:
                message = "You are not aproved by admin yet!"
            return render(request, 'login.html', {"message":message})
        except:
            pass
        user = authenticate(username = email, password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                if user.is_superuser:
                    return redirect('/admin/')
                return redirect('/dashboard/')
            else:
                return HttpResponse("User is not active")
        else:
            message = "Wrong username or password!! try again"
            return render(request, 'login.html', {"message":message})
    else:
        message = "Wrong request"
        return render(request, 'login.html', {"message":message})


def admin_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return render(request,"admin/main.html")
        else:
            return HttpResponse("you are not admin user")
    return redirect("/")


def admin_student_request(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            users = User.objects.filter(is_staff=False, is_active=False)
            students = User.objects.filter(is_staff=False)
            return render(request,"admin/viewstudent.html", {"users":users, "students":students})
        else:
            return HttpResponse("You are not admin user!!")
    return redirect("/")


def admin_teacher_request(request):
    teacher_list = []
    if request.user.is_authenticated:
        if request.user.is_superuser:
            teachers = Teacher.objects.all()
            for teacher in teachers:
                if teacher.user.is_staff:
                    if teacher.user.is_active==False:
                        teacher_list.append(teacher)
            print(teacher_list)
            return render(request, "admin/viewteacher.html", {"teacher_list":teacher_list, "teachers":teachers})
        else:
            return HttpResponse("You are not admin user!!")
    return redirect("/") 

def do_active_user(request, user_id):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            user = User.objects.get(id=user_id)
            user.is_active = True
            user.save()
            if user.is_staff:
                return redirect('/admin/teacher/request/')
            else:
                return redirect('/admin/student/request/')

def do_delete_user(request, user_id):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            user = User.objects.get(id=user_id)
            teacher = user.is_staff
            user.delete()
            if teacher:
                return redirect("/admin/teacher/request/")
            else:
                return redirect("/admin/student/request/")
                
        else:
            return HttpResponse("You are not admin user")
    return redirect('/admin/')


def admin_subjectform(request):
    if request.method=="GET":
        if request.user.is_authenticated:
            if request.user.is_superuser:
                subjects = Subject.objects.all()
                return render(request, "admin/subjectform.html", {"subjects":subjects})
        else:
            return redirect("/")
    if request.method == "POST":
        name = request.POST.get("subject")
        subject = Subject(name=name)
        subject.save()
        return redirect("/admin/subjects/")


def subject_request(request, subject_id):
    if request.user.is_staff:
        sub = Subject.objects.get(id=subject_id)
        subreq = SubjectRequest(subject=sub, user=request.user)
        subreq.save()
        return redirect("/dashboard/")
    else:
        return HttpResponse("You are not a teacher!")


def subject_admin(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            subreq = SubjectRequest.objects.all()
            subjects = Subject.objects.all()
            return render(request, "admin/subjectrequest.html",{"subjectrequest":subreq,"subjects":subjects})
        return HttpResponse("you are not admin user")
    return redirect("/")

def subject_approval(request, re_subject_id):
    sq = SubjectRequest.objects.get(id=re_subject_id)
    teacher = Teacher.objects.get(user = sq.user)
    subject = Subject.objects.get(id=sq.subject.id)
    subject.teacher = teacher
    subject.save()
    reqsubjects = SubjectRequest.objects.filter(subject=subject)
    reqsubjects.delete()
    return redirect("/admin/subject/request/")

def subject_delete(request,id):
    sub = Subject.objects.get(id=id)
    sub.delete()
    return redirect("/admin/subjects/")

def subject_request_delete(request,re_subject_id):
    sq = SubjectRequest.objects.get(id=re_subject_id)
    sq.delete()
    return redirect("/admin/subject/request/")

def dashboard(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect("/admin/")
        if request.user.is_staff:
            teacher = Teacher.objects.get(user=request.user)
            subjects = Subject.objects.filter(teacher=teacher)
            non_teach_subjects = Subject.objects.filter(teacher=None)
            subreq = SubjectRequest.objects.filter(user=request.user)
            for i in range(len(non_teach_subjects)):
                for s in subreq:
                    if s.subject==non_teach_subjects[i]:
                        non_teach_subjects[i].status=1 #for pending
            context = {
            'subjects':subjects,
            "non_teach_subjects":non_teach_subjects 
            }
            return render(request, 'teacher/subject.html', context)
        else:
            try:
                student = Student.objects.get(user=request.user)
            except:
                student = Student(user=request.user)
                student.save()
            subjects = Subject.objects.all()
            enrolls = Enroll.objects.filter(student=student,status=1)
            pendings = Enroll.objects.filter(student=student,status=0)
            for subject in subjects:
                for en in enrolls:
                    if en.subject == subject:
                        subject.status = str(2)
                for pen in pendings:
                    if pen.subject == subject:
                        subject.status = str(1)
                
            context = {
            "subjects":subjects,
            "enrolls": enrolls,
            "pendings": pendings
            }
            return render(request, 'student/subject.html',context)
    else:
        return redirect('/')


def log_out(request):
    logout(request)
    return redirect('/')


def signup_page(request,roll):
    if not request.user.is_authenticated:
        if roll=="teacher":
            return render(request,'teacher/signup.html')
        if roll=="student":
            return render(request, 'student/signup.html')
    return  HttpResponse("Wrong Request!!!")
def createuser(request):
    if request.method=="POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        mobile = request.POST.get('mobile')
        role = request.POST.get('role')
        try:
            User.objects.get(username=email)
            if role=="teacher":
                return render(request,"teacher/signup.html",{"message":"Email already Exists"})
            elif role=="student":
                return render(request,"student/signup.html",{"message":"Email already Exists"})
        except:
            pass
        if confirm_password==password:
            pass
        else:
            if role=="teacher":
                return render(request,"teacher/signup.html",{"message":"password and confirm password does not matched"})
            elif role=="student":
                return render(request,"student/signup.html",{"message":"password and confirm password does not matched"})
        user = User.objects.create_user(username = email,email=email, password = password)
        user.first_name = first_name
        user.last_name = last_name
        user.is_active = False
        user.save()
        if role=="teacher":
            teacher = Teacher(user=user, mobile=mobile,higher_education="PhD.")
            user.is_staff=True
            user.higher_education = request.POST.get('qualification')
            user.save()
            teacher.save()
        elif role=="student":
            student = Student(user=user, mobile=mobile)
            student.save()
        context = {
            'message': 'user successfully created!!'
        }
        return render(request, 'login.html', context)
    else:
        return render(request, 'student/signup.html')
    
def teacherview(request):
    subject = Subject.objects.filter(teacher=request.user)
    context = {
        'subjects':subject,
    }
    pass
    return render(request, 'teacher/subject.html')

def viewsubjectbyteacher(request,subject_id):
    subject = Subject.objects.get(id=subject_id)
    enrolls = Enroll.objects.filter(subject=subject)
    context = {
        "subject":subject,
        "students":enrolls,
    }
    return render(request, 'teacher/subjectview.html',context)

def enrollapproval(request, enroll_id):
    if request.user.is_staff:
        enroll = Enroll.objects.get(id=enroll_id)
        enroll.status = 1
        enroll.save()
        return redirect('/subject/' + str(enroll.subject.id))
    else:
        return HttpResponse("Wrong Request")

def delete_enroll(request,enroll_id):
    if request.user.is_staff:
        enroll = Enroll.objects.get(id=enroll_id)
        subject_id = str(enroll.subject.id)
        enroll.delete()
        return redirect('/subject/'+subject_id)



def assignmentuploadpage(request, subject_id):
    subject = Subject.objects.get(id=subject_id)
    return render(request, 'teacher/uploadassignment.html', {'subject':subject})


def uploadassignment(request, subject_id):
    try:
        subject  = Subject.objects.get(id=subject_id)
    except:
        return HttpResponse("Subject does not exist!!")
    if request.method=="POST":
        title = request.POST.get("title")
        max_marks = int(request.POST.get("max_marks"))
        due_date = request.POST.get('due_date')
        due_date = due_date.replace("-","/")
        due_date = datetime.strptime(due_date,"%Y/%m/%d")
        assignment = Assignment(max_marks=max_marks, file_assign=request.FILES['file'],name=title,subject=subject)
        assignment.due_date = due_date
        assignment.save()
        return redirect('/subject/assignments/' + str(assignment.subject.id))
    else:
        return HttpResponse("wrong request !!")


def viewassignments(request,subject_id):
    subject = Subject.objects.get(id=subject_id)
    assignments = Assignment.objects.filter(subject=subject)
    context = {"assignments": assignments, "subject":subject}
    if request.user.is_staff:
        return render(request, "teacher/viewassignment.html",context)
    else:
        return render(request, "student/viewassignment.html",context)


def downloadsubassignment(request, subassignment_id):
    obj = AssignmentSubmit.objects.get(id=subassignment_id)
    filename = "media/" + str(obj.file_submit)
    response = FileResponse(open(filename,'rb'))
    return response

def downloadassignment(request, assignment_id):
    obj = Assignment.objects.get(id=assignment_id)
    filename = "media/" + str(obj.file_assign)
    response = FileResponse(open(filename,'rb'))
    return response


def assignmentresponse(request,assignment_id):
    if request.user.is_staff==True:
        assignment = Assignment.objects.get(id=assignment_id)
        submitassigns = AssignmentSubmit.objects.filter(assignment=assignment)
        context ={
            "submitassigns":submitassigns,
        }
        return render(request, "teacher/assignmentresponse.html", context)
    else:
        return HttpResponse("Wrong request!!")


def newenrollment(request,subject_id):
    student = Student.objects.get(user=request.user)
    subject = Subject.objects.get(id=subject_id)
    message = ""
    try:
        enroll = Enroll.objects.get(student=student,subject=subject)
        message = "Already enrolled in this subject!!"
    except:
        enroll = Enroll(student=student,subject=subject)
        enroll.save()
        message = "Successfully enrolled!!"
    return redirect('/dashboard/')


def submitassignment(request, assignment_id):
    if request.method =="GET":
        assignment = Assignment.objects.get(id=assignment_id)
        from datetime import date
        duedate_status = True
        if date.today()>assignment.due_date:
            duedate_status = False
        try:
            assign = AssignmentSubmit.objects.get(assignment=assignment)
            context = {
                "assign":assign,
                "message":"uploaded",
                "duedate_status":duedate_status
            }
            return render(request, "student/submitassign.html",context)
        except:
            context = {
                "assignment_id":assignment_id,
                "message":"else",
                "duedate_status":duedate_status
                }
            return render(request, "student/submitassign.html", context)
    if request.method == "POST":
        assignment = Assignment.objects.get(id=assignment_id)
        student = Student.objects.get(user=request.user)
        if request.user.is_staff == False:
            file_submit = request.FILES['file']
            submit = AssignmentSubmit(assignment=assignment, student=student, file_submit = file_submit)
            submit.save()
            return redirect("/subject/assignments/"+ str(assignment.subject.id))


def assignemtmarks(request, submit_assign_id):
    if request.method == "GET":
        return render(request, 'teacher/assignmarks.html', {"submit_assign_id":submit_assign_id})

    if request.method == "POST":
        sbassign = AssignmentSubmit.objects.get(id=submit_assign_id)
        marks = request.POST.get('marks')
        sbassign.get_marks = marks
        sbassign.save()
        return redirect("/subject/assignment/response/" + str(sbassign.assignment.id))