# Generated by Django 3.1.4 on 2020-12-06 10:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bcs', '0026_auto_20201124_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='exam_date',
            field=models.DateField(blank=True, default=datetime.date(2020, 12, 6)),
        ),
    ]
