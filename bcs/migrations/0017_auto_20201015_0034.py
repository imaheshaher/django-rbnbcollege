# Generated by Django 3.0.5 on 2020-10-14 19:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bcs', '0016_auto_20201015_0009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student_query',
            name='student',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='bcs.Students'),
        ),
    ]