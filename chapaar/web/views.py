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
from django.db.models import Sum
from django.shortcuts import redirect



import jdatetime



from .models import *





def adminpanel(request):
    context = {}
    context['students'] = Student.objects.all()
    template = loader.get_template('app/adminpanel.html')
    return HttpResponse(template.render(context, request))


def studentInfo(student , startJdate , endJdate) :
    context = {}

    if startJdate == 0 and endJdate == 0 :
        currentDate = jdatetime.date.today()
        pastDate = jdatetime.date.today().__add__(jdatetime.timedelta(days=-7))
    else :
        currentDate = endJdate
        pastDate =  startJdate



    donat = list(Done.objects.filter(StudentName=student, DoneDate__gte=pastDate,
                                     DoneDate__lte=currentDate.__add__(jdatetime.timedelta(days=-1))).values(
        'CourseName__Name').order_by('CourseName__Name').annotate(sum=Sum('StudyHour')))
    donatTest = list(Done.objects.filter(StudentName=student, DoneDate__gte=pastDate,
                                         DoneDate__lte=currentDate.__add__(jdatetime.timedelta(days=-1))).values(
        'CourseName__Name').order_by('CourseName__Name').annotate(sum=Sum('TestNumber')))
    allTodo = list(Todo.objects.filter(StudentName=student, DueDate__gte=pastDate,
                                       DueDate__lte=currentDate.__add__(jdatetime.timedelta(days=-1))))
    allDone = list(Done.objects.filter(StudentName=student, DoneDate__gte=pastDate,
                                       DoneDate__lte=currentDate.__add__(jdatetime.timedelta(days=-1))))

    all = {}
    for done in allDone:
        all[(done.CourseName, done.DoneDate)] = (None, done)
    for todo in allTodo:
        if (todo.CourseName, todo.DueDate) in all.keys():
            (x, y) = all[(todo.CourseName, todo.DueDate)]
            all[(todo.CourseName, todo.DueDate)] = (todo, y)
        else:
            all[(todo.CourseName, todo.DueDate)] = (todo, None)

    context['all'] = all

    context['Student'] = student
    context['Courses'] = []

    context['ReportDay'] = currentDate.day
    context['ReportMonth'] = jdatetime.date.j_months_fa[currentDate.month - 1]
    context['ReportYear'] = currentDate.year

    yesterday = currentDate.__add__(jdatetime.timedelta(days=-1))

    context['ReportYesterdayDay'] = yesterday.day
    context['ReportYesterdayMonth'] = jdatetime.date.j_months_fa[yesterday.month - 1]
    context['ReportYesterdayYear'] = yesterday.year

    yesterdayTodoList = Todo.objects.filter(StudentName=student, DueDate=yesterday).order_by(
        'CourseName__id')
    yesterdayDoneList = Done.objects.filter(StudentName=student, DoneDate=yesterday).order_by(
        'CourseName__id')

    courses = Course.objects.filter(Grade=student.Grade)
    for course in courses:
        c = {}
        c['Name'] = course.Name
        c['id'] = course.id
        done = Done.objects.filter(StudentName=student, DoneDate=yesterday, CourseName=course)
        donecurrent = Done.objects.filter(StudentName=student, DoneDate=jdatetime.date.today(),
                                          CourseName=course)
        c['read'] = 0
        c['test'] = 0
        c['readcurrent'] = 0
        c['testcurrent'] = 0
        if len(done):
            c['read'] = done[0].StudyHour
            c['test'] = done[0].TestNumber
        if len(donecurrent):
            c['readcurrent'] = donecurrent[0].StudyHour
            c['testcurrent'] = donecurrent[0].TestNumber
        context['Courses'].append(c)

    isOk = 0
    if Done.objects.filter(StudentName=student, DoneDate=yesterday):
        context['readonlyYesterday'] = 'YES'
        isOk = 1

    if isOk == 0:
        yesterdayDoneList = yesterdayTodoList

    context['YesterdayList'] = zip(yesterdayTodoList, yesterdayDoneList)
    context['YesterdayList2'] = yesterdayTodoList


    context['ReportDay'] = jdatetime.date.today().day
    context['ReportMonth'] = jdatetime.date.j_months_fa[jdatetime.date.today().month - 1]
    context['ReportYear'] = jdatetime.date.today().year
    list1 = Todo.objects.filter(StudentName=student, DueDate=jdatetime.date.today()).order_by(
        'CourseName__id')
    list2 = Done.objects.filter(StudentName=student, DoneDate=jdatetime.date.today()).order_by(
        'CourseName__id')

    isOk = 0
    if Done.objects.filter(StudentName=student, DoneDate=jdatetime.date.today()):
        context['readonly'] = 'YES'
        isOk = 1

    if isOk == 0:
        list2 = list1

    list3 = zip(list1, list2)
    context['List'] = list3
    context['List2'] = list1
    day = currentDate
    context['readinghour'] = []
    context['todosHours'] = []
    context['testeddone'] = []
    context['testedtodos'] = []
    context['days'] = []
    while day != pastDate:
        day = day.__add__(jdatetime.timedelta(days=-1))
        dones = Done.objects.filter(StudentName=student, DoneDate=day)
        todos = Todo.objects.filter(StudentName=student, DueDate=day)
        todosHours = 0
        testeddone = 0
        testedtodos = 0
        readinghours = 0
        for d in dones:
            todosHours += d.StudyHour
            testedtodos += d.TestNumber
        for d in todos:
            readinghours += d.StudyHour
            testeddone += d.TestNumber
        context['days'].append(day.day)
        context['readinghour'].append(readinghours)
        context['testeddone'].append(testeddone)
        context['todosHours'].append(todosHours)
        context['testedtodos'].append(testedtodos)

    context['notseen'] = Notify.objects.filter(Receiver=student, Seen=False).count()

    context['donat'] = donat
    context['donatTest'] = donatTest

    return context

def studentpanel(request):

    student = Student.objects.get(Username=request.user)
    startJDate = 0
    endJDate = 0
    context = studentInfo(student , startJDate , endJDate)

    template = loader.get_template('app/studentpanel.html')
    return HttpResponse(template.render(context, request))

@csrf_exempt
def student(request , id):

    startJDate = 0
    endJDate = 0
    if request.method == 'POST' :
        startDate = request.POST['fromdate'].split('-')
        endDate = request.POST['todate'].split('-')
        startJDate = jdatetime.date(int(startDate[0]), int(startDate[1]), int(startDate[2]))
        endJDate = jdatetime.date(int(endDate[0]), int(endDate[1]), int(endDate[2]))


    student = Student.objects.get(id=id)
    context = studentInfo(student , startJDate , endJDate)

    template = loader.get_template('app/studentInfo.html')
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

    if 'fullname' not in msg or 'password' not in msg or 'phonenumber' not in msg or 'parentphonenumber' not in msg :
        context['message'] = 'مشخصات را به درستی وارد کنید'
        return JsonResponse(context, encoder=JSONEncoder)

    username = msg['phonenumber']
    if len(username)!=11 or username[0]!="0" or username[1]!="9" or not str(username).isdigit():
        context['message']='شماره تلفن موبایل خود را به درستی وارد کنید.به صورت اعداد انگلیسی و به فرمت 09123456789'
        return JsonResponse(context , encoder=JSONEncoder)
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
                if( not leader.IsValid ) :
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



def report(request):


    context = {}
    currentDate = jdatetime.date.today()

    context['ReportDay'] = currentDate.day
    context['ReportMonth'] = jdatetime.date.j_months_fa[ currentDate.month-1 ]
    context['ReportYear'] = currentDate.year

    yesterday = currentDate.__add__(jdatetime.timedelta(days=-1))

    context['ReportYesterdayDay'] = yesterday.day
    context['ReportYesterdayMonth'] = jdatetime.date.j_months_fa[ yesterday.month-1 ]
    context['ReportYesterdayYear'] = yesterday.year

    if request.method == "POST":
        if 'yesterday' in request.POST :
            for i in range(0, 50):
                tagName = 'readed' + str(i)
                if tagName in request.POST:
                    readed = request.POST[tagName]
                    if not readed :
                        readed = '0'
                    tested = request.POST['test' + str(i)]
                    if not tested :
                        tested = '0'
                    st = Student.objects.filter(Username=request.user)[0]
                    cr = Course.objects.filter(id=i)[0]
                    record = Done(StudentName=st, DoneDate=yesterday, CourseName=cr, StudyHour=readed,
                                  TestNumber=tested)
                    record.save()

        else :
            for i in range(0, 50):
                tagName = 'readed' + str(i)
                if tagName in request.POST:
                    readed = request.POST[tagName]
                    if not readed:
                        readed = '0'
                    tested = request.POST['test' + str(i)]
                    if not tested:
                        tested = '0'
                    st = Student.objects.filter(Username=request.user)[0]
                    cr = Course.objects.filter(id=i)[0]
                    record = Done(StudentName=st, DoneDate=jdatetime.date.today(), CourseName=cr, StudyHour=readed, TestNumber=tested)
                    record.save()
    return  studentpanel(request)

def logout(request):
    logout(request)
    return index(request)