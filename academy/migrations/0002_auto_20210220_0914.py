# Generated by Django 3.1.6 on 2021-02-20 07:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='students',
        ),
        migrations.AddField(
            model_name='group',
            name='students',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Student', to='academy.student'),
        ),
        migrations.RemoveField(
            model_name='group',
            name='teacher',
        ),
        migrations.AddField(
            model_name='group',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Lecturer', to='academy.lecturer'),
        ),
        migrations.AlterField(
            model_name='lecturer',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='student',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
