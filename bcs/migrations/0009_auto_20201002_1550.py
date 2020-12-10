# Generated by Django 3.0.5 on 2020-10-02 10:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bcs', '0008_auto_20201002_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students',
            name='class_name',
            field=models.CharField(choices=[('All bcs', 'All bcs'), ('fy bcs', 'fy bcs'), ('sy bcs', 'sy bcs'), ('ty bcs', 'ty bcs')], max_length=20),
        ),
        migrations.AlterField(
            model_name='study_material',
            name='class_name',
            field=models.CharField(choices=[('All bcs', 'All bcs'), ('fy bcs', 'fy bcs'), ('sy bcs', 'sy bcs'), ('ty bcs', 'ty bcs')], max_length=20),
        ),
        migrations.AlterField(
            model_name='subjects',
            name='class_name',
            field=models.CharField(choices=[('All bcs', 'All bcs'), ('fy bcs', 'fy bcs'), ('sy bcs', 'sy bcs'), ('ty bcs', 'ty bcs')], max_length=20),
        ),
        migrations.CreateModel(
            name='Notice_Board',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notice_class', models.CharField(choices=[('All bcs', 'All bcs'), ('fy bcs', 'fy bcs'), ('sy bcs', 'sy bcs'), ('ty bcs', 'ty bcs')], max_length=25)),
                ('notice_image', models.ImageField(null=True, upload_to='images/')),
                ('notice_description', models.TextField(blank=True, null=True)),
                ('notice_file', models.FileField(null=True, upload_to='uploads/% Y/% m/% d/')),
                ('notice_date', models.DateField(auto_now_add=True)),
                ('notice_time', models.TimeField(auto_now_add=True)),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bcs.Teachers')),
            ],
        ),
    ]