from django.urls import path
from classapp.views import *
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [

    path('admin/', admin_view, name="admin_view"),
    path('admin/student/request/',admin_student_request, name="admin_student_request"),
    path('admin/teacher/request/',admin_teacher_request, name="admin_teacher_request"),
    path('admin/request/activate/<int:user_id>/', do_active_user, name="do_active_user"),
    path('admin/user/delete/<int:user_id>/',do_delete_user, name="do_delete_user"),
    path("admin/subject/delete/<int:id>/",subject_delete, name="subject_delete"),

    path('admin/subjects/', admin_subjectform, name="admin_subjectform"),
    path('admin/subject/request/', subject_admin, name="subject_admin"),
    path('subject/request/<int:subject_id>/',subject_request, name="subject_request"),

    path('admin/subject/approval/<int:re_subject_id>/', subject_approval, name="subject_approval"),
    path('admin/subject/delete/request/<int:re_subject_id>/', subject_request_delete, name="subject_request_delete"),
    
    path('dashboard/', dashboard, name="dashboard"),
    path("",login_page, name="login_page"),
    path("login_view/",login_view, name="login_view"),
    path('logout/',log_out, name="log_out"),
    path('signupage/<str:roll>/', signup_page, name="signup"),
    path('createuser/', createuser, name="createuser"),
    path('subject/<int:subject_id>/',viewsubjectbyteacher, name="subject_teach"),
    path('subject/assignment/<int:subject_id>/', assignmentuploadpage, name="assignmentuploadpage"),
    path('subject/assignments/<int:subject_id>/', viewassignments, name="viewassignments"),
    path('subject/subassignment/down/<int:subassignment_id>/',downloadsubassignment, name="downloadsubassignment"),
    path('subject/assignment/down/<int:assignment_id>/', downloadassignment, name="downloadassignment"),
    path('subject/assignment/upload/<int:subject_id>/', uploadassignment, name="uplaodassignment"),
    path('subject/assignment/response/<int:assignment_id>/', assignmentresponse, name="assignmentresponse"),
    path('enroll/aproval/<int:enroll_id>/', enrollapproval, name="enrollapproval"),
    path('enroll/delete/<int:enroll_id>/', delete_enroll, name="delete_enroll"),
    path('student/enroll/<int:subject_id>/', newenrollment, name="newenrollment"),
    path('student/submitassignment/<int:assignment_id>/', submitassignment, name="submitassignment"),
    path('teacher/assignmentmarks/<int:submit_assign_id>/',assignemtmarks, name="assignemtmarks")

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)