from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.db.models import Q
from django.contrib import messages
import json
from .forms import *
import datetime
from collections import defaultdict
today_date = datetime.date.today()


def check_user(request):
    try:
        teacher = Teachers.objects.get(user=request.user)
        return teacher
    except:
        return HttpResponse("not user")


def index(request):
    return render(request, 'index.html')


def upcome_exam(request):
    return render(request, 'give_exam2.html')


def student_home(request):
    try:
        student = Students.objects.get(user=request.user)
    except:
        messages.error(request, "You are not logged in")
        return redirect("/")
    subject = Subjects.objects.filter(class_name=student.class_name)
    teacher_subject = {}
    for s in subject: 
        teacher_subject[s]=''
        t=Subject_Teacher.objects.filter(subject__id=s.id)
        if t.exists():
            teacher_subject[s]=t[0].teacher
    print(teacher_subject)
    notice_data = Notice_Board.objects.filter(
        Q(notice_class='All bcs') | Q(notice_class=student.class_name))[::-1][0:5]
    context = {
        'is_student': True,
        'student': student,
        'subject': teacher_subject,
        'notice_data': notice_data
    }
    return render(request, 'home.html', context)


def teacher_home(request):
    try:
        teacher = Teachers.objects.get(user=request.user)
    except:
        messages.error(request, "You are Not Logged in")
        return redirect('teacher_home')

    teacher_data = Subject_Teacher.objects.filter(teacher=teacher)
    notice_data = Notice_Board.objects.all()[::-1][0:5]

    context = {

        'teacher_data': teacher_data,
        'notice_data': notice_data
    }
    if request.method == 'POST':
        form = Subject_TeacherForm(request.POST)
        if form.is_valid():
            subform = form.save(commit=False)
            subform.teacher = teacher
            try:
                st = Subject_Teacher.objects.filter(
                    teacher=teacher, subject=subform.subject)[0]
                messages.success(request, "Already added this Subject")
                return redirect('teacher_home')
            except:
                subform.save()
            return redirect('teacher_home')
    else:
        form = Subject_TeacherForm()
    context['form'] = form
    return render(request, 'teacher_home.html', context)


# def exam(request):

#     question="what is the name of 1 in letter"
#     context ={
#         'que':question,
#         'op1':'one',
#         'op2':'two',
#         'op3':'three',
#         'op4':'four',
#         'true':'one'
#     }
#     if request.method=='POST':
#         ans=request.POST['r']
#         if ans==context['true']:
#             print('correct')
#         else:
#             print('incorrect')

#         return HttpResponse(ans)


#     return  render(request,'exam.html',context)

# def register_teacher(request):
#     if request.method=='POST':
#         form = UserForm(request.POST)
#         if form.is_valid():
#             password=request.POST['password']
#             user=form.save(commit=False)
#             user.set_password(password)
#             user.save()
#             user=authenticate(username=user.username,password=user.password)
#             if user is not None:
#                 auth.login(request,user)
#                 return redirect('teacher_info')


#         else:
#             return HttpResponse("Something Invalid")

#     else:
#         form = UserForm()

#     context = {
#         'form':form
#     }
#     return render(request,'register.html',context)
def register_teacher(request):
    if request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        form = UserForm(request.POST)
        teacherform = TeacherForm(request.POST)
        if form.is_valid() and teacherform.is_valid():
            password = request.POST['password']
            user = form.save(commit=False)
            user.set_password(password)
            user.save()
            t_form = teacherform.save(commit=False)
            t_form.user = user
            t_form.save()

            return redirect('login')
    else:
        form = UserForm()
        teacherform = TeacherForm()
    context = {
        'form': form,
        'dform': teacherform
    }
    return render(request, 'register.html', context)


def register_student(request):
    if request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        form = UserForm(request.POST)
        studentform = StudentForm(request.POST)
        if form.is_valid() and studentform.is_valid():
            password = request.POST['password']

            user = form.save(commit=False)
            user.set_password(password)

            user.save()
            s_form = studentform.save(commit=False)
            s_form.user = user
            s_form.save()
            #return HttpResponse(s_form.class_name)
            
            automate_attendance(request,s_form.class_name,s_form.department_name,s_form.id)
            return redirect('login')
        else:
            messages.error(request, "User Already Register")
            return redirect('register_student')
    else:
        form = UserForm()
        studentform = StudentForm()
    context = {
        'form': form,
        'dform': studentform
    }
    return render(request, 'register.html', context)


def login_user(request):
    if request.user.is_authenticated:
        try:
            find_user = Teachers.objects.get(user=request.user)
            return redirect('teacher_profile')
        except:
            find_user = Students.objects.get(user_id=request.user.id)
            return redirect('student_teacher')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            try:
                find_user = Teachers.objects.get(user_id=request.user.id)
                return redirect('teacher_home')
            except:
                find_user = Students.objects.get(user_id=request.user.id)
                return redirect('student_home')

        else:
            return HttpResponse("username or password is wrong")

    return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('index')


def teacher_profile(request):
    try:
        teacher = Teachers.objects.get(user_id=request.user.id)
    except:
        return HttpResponse("you are not teacher")
    teacher_data = Subject_Teacher.objects.filter(teacher=teacher)
    context = {

        'teacher_data': teacher_data,
        'teacher': teacher
    }
    if request.method == 'POST':

        form = Subject_TeacherForm(request.POST)
        context['form'] = form
        if form.is_valid():
            subform = form.save(commit=False)
            subform.teacher = teacher
            try:
                st = Subject_Teacher.objects.filter(
                    teacher=teacher, subject=subform.subject)[0]
                messages.success(request, "u already added this ")
                return redirect('teacher_profile')

            except:
                subform.save()
            # subform.save()
            return redirect('teacher_profile')

    else:
        form = Subject_TeacherForm()

    context['form'] = form

    return render(request, 'teacher_profile.html', context)


def add_question(request):
    try:
        teacher = Teachers.objects.get(user_id=request.user.id)
    except:
        return HttpResponse("you are not teacher")

    if request.method == 'POST':
        qform = QuestionForm(request.POST)
        ansform = AnswerForm(request.POST)

        if qform.is_valid() and ansform.is_valid():
            q = qform.save(commit=False)
            q.teacher = teacher
            q.save()
            ans = ansform.save(commit=False)
            ans.question = q
            ans.save()
            return HttpResponse("question added")

    else:
        qform = QuestionForm()
        ansform = AnswerForm()

    context = {
        'qform': qform,
        'ansform': ansform
    }
    return render(request, 'add_question.html', context)


def add_question_answer(request, sid):
    try:
        question_data = "no question"
        teacher = Teachers.objects.get(user_id=request.user.id)
        subject = Subjects.objects.get(id=sid)
        exam_date = datetime.date.today()
        examid = Exam.objects.get(
            teacher=teacher, subject=subject, post_exam=False)
        question_data = Question_Answer.objects.filter(exam=examid)
    except:
        return HttpResponse("you are not teacher Or You may be add at list one question to take exam")

    if request.method == 'POST':
        form = Question_AnswerForm(request.POST)

        if form.is_valid():

            qform = form.save(commit=False)
            x = request.POST['correct_answer']
            if x == 'A':
                x = request.POST['option_1']
            elif x == 'B':
                x = request.POST['option_2']
            elif x == 'C':
                x = request.POST['option_3']
            elif x == 'D':
                x = request.POST['option_4']
            else:
                return HttpResponse("somthing went wrong")

            qform.correct_answer = x
            qform.exam = examid
            qform.save()

            context = {
                'qform': qform,
                'question_data': question_data,
                'exam': examid,
                'subject': subject

            }
            return render(request, "add_question.html", context)

        else:
            messages.error(request, "You Should be Add Question Properly")
            return redirect('add_question', sid)

    else:
        qform = Question_AnswerForm()

    context = {
        'qform': qform,
        'question_data': question_data,
        'exam': examid,
        'subject': subject

    }
    return render(request, 'add_question.html', context)


def teacher_student(request):
    try:
        teacher = Teachers.objects.get(user_id=request.user.id)
    except:
        return HttpResponse("you are not teacher")

    teacher_data = Subject_Teacher.objects.filter(teacher=teacher)

    context = {
        'teacher_data': teacher_data
    }
    return render(request, 'teacher_student.html', context)


def student_teacher(request):
    try:
        student = Students.objects.get(user=request.user)
        class_name = student.class_name
    except:
        messages.error(request, "u are not logged in")
        return redirect('index')

    upcoming_exam = Exam.objects.filter(
        subject__class_name=class_name, exam_status=False).order_by('exam_date')
    # previous_exam=Exam.objects.filter(subject__class_name=class_name,post_exam=True,exam_status=True)

    context = {
        'exam': upcoming_exam,
        'is_student': True
    }
    # context = {}
    # subject_list={}
    # exam_list=[]
    # subject_data=Subjects.objects.filter(class_name=class_name)
    # print(subject_data)
    # for s in subject_data:

    #     t=Subject_Teacher.objects.filter(subject=s)[0]
    #     subject_list[s]=t.teacher

    #     #subject_list.append(s.subject_name)

    # exam_date=datetime.date.today()
    # for slist in subject_list:
    #     prev_exam=Exam.objects.filter(~Q(exam_date=today_date),subject__subject_name=slist,post_exam=True).order_by('-exam_date')
    #     try:
    #         exam_data=Exam.objects.filter(subject__subject_name=slist,post_exam=True)
    #         exam_list.append(exam_data)
    #     except:
    #         pass
    # print(exam_list)
    # context = {
    #     'subject_data':subject_data,
    #     'exam_data':exam_list,
    #     'class_name':class_name,
    #     'subject_teacher':subject_list,
    #     'prev_exam':prev_exam
    # }
    return render(request, 'upcoming_exam.html', context)


def take_exam(request, sid):

    try:
        teacher = Teachers.objects.get(user__id=request.user.id)

    except:
        return HttpResponse("you are not teacher")
    try:
        subject = Subjects.objects.get(id=sid)
    except:
        return HttpResponse("not subject fond")
    exam_date = datetime.date.today()

    current_exam_data = Exam.objects.filter(
        teacher=teacher, subject=subject, exam_status=False)
   # exam_data=Exam.objects.get_or_create(teacher=teacher,subject=subject,post_exam=False)
    # exam_data.save()

    # question_data=Question_Answer.objects.filter(teacher=teacher)
    context = {
        # 'question_data':question_data,
        'subject': subject.id,
        'current_exam': current_exam_data
    }
    return render(request, 'exam_detail.html', context)


def create_new_exam(request, sid):
    try:
        teacher = Teachers.objects.get(user=request.user)
        subject = Subjects.objects.get(id=sid)
        subject_teacher = Subject_Teacher.objects.get(
            subject=subject, teacher=teacher)
    except:
        messages.error(request, "Your are Not Logged in")
        return redirect('teacher_home')

    exam = Exam.objects.filter(
        teacher=teacher, subject=subject, post_exam=False)
    if exam.exists():
        exam_exist = True
        messages.success(
            request, "Exam is Already Created You can Update Exam Detail Or Add Question")
    else:
        exam_exist = False
    new_exam = Exam.objects.get_or_create(
        teacher=teacher, subject=subject, post_exam=False)

    obj = get_object_or_404(Exam, id=new_exam[0].id)
    examform = ExamForm(request.POST or None, instance=obj)
    if examform.is_valid():
        try:
            examform.save()
            return redirect('take_exam', subject.id)
        except:
            messages.error(request, "All Field Required")
            return redirect('create_new_exam', subject.id)

    context = {
        'examform': examform,
        'new_exam': new_exam[0],
        'exam_exist': exam_exist
    }

    return render(request, 'teacher_exam_detail.html', context)


def end_exam(request, eid):
    teacher = check_user(request)
    if teacher:
        Exam.objects.filter(id=eid, teacher=teacher,
                            post_exam=True).update(exam_status=True)
        return redirect('teacher_exam')


def check_ajax(request):
    if request.method == 'POST':
        data = request.GET.get('userdata')
        
    return render(request, 'ajax_test.html')


def add_student_result(sid, eid):
    marks = 0
    exam = Exam.objects.get(id=eid)
    student = Students.objects.get(id=sid)
    sresult_data = Student_Result.objects.filter(student=student, exam=exam)
    qresult_data = Question_Answer.objects.filter(exam=exam)
    # for qr in qresult_data:
    #     for sr in sresult_data:
    #         if qr.id==sr.question.id and qr.correct_answer == sr.student_answer:
    #             mark=+1
    for r in qresult_data:
        for sr in sresult_data:
            if sr.student_answer == r.correct_answer and r.id == sr.question.id:

                marks += 1
    Student_Mark.objects.get_or_create(
        exam=exam, student=student, student_mark=marks, out_of_mark=len(qresult_data))

    return 'added'


def student_exam_data(request):

    data = request.GET.get('userdata')

    a = json.loads(data)
    # id=Students.objects.get(user__id=request.user.id)

    for i in a:
        student = Students.objects.get(user__id=i['student_id'])
        exam = Exam.objects.get(id=i['exam_id'])
        question = Question_Answer.objects.get(id=i['question_id'])
        student_answer = i['option']

        dataexist = Student_Result.objects.filter(
            student=student, exam=exam, question=question)
        if dataexist.exists():
            messages.success(request, "Someone Given Your Exam")
            return redirect('index')

        try:
            exam_end = Exam.objects.get(id=exam.id, exam_status=True)
            return HttpResponse("This Exam is End..")
        except:
            pass
        rdata = Student_Result.objects.get_or_create(
            student=student, exam=exam, question=question, student_answer=student_answer)
        # rdata.save()
    add_student_result(student.id, exam.id)
    a = {'status': 0}
    return HttpResponse(json.dumps(a), content_type='application/json')


def give_exam(request, eid):
    try:
        student = Students.objects.get(user__id=request.user.id)
        exam = Exam.objects.get(id=eid)
    except:
        return HttpResponse("you are not student")

    try:
        student_result = Student_Result.objects.filter(
            student=student, exam=exam)[0]
        
        return redirect('calculate_result', student.id, eid)
    except:
        pass
    question_data = Question_Answer.objects.filter(exam=exam)

    context = {
        'question_data': question_data,
        'exam': exam
    }

    return render(request, "give_exam.html", context)


def calculate_result(request, eid, sid=None):
    marks = 0
    try:
        student = Students.objects.get(user__id=request.user.id)
        exam = Exam.objects.get(id=eid)
        student_result = Student_Result.objects.filter(
            student=student, exam=exam)[0]
    except:
        try:
            teacher = Teachers.objects.get(user=request.user)
            exam = Exam.objects.get(id=eid)
            student = Students.objects.get(id=sid)
            
            student_result = Student_Result.objects.filter(
                student__id=sid, exam=exam)[0]
        except:
            return HttpResponse("This Exam will be Ended by teacher or You Should Not Submitted Exam")
    qresult_data = Question_Answer.objects.filter(exam=exam)
    student_result_data = Student_Result.objects.filter(
        student=student, exam=exam)
    

    newrdict = {}

    for r in qresult_data:
        newrdict[r] = {'correct_answer': r.correct_answer,
                       'student_answer': ''}
    for sr in student_result_data:
        newrdict[sr.question]['student_answer'] = sr.student_answer

    for r in qresult_data:
        for sr in student_result_data:
            if sr.student_answer == r.correct_answer and r.id == sr.question.id:

                marks += 1

    mdata = {'marks': marks, 'outof': len(qresult_data)}

    context = {
        'student_result': student_result_data,
        'result_data': qresult_data,
        'marks': mdata,
        'sresult_data': newrdict,
        'exam': exam,
        'student': student
    }

    return render(request, 'student_exam_result.html', context)


def show_student(request, sid):
    try:
        teacher = Teachers.objects.get(user__id=request.user.id)
        subject = Subjects.objects.get(id=sid)
        teacher_subject=Subject_Teacher.objects.get(teacher=teacher,subject=subject)
    except:
        return HttpResponse("u are not teacher")

    department = subject.department_name

    student_data = Students.objects.filter(
        department_name=department, class_name=subject.class_name)

    context = {
        'student_data': student_data,
        'subject': subject,
        'teacher_subject':teacher_subject
    }

    return render(request, 'students.html', context)


# def post_exam(request,eid):
#     teacher=Teachers.objects.get(user__id=request.user.id)
#     exam=Exam.objects.get(id=eid)
#     e=Exam.objects.filter(id=eid,teacher=teacher).update(post_exam=True)


#     return HttpResponse("exam conducted")


def teacher_exam_pannel(request, eid):
    try:
        teacher = Teachers.objects.get(user__id=request.user.id)
        exam = Exam.objects.get(id=eid)
    except:
        return HttpResponse("You are not teacher")

    question_data = Question_Answer.objects.filter(exam=exam)

    context = {
        'question_data': question_data,
        'exam': exam
    }

    return render(request, 'teacher_exam_pannel.html', context)


def update_question(request, eid, qid):
    try:
        teacher = Teachers.objects.get(user__id=request.user.id)

        exam = Exam.objects.get(id=eid, teacher=teacher)

    except:
        return HttpResponse("You are not teacher")
    context = {}
    obj = get_object_or_404(Question_Answer, id=qid)
    form = Question_AnswerForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('add_question', obj.exam.subject.id)
    context["form"] = form

    return render(request, 'update_question.html', context)


def delete_question(request, eid, qid):
    try:
        teacher = Teachers.objects.get(user__id=request.user.id)

        e = Exam.objects.get(id=eid, teacher=teacher)

    except:
        return HttpResponse("You are not teacher")

    obj = get_object_or_404(Question_Answer, id=qid)
    obj.delete()
    return redirect('add_question', obj.exam.subject.id)


def cancel_exam(request, eid):
    try:
        teacher = Teachers.objects.get(user__id=request.user.id)
        e = Exam.objects.filter(teacher=teacher, id=eid)
    except:
        return HttpResponse("Something went wrong")
    e.delete()
    return redirect('teacher_exam')


def post_exam(request, eid):
    try:
        teacher = Teachers.objects.get(user__id=request.user.id)
        e = Exam.objects.filter(teacher=teacher, id=eid)

        q = Question_Answer.objects.filter(exam__id=e[0].id)[0]

    except:
        return HttpResponse("You must be add at least one question")
    e.update(post_exam=True)
    return redirect('teacher_exam')


def previous_exam(request, sid):
    try:
        teacher = Teachers.objects.get(user__id=request.user.id)
        subject = Subjects.objects.get(id=sid)
        # subject=Subject_Teacher.objects.filter(id=sid,teacher=teacher)
    except:
        return HttpResponse("Something went wrong")
    exam = Exam.objects.filter(teacher=teacher, subject=subject,
                               post_exam=True, exam_status=True).order_by('-exam_date')[::-1]
    if len(exam) > 0:
        exam_subject = exam[0].subject
    else:
        exam_subject = subject
    context = {
        'previous_exam': exam,
        'subject': exam_subject
    }
    return render(request, 'previous_exam.html', context)


def all_student_result(request, eid):
    try:
        teacher = Teachers.objects.get(user__id=request.user.id)
        exam = Exam.objects.get(id=eid)
    except:
        return HttpResponse("not yet it something wrong")
    student_result = Student_Mark.objects.filter(exam=exam)
    slist = []
    qanslen = Question_Answer.objects.filter(exam=exam).count()

    out_of = qanslen
    for s in student_result:
        slist.append(s.student.id)
        out_of = s.out_of_mark
    not_attempt_student = Students.objects.filter(
        ~Q(id__in=slist), class_name=exam.subject.class_name)
    context = {

        'student_result': student_result,
        'not_attempt_student': not_attempt_student,
        'out_of_mark': out_of,
        'exam': exam
    }
    return render(request, 'all_student_result.html', context)


def delete_subject(request, stid):
    try:
        teacher = Teachers.objects.get(user__id=request.user.id)
        subject_teacher = Subject_Teacher.objects.get(id=stid, teacher=teacher)
    except:
        return redirect('teacher_profile')

    subject_teacher.delete()

    return redirect('teacher_profile')


def take_another_exam(request):
    try:
        teacher = Teachers.objects.get(user__id == request.user.id)
    except:
        return HttpResponse("You are not teacher")


def dict_data(request):
    data = {}
    data[1] = {'correct': 'mahesh', 'stud': 'aher'}
    data[2] = {'correct': 'shbu', 'stud': ''}

    context = {
        'data': data
    }
    return render(request, 'dict_data.html', context)


# New Functions

def upcoming_exam(request):
    try:
        student = Students.objects.get(user=request.user)
        class_name = student.class_name
    except:
        messages.error(request, "You are not logged in")
        return redirect("upcoming_exam")


def teacher_exam(request):
    try:
        teacher = Teachers.objects.get(user=request.user)
    except:
        messages.error(request, "You are Not Logged in")
        return redirect('teacher_home')
    teacher_data = Subject_Teacher.objects.filter(teacher=teacher)
    context = {
        'teacher_data': teacher_data
    }
    return render(request, 'teacher_exam.html', context)


def student_previous_exam(request):
    try:
        student = Students.objects.get(user=request.user)
        class_name = student.class_name

    except:
        messages.error(request, "You are not logged in")
        return redirect('student_home')
    pre_exam = Exam.objects.filter(
        subject__class_name=class_name, exam_status=True)

    context = {
        'pre_exam': pre_exam
    }

    return render(request, 'student_previous_exam.html', context)


def study_material(request, sid):

    try:
        teacher = Teachers.objects.get(user=request.user)
        subject = Subjects.objects.get(id=sid)
    except:
        messages.error(request, "Your are not logged in ")
        return redirect('/')
    study_data = Study_material.objects.filter(
        teacher_user=teacher, class_name=subject.class_name, subject=subject)[::-1]
    context = {
        "study_data": study_data,
        "subject": subject
    }
    if request.method == "POST":

        form = Study_MaterailForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save(commit=False)
            f.teacher_user = teacher
            f.class_name = subject.class_name
            f.subject = subject
            f.save()
            return redirect('study_material', subject.id)

        else:
            return HttpResponse("something wrong")
    else:
        form = Study_MaterailForm()

    context["form"] = form
    return render(request, "t_study_material.html", context)


def show_study_material(request, sid):
    try:
        student = Students.objects.get(user=request.user)
        subject = Subjects.objects.get(id=sid)
    except:
        messages.error(request, "You are not logged in")
        return redirect('/bcs')
    study_data = Study_material.objects.filter(
        subject=subject)[::-1]
    if len(study_data) > 0:
        teacher = study_data[0].teacher_user
    else:
        teacher = None
    # subject_teacher=Subject_Teacher.objects.get(teacher=)
    context = {
        "study_data": study_data,
        "subject": subject,
        "teacher": teacher
    }
    return render(request, "s_study_material.html", context)


def teacher_notice(request):
    try:
        teacher = Teachers.objects.get(user=request.user)
    except:
        messages.error(request, "You are Not Logged in")
        return redirect('/')

    if request.method == 'POST':
        form = Notice_BoardForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save(commit=False)
            f.teacher = teacher
            f.save()
            return redirect("teacher_home")

        else:
            return HttpResponse("form valid is not valid")
    else:
        form = Notice_BoardForm()

    context = {
        'form': form
    }
    return render(request, "t_notice.html", context={'form': form})


def delete_notice(request, nid):
    try:
        teacher = Teachers.objects.get(user=request.user)
        notice = Notice_Board.objects.get(id=nid, teacher=teacher)

    except:
        
        messages.error(request, "You are Not Logged in")
        return redirect('/bcs')
    notice.delete()
    messages.success(request, "Notice Deleted")
    

    return redirect("teacher_home")


def delete_study_material(request, stdmid):
    try:
        teacher = Teachers.objects.get(user=request.user)
        material = Study_material.objects.get(id=stdmid, teacher_user=teacher)

    except:
    
        messages.error(request, "You are Not Logged in")
        return redirect('/bcs')
    sid = material.subject.id
    
    material.delete()
    messages.success(request, "Deleted")

    return redirect("study_material", sid)


def student_query(request, tid, sid):
    try:

        subject = Subjects.objects.get(id=sid)
        teacher = Teachers.objects.get(id=tid)
        sub_teacher = Subject_Teacher.objects.get(
            subject=subject, teacher=teacher)

    except:
        messages.error(request, "You are not logged in")
        return redirect('/bcs')

    try:
        student = Students.objects.get(user=request.user)
        student_status = True
    except:
        student_status = False
    if request.method == 'POST':
        form = Student_QueryForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save(commit=False)
            if student_status:
                f.student = student
            f.teacher = teacher
            f.subject = subject
            f.save()
            return redirect('student_query', tid, sid)
        else:
            messages.error(request, "form not valid")
            return redirect("/bcs")
    else:
        form = Student_QueryForm()
    if student_status:
        query = Student_Query.objects.filter(subject=subject)[::-1]
    else:
        query = Student_Query.objects.filter(
            teacher=teacher, subject=subject)[::-1]

    context = {
        'form': form,
        'query_data': query,
        'subject': subject,
        'student_status': student_status
    }

    return render(request, 'student_query.html', context)


# filter subject
def teacher_info(request):
    try:
        teacher=Teachers.objects.get(user__id=request.user.id)
        subject_teacher=Subject_Teacher.objects.filter(teacher=teacher)
    except:
        return HttpResponse("not teacher")

    if request.method=='POST':
        form=Subject_TeacherForm(request.POST)

        if form.is_valid():
            subform=form.save(commit=False)
            subform.teacher=teacher
            try:
                st = Subject_Teacher.objects.filter(
                    teacher=teacher, subject=subform.subject)[0]
                messages.success(request, "Already added this Subject")
                return redirect('teacher_home')
            except:
                subform.save()
            return redirect('teacher_home')
            
        else:
            return HttpResponse("not valid")
    else:
        form=Subject_TeacherForm()

    context = {
        'form':form,
        'subjcet':subject_teacher
    }

    return render(request,'teacher_info.html',context)


def get_subject(request):
    class_name = request.GET.get('class_name')
    dept_name = request.GET.get('dept_name')
    
    subject_name = Subjects.objects.filter(
        class_name=class_name, department_name=dept_name)
    
    return render(request, 'subject_list.html', {'subject_name': subject_name})


def aboutus(request):
    return render(request, 'partial/aboutus.html')


def help(request):
    return render(request, 'partial/help.html')



def attendance(request,sid):
    try:
        teacher=Teachers.objects.get(user=request.user)
        subject_teacher=Subject_Teacher.objects.get(id=sid)
    except:
        return HttpResponse("You are not teacher")
    context={
        'st':subject_teacher
    }
  
    return render(request,'teacher_attendance.html',context)
    
def student_attendance(request,sid,tat_id):
    try:
        teacher = Teachers.objects.get(user__id=request.user.id)
        subject = Subjects.objects.get(id=sid)
        teacher_subject=Subject_Teacher.objects.get(teacher=teacher,subject=subject)
        teacher_attend=Teacher_Attendance.objects.get(id=tat_id,subject=subject,subject_teacher=teacher_subject)
    except:
        return HttpResponse("u are not teacher")

    department = subject.department_name

    student_data = Students.objects.filter(
        department_name=department, class_name=subject.class_name).order_by('roll_no')

    context = {
        'student_data': student_data,
        'subject': subject,
        'teacher_subject':teacher_subject,
        'teacher_attendance':teacher_attend
    }

    return render(request, 'student_attendance.html', context)


def teacher_attendance(request,tat_id=None):
    if request.method=='POST':

        start_time=request.POST['start_time']
        end_time=request.POST['end_time']
        date=request.POST['attendance_date']
        status=request.POST['status']
        st=request.POST['subject_teacher']
        subject=request.POST['subject_id']
        try:
            sub_teacher=Subject_Teacher.objects.get(id=st)
            sub=Subjects.objects.get(id=subject)
            teacher=Teachers.objects.get(user=request.user)
            try:
                tattend=Teacher_Attendance.objects.get(id=tat_id)

                tattend.lect_start_time
                tattend.lect_end_time
                tattend.status
                tattend.save()
            except:
                
                tattend=Teacher_Attendance.objects.create(teacher=teacher,subject=sub,subject_teacher=sub_teacher,lect_start_time=start_time,lect_end_time=end_time,attendance_date=date,status=status)
                tattend.save()
        except:
            return HttpResponse("Data not found.. Please Check form is filled correctly")
    else:
        return HttpResponse("something wrong")

    return redirect('student_attendance',sub.id,tattend.id)



def take_attendance(request,sid,tat_id):
    try:
        teacher = Teachers.objects.get(user__id=request.user.id)
        subject = Subjects.objects.get(id=sid)
        teacher_attendance=Teacher_Attendance.objects.get(id=tat_id)
        department = subject.department_name
    except:
        return HttpResponse("You should not be teacher")

    student_data = Students.objects.filter(
        department_name=department, class_name=subject.class_name)
    if request.method=='POST':
        attend=request.POST.get('attendance')
        for i in student_data:
            pid=str(i.id)
            status=request.POST.get(pid)
            print("status",status)
            if status=='present':
                status=True
            else:
                status=False
            
            try:
                stud=Student_Attendance.objects.get(teacher_attendance=teacher_attendance,student=i)
                stud.attendance=status
                stud.save()
            except:
                stud_attend=Student_Attendance.objects.create(teacher_attendance=teacher_attendance,student=i,attendance=status)
        return redirect('attendance_report',sid,teacher_attendance.id)
    return HttpResponse('None is none')


def attendance_report(request,sid,tat_id):
    try:
        teacher = Teachers.objects.get(user__id=request.user.id)
        subject = Subjects.objects.get(id=sid)
        teacher_subject=Subject_Teacher.objects.get(teacher=teacher,subject=subject)
        teacher_attend_data=Teacher_Attendance.objects.get(id=tat_id)
        student_attend_data=Student_Attendance.objects.filter(teacher_attendance=teacher_attend_data)
        
    except:
        return HttpResponse("u are not teacher")

    department = subject.department_name

    student_data = Students.objects.filter(
        department_name=department, class_name=subject.class_name).order_by('roll_no')
    
    present=Student_Attendance.objects.filter(teacher_attendance=tat_id,attendance=True).count()
    absent=Student_Attendance.objects.filter(teacher_attendance=tat_id,attendance=False).count()
    if present+absent==0:
        total_student=False
    else:
        total_student=present+absent
    context = {
        'student_data': student_data,
        'subject': subject,
        'teacher_subject':teacher_subject,
        'teacher_attendance_data':teacher_attend_data,
        'student_attendance_data':student_attend_data,
        'present':present,
        'absent':absent,
        'total':total_student
    }

    return render(request, 'student_attendance_report.html', context)


def cancel_attendance(request,tat_id):
    try:
        teacher=Teachers.objects.get(user=request.user)
        teacher_attendance=Teacher_Attendance.objects.get(id=tat_id,teacher=teacher)
        teacher_attendance.delete()
        return redirect('teacher_profile')
    except:
        return HttpResponse("Something wrong")


    
def attendance_detail(request,sid):
    try:
        teacher=Teachers.objects.get(user=request.user)
        subject=Subjects.objects.get(id=sid)
        attendance_data=Teacher_Attendance.objects.filter(teacher=teacher,subject=subject)
    except:
        return HttpResponse("Something Went Wrong")
    atten_list=[]
    for attend in attendance_data:
        dict={}
        tat_id=attend.id
        present=Student_Attendance.objects.filter(teacher_attendance=attend,attendance=True).count()
        absent=Student_Attendance.objects.filter(teacher_attendance=attend,attendance=False).count()
        dict[tat_id]=[present,absent]
        atten_list.append(dict)
    
    context= {
        'attendance_data':attendance_data,
        'attend_list':atten_list
    }

    return render(request,'attendance_detail.html',context)



def update_attendance(request,tat_id):
    teacher=check_user(request)
    teacher_attendance=Teacher_Attendance.objects.get(id=tat_id)
    
    obj=get_object_or_404(Teacher_Attendance,id=tat_id)

    form=Teacher_Attendance_Form(request.POST or None ,instance=obj)
    try:
        stud=Students.objects.filter(department_name=teacher_attendance.subject.department_name,class_name=teacher_attendance.subject.class_name).order_by('roll_no')
        stud_attend=Student_Attendance.objects.filter(teacher_attendance=teacher_attendance)

    except:
        return HttpResponse("Something went wrong")
    if request.method=='POST':
        if form.is_valid():
            form.save()
            return HttpResponse("Updated")

    context={
        
        'form':form,
        'stud':stud,
        'stud_attend':stud_attend,
        'tat_id':tat_id,
        'sub_id':teacher_attendance.subject.id
    }
    return render(request,'update_attendance.html',context)



def attendance_month(request):
    try:
        teacher=Teachers.objects.get(user=request.user)
    except:
        messages.error(request,"You are not logged in")
        return redirect('/')
    
    if request.method=='POST' :
        start_date=request.POST['start_date']
        end_date=request.POST['end_date']
        sid=request.POST['subject_id']
    sub=Subjects.objects.get(id=sid)
    try:
        teach=Teacher_Attendance.objects.filter(subject=sub,teacher=teacher)[0]
        t=Teachers.objects.get(id=teach.teacher.id)
    except:
        return HttpResponse("No Attendance Detail Found")

    stud_attend=Student_Attendance.objects.filter(teacher_attendance__subject=sub,teacher_attendance__teacher=t,teacher_attendance__attendance_date__gte=start_date,teacher_attendance__attendance_date__lte=end_date)
    dict={}
    stud=Students.objects.filter(class_name=sub.class_name,department_name=sub.department_name)
    # print(stud)
    for i in stud_attend:
        try:
            dict[i.student].append(i.attendance)
           # print("true")
        except:
            dict[i.student]=[i.attendance]
            #print(False)

    st=defaultdict()
    name={}
    for s in stud_attend:
        st[s.teacher_attendance]=s.teacher_attendance.attendance_date
        name[s.student]=''
    stattend=[]
    for a,p in st.items():
        attend=Student_Attendance.objects.filter(teacher_attendance=a)
        stattend.append(attend)
        #print(attend)


    #print(name)

    # print(stud_attend)
    # transposed={}
    # for st in stud_attend:
    #     transposed.setdefault(st['student'],{}).update( {'student%s' % st['student']:st['attendance']})
        
    # print(transposed)
    studat=Student_Attendance.objects.filter()
    context = {
        'teach':stattend,
        'stud_attend':st,
        'name':name,
        'attendance':dict,
        'subject':sub
    }
    return render(request,'attendance_month_report.html',context)




def attendance_month_form(request,sid):
    try:
        teacher=Teachers.objects.get(user=request.user)
        subject_teacher=Subject_Teacher.objects.get(id=sid)
        subject=Subjects.objects.get(id=sid)
    except:
        return HttpResponse("You are not teacher")
    context={
        'st':subject
    }
  
    return render(request,'attendance_month_form.html',context)

def automate_attendance(request,class_name,department_name,stud):

    subject=Subjects.objects.filter(class_name=class_name,department_name=department_name)
    teach_attend=Teacher_Attendance.objects.filter(subject__in=subject)
    
    s=Students.objects.get(id=stud)
    
    for i in teach_attend:
        Student_Attendance.objects.create(teacher_attendance=i,student=s,attendance=False)
    
    print("Done it All")
    return HttpResponse("Updated")
