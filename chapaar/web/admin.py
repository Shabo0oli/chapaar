# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Student, Todo, Course, Done,Notify,Category
# Register your models here.

from django_jalali.admin.filters import JDateFieldListFilter
import django_jalali.admin as jadmin


class TodoAdmin(admin.ModelAdmin):
    list_filter = (
        ('DueDate', JDateFieldListFilter),
    )


class DoneAdmin(admin.ModelAdmin):
    list_filter = (
        ('DoneDate', JDateFieldListFilter),
    )


admin.site.register(Todo, TodoAdmin)
admin.site.register(Done, DoneAdmin)


admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Notify)
admin.site.register(Category)
