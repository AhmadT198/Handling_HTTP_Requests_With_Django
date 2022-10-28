# Generated by Django 4.1.2 on 2022-10-28 13:24

from django.db import migrations, models
import django.db.models.deletion
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Accounts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=50)),
                ('type', models.CharField(choices=[('PRNT', 'Parent'), ('STUD', 'Student')], max_length=4)),
            ],
            options={
                'db_table': 'Accounts',
            },
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('parentID', models.AutoField(primary_key=True, serialize=False)),
                ('firstName', models.CharField(max_length=50, validators=[users.models.validate_name])),
                ('lastName', models.CharField(max_length=50, validators=[users.models.validate_name])),
                ('email', models.EmailField(max_length=256)),
                ('job', models.CharField(max_length=150)),
                ('login', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.accounts')),
            ],
            options={
                'db_table': 'parents',
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('subjectID', models.AutoField(primary_key=True, serialize=False)),
                ('subjectName', models.CharField(max_length=70, unique=True)),
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
                ('email', models.EmailField(max_length=256, null=True)),
                ('grade', models.IntegerField(null=True)),
                ('studentClass', models.IntegerField(null=True)),
                ('age', models.IntegerField(null=True)),
                ('login', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.accounts')),
                ('parentID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.parent')),
                ('subjects', models.ManyToManyField(null=True, related_name='students', to='users.subject')),
            ],
            options={
                'db_table': 'students',
            },
        ),
        migrations.CreateModel(
            name='loginTokens',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(blank=True, max_length=2720, unique=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.accounts')),
            ],
            options={
                'db_table': 'tokens',
            },
        ),
        migrations.AddConstraint(
            model_name='accounts',
            constraint=models.CheckConstraint(check=models.Q(('username__length__gte', 8)), name='username_min_length', violation_error_message='Minimum 10 Characters for Username.'),
        ),
        migrations.AddConstraint(
            model_name='accounts',
            constraint=models.CheckConstraint(check=models.Q(('password__length__gte', 8)), name='password_min_length', violation_error_message='Minimum 10 Characters for Password.'),
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
        migrations.AlterUniqueTogether(
            name='parent',
            unique_together={('firstName', 'lastName')},
        ),
    ]
