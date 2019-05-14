from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django_jalali.db import models as jmodels


# Create your models here.


class Category(models.Model):
    Name = models.CharField(max_length=50)
    Num = models.CharField(max_length=10)

    def __str__(self):
        return "{}".format(self.Name)


class Student(models.Model):
    Username = models.OneToOneField(User, on_delete=models.CASCADE)
    PhoneNumber = models.CharField(max_length=15, blank=True)
    ParentPhoneNumber = models.CharField(max_length=15, blank=True)
    #Avatar = models.ImageField(upload_to='web/static/avatar/', default='web/static/avatar/default.png')
    Name = models.CharField(max_length=40, blank=True)
    IsValid = models.BooleanField(default=False)
    Smsactive = models.BooleanField(default=True)
    Grade = models.ForeignKey(Category, blank=True, null=True , on_delete=models.CASCADE)

    def __str__(self):
        return "{}".format(self.Name)


class Course(models.Model) :
    Name = models.CharField(max_length=30, blank=True)
    Grade = models.ForeignKey(Category, blank=True, null=True, on_delete=models.CASCADE)

    def __unicode__(self):
        return "{}".format(self.Name)


class Todo(models.Model):
    objects = jmodels.jManager()
    StudentName = models.ForeignKey(Student, on_delete=models.CASCADE)
    DueDate = jmodels.jDateField()
    CourseName = models.ForeignKey(Course, on_delete=models.CASCADE)
    StudyHour = models.FloatField(blank=True)
    TestNumber = models.IntegerField(blank=True)

    def __unicode__(self):
        return "{} : {}".format(self.StudentName, self.CourseName)


class Done(models.Model):
    objects = jmodels.jManager()
    StudentName = models.ForeignKey(Student, on_delete=models.CASCADE)
    DoneDate = jmodels.jDateField()
    CourseName = models.ForeignKey(Course, on_delete=models.CASCADE)
    StudyHour = models.IntegerField(blank=True)
    TestNumber = models.IntegerField(blank=True)

    def __unicode__(self):
        return "{} : {}".format(self.StudentName, self.CourseName)


class Notify(models.Model):
    objects = jmodels.jManager()
    Receiver = models.ForeignKey(Student, on_delete=models.CASCADE)
    Date = jmodels.jDateField()
    Subject = models.CharField(max_length=100, blank=True)
    Message = models.TextField(max_length=500, blank=True)
    Seen = models.BooleanField(default=False)

    def __unicode__(self):
        return "{} : {}".format(self.Receiver, self.Subject)
