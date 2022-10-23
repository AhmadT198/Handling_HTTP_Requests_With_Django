from django import forms
from .models import *
from django.forms import ValidationError

def nameCheck(value):
    if value[0] != value[0].upper():
        raise ValidationError("Name must start with Uppercase letter.")

    if not value.isalpha():
        raise ValidationError("Name must consist of letters only.")


class StudentForm(forms.ModelForm):
    firstName = forms.CharField(max_length=50, validators=[nameCheck])
    lastName = forms.CharField(max_length=50, validators=[nameCheck])

    class Meta:
        model = Student
        fields = "__all__"

class ParentForm(forms.ModelForm):
    firstName = forms.CharField(max_length=50, validators=[nameCheck])
    lastName = forms.CharField(max_length=50, validators=[nameCheck])

    class Meta:
        model = Parent
        fields = "__all__"




class SubjectForm(forms.ModelForm):

    class Meta:
        model = Subject
        fields = "__all__"
