# Generated by Django 4.1.2 on 2022-10-21 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('studentID', models.AutoField(primary_key=True, serialize=False)),
                ('firstName', models.CharField(max_length=50)),
                ('lastName', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=256)),
                ('studentClass', models.IntegerField()),
                ('age', models.IntegerField()),
            ],
            options={
                'db_table': 'students',
            },
        ),
    ]
