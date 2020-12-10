from django import forms
from django.forms import ModelForm

from .models import *
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username']


class TeacherForm(forms.ModelForm):
    class Meta:
        model=Teachers
        exclude=['user']
        fields=['department_name',]

class StudentForm(forms.ModelForm):
    class Meta:
        model=Students
        exclude=['user']
        fields=['department_name','class_name']

class Subject_TeacherForm(forms.ModelForm):
    class Meta:
        model=Subject_Teacher
        exclude=['teacher']
        fields=['subject','department_name']


class QuestionForm(forms.ModelForm):
    class Meta:
        model=Question
        exclude=['teacher']
        fields=['question_text']

class AnswerForm(forms.ModelForm):
    class Meta:
        model=Answers
        exclude=['question']
        fields=['answer','correct_answer']


    
class Question_AnswerForm(forms.ModelForm):
    class Meta:
        model=Question_Answer
        exclude=['teacher','exam']
        fields=['question_text','option_1','option_2','option_3','option_4','correct_answer']
class TimeInput(forms.TimeInput):
    input_type="time"
class DateInput(forms.DateInput):
    input_type = 'date'
class ExamForm(forms.ModelForm):
    class Meta:
        model=Exam
        fields = ['exam_date','start_time','end_time','exam_time']
        widgets = {
            'exam_date': DateInput(),
            'start_time':TimeInput(),
            'end_time':TimeInput()
        }


class Study_MaterailForm(forms.ModelForm):
    class Meta:
        model = Study_material
        exclude = ["teacher_user","subject","class_name"]
        fields = ["study_file","study_image","study_description"]
        

class Notice_BoardForm(forms.ModelForm):
    class Meta:
        model = Notice_Board
        exclude = ["teacher"]
        fields = ["notice_image","notice_class","notice_description","notice_file"]


class Student_QueryForm(forms.ModelForm):
    class Meta:
        model = Student_Query
        exclude = ["student","teacher","subject" ]
        fields = ["query_image","query_file","query_description"]




class Teacher_Attendance_Form(forms.ModelForm):
    class Meta:
        model=Teacher_Attendance
        exclude=["teacher","subject","subject_teacher"]
        fields=["lect_start_time","lect_end_time","attendance_date","status"]

        widgets={
            'lect_start_time':TimeInput(),
            'lect_end_time':TimeInput(),
            'attendance_date':DateInput()
        }