from rest_framework import serializers
from .models import *
from django.forms import ValidationError



def typeCheck(value):
    if value != "STUD" and value != "PRNT":
        raise ValidationError("Invalid User Type.")
class AccountsSerializer(serializers.ModelSerializer):
    type = serializers.CharField(max_length=4, validators= [typeCheck])

    class Meta:
        model = Accounts
        fields = "__all__"



def nameCheck(value):
    if value[0] != value[0].upper():
        raise ValidationError("Name must start with Uppercase letter.")

    if not value.isalpha():
        raise ValidationError("Name must consist of letters only.")

class ParentSerializer(serializers.ModelSerializer):
    firstName = serializers.CharField(max_length=50, validators=[nameCheck])
    lastName = serializers.CharField(max_length=50, validators=[nameCheck])

    class Meta:
        model = Parent
        fields = "__all__"



class SubjectListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        fields = "__all__"

class StudentSerializer(serializers.ModelSerializer):
    firstName = serializers.CharField(max_length=50, validators=[nameCheck])
    lastName = serializers.CharField(max_length=50, validators=[nameCheck])
    subjects = SubjectListSerializer(many=True, read_only=True)

    class Meta:
        model = Student
        fields = "__all__"



class SubjectSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True, required=False)
    class Meta:
        model = Subject
        fields = "__all__"


class TokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = loginTokens
        fields = "__all__"