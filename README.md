# Assignment_Submission_Tool
This project is made to easy learning for student and teacher manage assignment submission .
In this project there is three pannel 
1.Admin pannel    2.Stdent pannel   3.Teacher Pannel

ADMIN PANNEL:  
1> Admin pannel is a super user of our project which can handle all request of teacher and student to signup admin can approve or decline if admin approve the users then user become active and can signin to their account and if admin decline request to signup then user can not signin it will automatically delete their account.
2> Admin also handle the request to assign subject  to teacher every teacher send request to teach particular subject then request comes to admin pannel if admin approve then teacher can able to teach that subject if admin decline then request will be deleted and teacher can not teach that subject.
3>Admin can also have handle to create the subject delete subject.

Teacher Pannel:
1>Teacher can able to  see all subject which are added by admin then he can send request to teach if admin approve then teacher can teach that subject else not 
Teacher have feature to upload assignment view assignment in view assignment he can able to see all assignment uploaded by him and all response from student side for particular assignment,after evaluate assignment teacher can give marks and after giving marks student can able to see his marks.

Student Pannel:
1> student can able to see all subject which are created by admin student can reqest to enroll after enroll click its in pemding stage and request goes to teacher who teaches that subject if teacher approve then student can enrolled that subject and able to see all assignment for that subject he can dounload assignment upload assignment within due date and check their marks.
NOTE:
 To OPEN ADMIN PANNEL go to login pagin enter credential email id :- admin@gmail.com    password:admin
 Student:-email:radha@gmail.com   psw:-12345
          email:sarita@gmail.com   pdw:-12345
          
          
 Teacher :email :amit@gmail.com    psw:12345
 
 
TECHNOLOGY USED FOR THIS PROJECT :JAVASCRIPT,HTML,CSS,SQLITE3 DATABASE,DJANGO FRAMEWORK,
 
 
 
 
 Work FLOW:
 
 . first of user have to signup their account then request goes to admin pannel if admin approve then only user can login their account otherwise not to approve request admin can see request in admin pannel if he want to approve then approve else decline 
 
 .if admin approve then users become active user and can able to login their account i have have hadle each validdation in signup page and login page .
 a> name can not be space bar   ,mob no should be 10 digit numeric,emailid must contain @ and .com  ,password and confirm password should be matched.
 b>if new user signup with email which is already registered then it can through error msg .
 
 . In teacher panner teacher can able to see all subject which is added by admin and which not assigned to another teacher if teacher wats to teach that subject then teacher can send request to teach now this will be in pending stage and admin can able to see this request if admin approve then teacher can teach that subject.
 . Teacher can upload assignment and able to see all student erolled for that class and submitted assignment by students and teacher can give marks on assignment.
 
 .after login to student account student can able to see all subject now student ca request to learn that subject now this request goes to teacher for that subject if teacher approve then studet able to join that class and he can view all assignment uploaded by teacher and can upload file then teacher can give marks and student can able to see marks.
