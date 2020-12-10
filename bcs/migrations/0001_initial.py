# Generated by Django 3.1 on 2020-09-15 17:13

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_date', models.DateField(blank=True, default=datetime.date(2020, 9, 15))),
                ('start_time', models.TimeField(blank=True, default=datetime.time(12, 0))),
                ('end_time', models.TimeField(blank=True, default=datetime.time(1, 0))),
                ('exam_time', models.IntegerField(blank=True)),
                ('post_exam', models.BooleanField(default=False)),
                ('exam_status', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Question_Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=250)),
                ('option_1', models.CharField(max_length=250)),
                ('option_2', models.CharField(max_length=250)),
                ('option_3', models.CharField(max_length=250)),
                ('option_4', models.CharField(max_length=250)),
                ('correct_answer', models.CharField(max_length=250)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bcs.exam')),
            ],
        ),
        migrations.CreateModel(
            name='Subjects',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_name', models.CharField(max_length=20)),
                ('class_name', models.CharField(choices=[('fy bcs', 'fy bcs'), ('sy bcs', 'sy bcs'), ('ty bcs', 'ty bcs')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Teachers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_name', models.CharField(choices=[('bcs', 'bcs')], max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Subject_Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bcs.subjects')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bcs.teachers')),
            ],
        ),
        migrations.CreateModel(
            name='Study_material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.CharField(choices=[('fy bcs', 'fy bcs'), ('sy bcs', 'sy bcs'), ('ty bcs', 'ty bcs')], max_length=20)),
                ('study_image', models.ImageField(blank=True, upload_to='images/')),
                ('study_description', models.TextField(blank=True)),
                ('teacher_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bcs.teachers')),
            ],
        ),
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_name', models.CharField(choices=[('bcs', 'bcs')], max_length=20)),
                ('class_name', models.CharField(choices=[('fy bcs', 'fy bcs'), ('sy bcs', 'sy bcs'), ('ty bcs', 'ty bcs')], max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Student_Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_answer', models.CharField(max_length=250)),
                ('exam', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bcs.exam')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bcs.question_answer')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bcs.students')),
            ],
        ),
        migrations.CreateModel(
            name='Student_Mark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_mark', models.IntegerField()),
                ('out_of_mark', models.IntegerField()),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bcs.exam')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bcs.students')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=250)),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bcs.teachers')),
            ],
        ),
        migrations.AddField(
            model_name='exam',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bcs.subjects'),
        ),
        migrations.AddField(
            model_name='exam',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bcs.teachers'),
        ),
        migrations.CreateModel(
            name='Answers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=250)),
                ('correct_answer', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bcs.question')),
            ],
        ),
    ]
