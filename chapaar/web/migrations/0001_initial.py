# Generated by Django 2.2 on 2019-04-07 09:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(blank=True, max_length=30)),
                ('Grade', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PhoneNumber', models.CharField(blank=True, max_length=15)),
                ('ParentPhoneNumber', models.CharField(blank=True, max_length=15)),
                ('Name', models.CharField(blank=True, max_length=30)),
                ('IsValid', models.BooleanField(default=False)),
                ('Smsactive', models.BooleanField(default=True)),
                ('Grade', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.Category')),
                ('Username', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DueDate', django_jalali.db.models.jDateField()),
                ('StudyHour', models.FloatField(blank=True)),
                ('TestNumber', models.IntegerField(blank=True)),
                ('CourseName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Course')),
                ('StudentName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Student')),
            ],
        ),
        migrations.CreateModel(
            name='Notify',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date', django_jalali.db.models.jDateField()),
                ('Subject', models.CharField(blank=True, max_length=100)),
                ('Message', models.TextField(blank=True, max_length=500)),
                ('Seen', models.BooleanField(default=False)),
                ('Receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Student')),
            ],
        ),
        migrations.CreateModel(
            name='Done',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DoneDate', django_jalali.db.models.jDateField()),
                ('StudyHour', models.IntegerField(blank=True)),
                ('TestNumber', models.IntegerField(blank=True)),
                ('CourseName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Course')),
                ('StudentName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Student')),
            ],
        ),
    ]
