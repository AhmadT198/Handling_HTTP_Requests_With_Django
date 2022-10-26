from rest_framework import serializers
from .models import *
from django.forms import ValidationError

def nameCheck(value):
    if value[0] != value[0].upper():
        raise ValidationError("Name must start with Uppercase letter.")

    if not value.isalpha():
        raise ValidationError("Name must consist of letters only.")


class SubjectListSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='subject-detail', format='html')

    class Meta:
        model = Subject
        fields = ['url']

class StudentSerializer(serializers.HyperlinkedModelSerializer):
    firstName = serializers.CharField(max_length=50, validators=[nameCheck])
    lastName = serializers.CharField(max_length=50, validators=[nameCheck])
    subjects = SubjectListSerializer(many=True)
    subjectlist = serializers.HyperlinkedRelatedField(many=True, view_name='subject-detail', read_only=True)

    class Meta:
        model = Student
        fields = ["url", "subjectlist", "firstName", "lastName", "subjects"]


class ParentSerializer(serializers.ModelSerializer):
    firstName = serializers.CharField(max_length=50, validators=[nameCheck])
    lastName = serializers.CharField(max_length=50, validators=[nameCheck])
    class Meta:
        model = Parent
        fields = "__all__"


class SubjectSerializer(serializers.ModelSerializer):

    students = StudentSerializer(many=True)
    class Meta:
        model = Subject
        fields = "__all__"
