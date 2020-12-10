# Generated by Django 3.1 on 2020-09-27 03:24

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bcs', '0003_auto_20200926_0916'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='study_material',
            name='class_name',
        ),
        migrations.AddField(
            model_name='study_material',
            name='subject',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='bcs.subjects'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='exam',
            name='exam_date',
            field=models.DateField(blank=True, default=datetime.date(2020, 9, 27)),
        ),
    ]
