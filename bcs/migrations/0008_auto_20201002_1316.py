# Generated by Django 3.0.5 on 2020-10-02 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bcs', '0007_auto_20201002_1232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='study_material',
            name='study_material_time',
            field=models.TimeField(auto_now_add=True),
        ),
    ]
