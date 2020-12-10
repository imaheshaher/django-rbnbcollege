from django.db import models

from django.shortcuts import HttpResponse,reverse,redirect
import datetime
from django.contrib.auth.models import User

from django.conf import settings
import datetime
# Create your models here.

class_choice= (
    ('All','All'),
    ('FY','FY'),
    ('SY','SY'),
    ('TY','TY')
  
)

department_choice = (
    ('Bsc','Bsc'),
    ('Bsc Computer Science','Bsc Computer Science'),
    ('BA','BA'),
    ('MA','MA'),
    ('Msc','Msc'),
    ('Mcs','Mcs'),

)


class Subjects(models.Model):
    subject_name=models.CharField(max_length=20)
    department_name=models.CharField(max_length=30,choices=department_choice,blank=True,null=True)
    class_name=models.CharField(max_length=20,choices=class_choice)

    def __str__(self):
        return '{}'.format(self.subject_name)


class Teachers(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    department_name=models.CharField(max_length=20,choices=department_choice,null=True,blank=True)
    def __str__(self):
        return r'{} {}'.format(self.user.first_name,self.user.last_name)

class Students(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    roll_no=models.IntegerField(null=True,blank=True)                                       
    department_name=models.CharField(max_length=20,choices=department_choice,null=True,blank=True)
    class_name=models.CharField(max_length=20,choices=class_choice)

    def __str__(self):
        return str(self.user)

    def is_students(self):
        return True
class Subject_Teacher(models.Model):
    subject=models.ForeignKey(Subjects,on_delete=models.CASCADE)
    teacher=models.ForeignKey(Teachers,on_delete=models.CASCADE)
    department_name=models.CharField(max_length=20,choices=department_choice,null=True,blank=True)

    def __str__(self):
        return '{} - {}'.format(self.subject,self.teacher)

    def update_delete_subject(self):
        print(self.id)
       
        return reverse('teacher_profile')


class Study_material(models.Model):
    teacher_user=models.ForeignKey(Teachers,on_delete=models.CASCADE)
    subject = models.ForeignKey(Subjects,on_delete=models.CASCADE)
    class_name=models.CharField(max_length=20,choices=class_choice)
    department_name=models.CharField(max_length=20,choices=department_choice,null=True,blank=True)
    study_image=models.ImageField(upload_to="images/",blank=True,null=True)
    study_file=models.FileField(upload_to="uploads/",blank=True,null=True)
    study_description=models.TextField(blank=True)
    study_materail_date = models.DateField(auto_now_add=True)
    study_material_time = models.TimeField(auto_now_add=True)


class Question(models.Model):
    teacher=models.ForeignKey(Teachers,on_delete=models.CASCADE)
    question_text=models.CharField(max_length=250)


class Answers(models.Model):
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    answer=models.CharField(max_length=250)
    correct_answer=models.BooleanField(default=False)

class Exam(models.Model):
    teacher=models.ForeignKey(Teachers,on_delete=models.CASCADE)
    subject=models.ForeignKey(Subjects,on_delete=models.CASCADE)
    exam_date=models.DateField(blank=True,default=datetime.date.today())
    start_time=models.TimeField(blank=True,default=datetime.time(12,00,00))
    end_time=models.TimeField(blank=True,default=datetime.time(1,00,00))
    exam_time=models.IntegerField(default=10)
    post_exam=models.BooleanField(default=False)
    exam_status=models.BooleanField(default=False)


    # def update_exam_status(self):
    #     try:
    #         q=Question_Answer.objects.filter(exam__id=self.id)
    #         print(q)
    #         if q.exists():
    #             Exam.objects.update(post_exam=True)
    #             return reverse("teacher_exam_pannel",kwargs = {
    #                 'eid':self.id
    #             })
    #         else:
    #             print('not yet')
    #     except:
    #         pass
class Question_Answer(models.Model):
    exam=models.ForeignKey(Exam,on_delete=models.CASCADE)
    
    question_text=models.CharField(max_length=250)
    option_1=models.CharField(max_length=250)
    option_2=models.CharField(max_length=250)
    option_3=models.CharField(max_length=250)
    option_4=models.CharField(max_length=250)
    correct_answer=models.CharField(max_length=250)

    def __str__(self):
        return str(self.question_text)




class Student_Result(models.Model):
    student=models.ForeignKey(Students,on_delete=models.CASCADE)
    exam=models.ForeignKey(Exam,on_delete=models.CASCADE,null=True,blank=True)
    question=models.ForeignKey(Question_Answer,on_delete=models.CASCADE)
    student_answer=models.CharField(max_length=250)
    

class Student_Mark(models.Model):
    student=models.ForeignKey(Students,on_delete=models.CASCADE)
    exam=models.ForeignKey(Exam,on_delete=models.CASCADE)
    student_mark=models.IntegerField()
    out_of_mark=models.IntegerField()




class Notice_Board(models.Model):
    teacher=models.ForeignKey(Teachers,on_delete=models.CASCADE)
    notice_class=models.CharField(choices=class_choice,max_length=25)

    notice_department=models.CharField(choices=department_choice,max_length=25,null=True,blank=True)
    notice_image=models.ImageField(upload_to='images/', null=True,blank=True)
    notice_description=models.TextField(blank=True,null=True)
    notice_file=models.FileField(upload_to='uploads/', null=True,blank=True)
    notice_date=models.DateField(auto_now_add=True)
    notice_time = models.TimeField(auto_now_add=True)


class Student_Query(models.Model):
    student=models.ForeignKey(Students,on_delete=models.CASCADE,blank=True,null=True)
    teacher=models.ForeignKey(Teachers,on_delete=models.CASCADE)
    subject = models.ForeignKey(Subjects,on_delete=models.CASCADE)
    query_image=models.ImageField(upload_to="images/",blank=True,null=True)
    query_file=models.FileField(upload_to="uploads/",blank=True,null=True)
    query_description=models.TextField()
    query_date = models.DateField(auto_now_add=True)
    query_time = models.TimeField(auto_now_add=True)


# class Teacher_Message(models.Model):
#     teacher_user=models.ForeignKey(Teachers,on_delete=models.CASCADE)
#     subject = models.ForeignKey(Subjects,on_delete=models.CASCADE)
#     class_name=models.CharField(max_length=20,choices=class_choice)
#     study_image=models.ImageField(upload_to="images/",blank=True,null=True)
#     study_file=models.FileField(upload_to="uploads/",blank=True,null=True)
#     study_description=models.TextField(blank=True)
#     study_materail_date = models.DateField(auto_now_add=True)
#     study_material_time = models.TimeField(auto_now_add=True)


class Teacher_Attendance(models.Model):
    teacher=models.ForeignKey(Teachers,on_delete=models.CASCADE)
    subject=models.ForeignKey(Subjects,on_delete=models.CASCADE)
    subject_teacher=models.ForeignKey(Subject_Teacher,on_delete=models.CASCADE)
    lect_start_time=models.TimeField(null=True)
    lect_end_time=models.TimeField(null=True)

    attendance_date=models.DateField()
    status=models.CharField(max_length=200,blank=True,null=True)


class Student_Attendance(models.Model):
    teacher_attendance=models.ForeignKey(Teacher_Attendance,on_delete=models.CASCADE)
    student=models.ForeignKey(Students,on_delete=models.CASCADE)
    attendance=models.BooleanField(default=True)
