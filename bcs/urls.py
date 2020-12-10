from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('',views.index,name='index'),
    # path('exam',views.exam,name='exam'),

    #About Us and Help

    path('help',views.help,name='help'),
    path('aboutus',views.aboutus,name='aboutus'),
    # filter subject url
    path('get/subject',views.get_subject,name='get_subject'),
    path('teacher/info',views.teacher_info,name='teacher_info'),
    path('student/home',views.student_home,name='student_home'),
    path('teacher/home',views.teacher_home,name='teacher_home'),
    
    path('register/teacher',views.register_teacher,name='register_teacher'), #register teacher
    path('register/student',views.register_student,name='register_student'), #register student
    path('login',views.login_user,name='login'), #login user
    path('logout',views.logout,name='logout'),
    path('teacher/profile',views.teacher_profile,name='teacher_profile'), #teacher profile
    path('add/question/<slug:sid>',views.add_question_answer,name='add_question'), # add question
    path('teacher/student',views.teacher_student,name='teacher_student'), #
    path('take/exam/<slug:sid>',views.take_exam,name='take_exam'),
    path('check/ajax',views.check_ajax,name='check_ajax'),
    path('student/exam/data',views.student_exam_data,name='student_exam_data'),
    path('student/pannel',views.student_teacher,name="student_teacher"),
    path('give/exam/<slug:eid>',views.give_exam,name="give_exam"),
    path('student/result/<slug:sid>/<slug:eid>',views.calculate_result,name="calculate_result"),
    path('show/student/<slug:sid>',views.show_student,name='show_student'),
    #path('post/exam/<slug:eid>',views.post_exam,name="post_exam"),
    path('teacher/exam/pannel/<eid>',views.teacher_exam_pannel,name='teacher_exam_pannel'),
    path('dict/data',views.dict_data,name='dict_data'),
    path('update/question/<slug:eid>/<slug:qid>',views.update_question,name='update_question'),
    path('delete/question/<slug:eid>/<slug:qid>',views.delete_question,name='delete_question'),
    path('cancel/exam/<slug:eid>',views.cancel_exam,name="cancel_exam"),
    path('post/exam/<slug:eid>',views.post_exam,name='post_exam'),
    path('previous/exam/<slug:sid>',views.previous_exam,name='previous_exam'),
    path('all/student/result/<slug:eid>',views.all_student_result,name='all_student_result'),
    path('delete/subject/<slug:stid>',views.delete_subject,name='delete_subject'),
    path('create/new/exam/<slug:sid>',views.create_new_exam,name='create_new_exam'),
    
    path('upcome/exam',views.upcome_exam,name='upcome_exam'),
    path('teacher/exam',views.teacher_exam,name='teacher_exam'),
    path('end/exam/<slug:eid>',views.end_exam,name='end_exam'),
    path('student/previous/exam',views.student_previous_exam,name='student_previous_exam'),

    #Study materail

    path('teacher/study/materail/<slug:sid>',views.study_material,name="study_material"),
    path('student/study/materail/<slug:sid>',views.show_study_material,name="show_study_material"),
    path("delete/study/material/<slug:stdmid>",views.delete_study_material,name="delete_study_material"),
    #Notice Board

    path("teacher/notice",views.teacher_notice,name="teacher_notice"),
    path("delete/notice/<slug:nid>",views.delete_notice,name="delete_notice"),
    #chatting
    path("student/query/<slug:tid>/<slug:sid>",views.student_query,name='student_query'),

    #Attendance
    path('attendance/<slug:sid>',views.attendance,name='attendace'),
    path('teacher/attendance',views.teacher_attendance,name='teacher_attendance'),
    path('student/attendance/<slug:sid>/<slug:tat_id>',views.student_attendance,name='student_attendance'),
    path('take/attendance/<slug:sid>/<slug:tat_id>',views.take_attendance,name='take_attendance'),
    path('attendance/report/<slug:sid>/<slug:tat_id>',views.attendance_report,name='attendance_report'),
    path('cancel/attendance/<slug:tat_id>',views.cancel_attendance,name='cancel_attendance'),

    #Attendance Detail

    path('teacher/attendance/detail/<slug:sid>',views.attendance_detail,name='attendance_detail'),
    path('update/attendance/<slug:tat_id>',views.update_attendance,name='update_attendance'),
    #Attendance Report
    path('attendance/month/report',views.attendance_month,name='attendance_month_report'),
    path('attendance/month/form/<slug:sid>',views.attendance_month_form,name='attendance_month_form')
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    