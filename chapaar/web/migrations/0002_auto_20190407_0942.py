# Generated by Django 2.2 on 2019-04-07 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='Name',
            field=models.CharField(blank=True, max_length=40),
        ),
    ]
