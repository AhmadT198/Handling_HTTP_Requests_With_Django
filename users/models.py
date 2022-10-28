from django.db import models
from django.db.models.functions import Length
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

models.CharField.register_lookup(Length)

def validate_name(value):
    if (value[0] >= 'a' and value[0] <= 'z'):
        raise ValidationError(
            _('%(value)s should start with a capital letter.'),
            params={'value': value},
        )

    if not value.isalpha():
        print(value)
        raise ValidationError(
            _('%(value)s should containt only letters.'),
            params={'value': value},
        )



class Accounts(models.Model):
    username = models.CharField(max_length=50, unique=True, null=False, blank=False)
    password = models.CharField(max_length=50, null=False, blank=False)
    type = models.CharField(null=False, blank=False, choices=[("PRNT", 'Parent'), ("STUD", 'Student')], max_length=4)

    class Meta:
        db_table='Accounts'
        constraints=[
            models.CheckConstraint(check=models.Q(username__length__gte= 8), name='username_min_length',
                                   violation_error_message="Minimum 10 Characters for Username."),

            models.CheckConstraint(check=models.Q(password__length__gte=8), name='password_min_length',
                                   violation_error_message="Minimum 10 Characters for Password.")

        ]


class Parent(models.Model):
    parentID = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=50, validators=[validate_name])
    lastName = models.CharField(max_length=50, validators=[validate_name])
    email = models.EmailField(max_length=256)
    job = models.CharField(max_length=150)

    login = models.OneToOneField(Accounts, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "%s %s" % (self.firstName,self.lastName)

    class Meta:
        db_table= "parents"
        unique_together = [['firstName','lastName']]



class Subject(models.Model):
    subjectID = models.AutoField(primary_key=True)
    subjectName = models.CharField(max_length=70, unique=True)
    def __str__(self):
        return self.subjectName

    class Meta:
        db_table = "subjects"


class Student(models.Model):
    studentID = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    email = models.EmailField(max_length=256, null=True)
    grade = models.IntegerField(null=True)
    studentClass = models.IntegerField(null=True)
    age = models.IntegerField(null=True)
    parentID = models.ForeignKey(Parent, on_delete=models.CASCADE)
    subjects = models.ManyToManyField(Subject, related_name="students", null=True)

    login = models.OneToOneField(Accounts, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "%s %s" % (self.firstName,self.lastName)

    class Meta:
        db_table = 'students'
        unique_together = [['firstName','lastName']]
        constraints = [
            models.CheckConstraint(check=models.Q(age__gte=16), name="ageCheck", violation_error_message="Age Must be more than or equal 16"),
            models.CheckConstraint(check=(models.Q(studentClass__gte=1) & models.Q(studentClass__lte=12)), name="classCheck",
                                   violation_error_message="Class must be between 1 and 12"),
            models.CheckConstraint(check=(models.Q(grade__gte=0)),
                                   name="gradeCheck",
                                   violation_error_message="Student Grade must be more than Zero."),
        ]






class loginTokens(models.Model):
    token=models.CharField(null=False, unique=True, blank=True,max_length=2720)
    user=models.ForeignKey(Accounts, on_delete=models.CASCADE)

    class Meta:
        db_table = 'tokens'