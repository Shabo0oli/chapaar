from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import *
from json import JSONEncoder
from django.contrib.admin.views.decorators import staff_member_required

import jdatetime



from .models import *





def adminpanel(request):
    context = {}
    context['students'] = Student.objects.all()
    template = loader.get_template('app/adminpanel.html')
    return HttpResponse(template.render(context, request))

def studentpanel(request):
    context = {}




    currentDate = jdatetime.date.today()

    context['ReportDay'] = currentDate.day
    context['ReportMonth'] = jdatetime.date.j_months_fa[currentDate.month - 1]
    context['ReportYear'] = currentDate.year

    yesterday = currentDate.__add__(jdatetime.timedelta(days=-1))

    context['ReportYesterdayDay'] = yesterday.day
    context['ReportYesterdayMonth'] = jdatetime.date.j_months_fa[yesterday.month - 1]
    context['ReportYesterdayYear'] = yesterday.year

    yesterdayTodoList = Todo.objects.filter(StudentName__Username=request.user, DueDate=yesterday).order_by(
        'CourseName__id')
    yesterdayDoneList = Done.objects.filter(StudentName__Username=request.user, DoneDate=yesterday).order_by(
        'CourseName__id')

    isOk = 0
    if Done.objects.filter(StudentName__Username=request.user, DoneDate=yesterday):
        context['readonlyYesterday'] = 'YES'
        isOk = 1

    if isOk == 0:
        yesterdayDoneList = yesterdayTodoList

    context['YesterdayList'] = zip(yesterdayTodoList, yesterdayDoneList)

    context['ReportDay'] = jdatetime.date.today().day
    context['ReportMonth'] = jdatetime.date.j_months_fa[jdatetime.date.today().month - 1]
    context['ReportYear'] = jdatetime.date.today().year
    list1 = Todo.objects.filter(StudentName__Username=request.user, DueDate=jdatetime.date.today()).order_by(
        'CourseName__id')
    list2 = Done.objects.filter(StudentName__Username=request.user, DoneDate=jdatetime.date.today()).order_by(
        'CourseName__id')

    isOk = 0
    if Done.objects.filter(StudentName__Username=request.user, DoneDate=jdatetime.date.today()):
        context['readonly'] = 'YES'
        isOk = 1

    if isOk == 0:
        list2 = list1

    list = zip(list1, list2)
    context['List'] = list
    day = jdatetime.date.today()
    context['readinghour'] = []
    context['todosHours'] = []
    context['days'] = []
    for i in range(0,7):
        day = day.__add__(jdatetime.timedelta(days=-1))
        dones = Done.objects.filter(StudentName__Username=request.user ,DoneDate=day )
        todos = Todo.objects.filter(StudentName__Username=request.user ,DueDate=day )
        todosHours = 0
        readinghours = 0
        for d in dones :
            todosHours += d.StudyHour
        for d in todos :
            readinghours += d.StudyHour
        context['days'].append(day.day)
        context['readinghour'].append(readinghours)
        context['todosHours'].append(todosHours)

    st = Student.objects.filter(Username=request.user)[0]
    context['notseen'] = Notify.objects.filter(Receiver=st, Seen=False).count()






    template = loader.get_template('app/studentpanel.html')
    return HttpResponse(template.render(context, request))


@csrf_exempt
def verify(request):
    if 'id' in request.POST :
        id = request.POST['id']
        st = Student.objects.get(id=id)
        st.IsValid = True
        st.save()
    return index(request)
# Create your views here.


def index(request):
    if request.user.is_authenticated and  request.user.is_superuser:
        return adminpanel(request)
    elif request.user.is_authenticated:
        return studentpanel(request)
    else:
        context = {}
        template = loader.get_template('home.html')
        return HttpResponse(template.render(context, request))


def gentella_html(request):
    context = {}
    # The template to be loaded as per gentelella.
    # All resource paths for gentelella end in .html.

    # Pick out the html file name from the url. And load that template.
    load_template = request.path.split('/')[-1]
    template = loader.get_template('app/' + load_template)
    return HttpResponse(template.render(context, request))



@csrf_exempt
def apiregister(request) :
    context = {}
    msg = request.POST

    if 'username' not in msg or 'fullname' not in msg or 'password' not in msg or 'phonenumber' not in msg or 'parentphonenumber' not in msg :
        context['message'] = 'مشخصات را به درستی وارد کنید'
        return JsonResponse(context, encoder=JSONEncoder)

    username = msg['username']
    Fullname = msg['fullname']
    Password = msg['password']
    Phonenumber = msg['phonenumber']
    ParentPhonenumber = msg['parentphonenumber']

    if Student.objects.filter(PhoneNumber=Phonenumber).exists() or User.objects.filter(username=username).exists():
        context['message'] = 'مشخصات وارد شده تکراری میباشد.کاربری با این مشخصات قبلا ثبت نام کرده است.'
        return JsonResponse(context, encoder=JSONEncoder)

    cat = Category.objects.get(Num = msg['grade'])
    user = User.objects.create_user(username=username, password=Password)
    user.save()
    info = Student(Username=user,  PhoneNumber=Phonenumber, Name=Fullname , ParentPhoneNumber = ParentPhonenumber , Grade=cat)
    info.save()

    context['message'] = 'ثبت نام شما با موفقیت انجام شد.شما میتوانید پس از تایید ثبت نام توسط مدیر سیستم وارد سیستم شوید'

    return JsonResponse(context, encoder=JSONEncoder)

@csrf_exempt
def apilogin(request):
    context = {}
    if 'username' in request.POST and 'password' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None :
            if Student.objects.filter(Username=user).count() >0  :
                leader = Student.objects.get(Username=user)
                if( not leader.isValid ) :
                    context['message'] = 'اکانت شما هنوز تایید نشده است'
                else :
                    login(request, user)
                    context['response'] = '200'
                    #context['request'] = request.user
                    context['message'] = 'ورود با موفقیت انجام شد'
            else:
                login(request, user)
                context['response'] = '200'
                # context['request'] = request.user
                context['message'] = 'ورود با موفقیت انجام شد'
        else:
            context['message'] ='نام کاربری یا پسورد وارد شده اشتباه میباشد'
        return JsonResponse(context, encoder=JSONEncoder)


@staff_member_required
@csrf_exempt
def settodo(request , studentid):
    context = {}
    if request.method == 'POST' :
        startDate = request.POST['date'].split('-')
        startJDate = jdatetime.date(int(startDate[0]), int(startDate[1]), int(startDate[2]))
        stid = request.POST['studentid']
        st = Student.objects.get(id=stid)
        for key in request.POST :
            if key[0]=='!' :
                val = request.POST[key]
                typ,uniq = key.split('#')
                valTest = request.POST['test#'+uniq]
                cr = Course.objects.get(id=uniq)
                record = Todo(StudentName=st, DueDate=startJDate, CourseName=cr, StudyHour=val, TestNumber=valTest)
                record.save()
        context['message'] = ' با موفقیت ذخیره شد '
    student = Student.objects.get(id=studentid)
    courses = Course.objects.filter(Grade=student.Grade)
    context['student'] = student
    context['Courses'] = courses
    template = loader.get_template('app/settodo.html')
    return HttpResponse(template.render(context, request))