from django.db import models

class Student(models.Model):
    studentID = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    email = models.EmailField(max_length=256)
    studentClass = models.IntegerField()
    age = models.IntegerField()

    # def __str__(self):
    #     return self.firstName + " " + self.lastName
    class Meta:
        db_table = 'students'
