# Generated by Django 3.0.5 on 2020-11-18 16:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bcs', '0023_auto_20201022_1949'),
    ]

    operations = [
        migrations.AddField(
            model_name='students',
            name='roll_no',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='exam',
            name='exam_date',
            field=models.DateField(blank=True, default=datetime.date(2020, 11, 18)),
        ),
    ]
