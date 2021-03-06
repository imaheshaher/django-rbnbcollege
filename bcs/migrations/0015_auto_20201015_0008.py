# Generated by Django 3.0.5 on 2020-10-14 18:38

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bcs', '0014_auto_20201014_1257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='exam_date',
            field=models.DateField(blank=True, default=datetime.date(2020, 10, 15)),
        ),
        migrations.CreateModel(
            name='Student_Query',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query_image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('query_file', models.FileField(blank=True, null=True, upload_to='uploads/')),
                ('query_description', models.TextField(blank=True)),
                ('query_date', models.DateField(auto_now_add=True)),
                ('query_time', models.TimeField(auto_now_add=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bcs.Students')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bcs.Subjects')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bcs.Teachers')),
            ],
        ),
    ]
