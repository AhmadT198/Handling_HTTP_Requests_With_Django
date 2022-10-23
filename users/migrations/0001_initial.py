# Generated by Django 4.1.2 on 2022-10-23 19:48

from django.db import migrations, models
import django.db.models.deletion
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('parentID', models.AutoField(primary_key=True, serialize=False)),
                ('firstName', models.CharField(max_length=50, validators=[users.models.validate_name])),
                ('lastName', models.CharField(max_length=50, validators=[users.models.validate_name])),
                ('email', models.EmailField(max_length=256)),
                ('job', models.CharField(max_length=150)),
            ],
            options={
                'db_table': 'parents',
                'unique_together': {('firstName', 'lastName')},
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('subjectID', models.AutoField(primary_key=True, serialize=False)),
                ('subjectName', models.CharField(max_length=70)),
            ],
            options={
                'db_table': 'subjects',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('studentID', models.AutoField(primary_key=True, serialize=False)),
                ('firstName', models.CharField(max_length=50)),
                ('lastName', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=256)),
                ('grade', models.IntegerField()),
                ('studentClass', models.IntegerField()),
                ('age', models.IntegerField()),
                ('parentID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.parent')),
                ('subjects', models.ManyToManyField(to='users.subject')),
            ],
            options={
                'db_table': 'students',
            },
        ),
        migrations.AddConstraint(
            model_name='student',
            constraint=models.CheckConstraint(check=models.Q(('age__gte', 16)), name='ageCheck', violation_error_message='Age Must be more than or equal 16'),
        ),
        migrations.AddConstraint(
            model_name='student',
            constraint=models.CheckConstraint(check=models.Q(('studentClass__gte', 1), ('studentClass__lte', 12)), name='classCheck', violation_error_message='Class must be between 1 and 12'),
        ),
        migrations.AddConstraint(
            model_name='student',
            constraint=models.CheckConstraint(check=models.Q(('grade__gte', 0)), name='gradeCheck', violation_error_message='Student Grade must be more than Zero.'),
        ),
        migrations.AlterUniqueTogether(
            name='student',
            unique_together={('firstName', 'lastName')},
        ),
    ]
