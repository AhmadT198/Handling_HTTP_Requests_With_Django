from django.http import HttpRequest, JsonResponse, HttpResponse
from django.shortcuts import render
import json

from .models import Student
from django.core import serializers
from django.views import View

class SingleStudent(View):
    def get(self, request, *args, **kwargs):
        id = kwargs['id']
        data = Student.objects.filter(studentID=id)
        data = serializers.serialize( 'json',data)
        data= json.loads(data)
        data[0]['fields']['studentID'] = data[0]['pk']
        data[0] = data[0]['fields']
        return JsonResponse(data, safe=False);

    def put(elf, request, *args, **kwargs):
        id = kwargs['id']
        data = json.loads(request.body)
        student = Student.objects.get(studentID=id)
        student.firstName = data['firstName']
        student.lastName = data['lastName']
        student.age = data['age']
        student.email = data['email']
        student.studentClass = data['studentClass']
        student.save()

        print(student)
        return JsonResponse(data);

    def delete(elf, request, *args, **kwargs):
        id = kwargs['id']
        Msg = ""
        try:
            inst = Student.objects.get(studentID=id).delete()
        except Exception as e:
            Msg=str(e)
        else:
            Msg = "Deleted"


        return JsonResponse({"message":Msg});


class MultipleStudents(View):
    def get(self, request):
        data = Student.objects.all()
        print(data)
        data = serializers.serialize('json', data)

        data = json.loads(str(data));
        for student in range(len(data)):
            data[student]['fields']['studentID'] = data[student]['pk']
            data[student] = data[student]['fields']
        print(data)

        return JsonResponse(data, safe=False);

    def post(self, request):
        data = json.loads(request.body)
        print(data)
        if isinstance(data, list):
            for singleStudent in data:
                Student.objects.create(firstName=singleStudent['firstName'], lastName=singleStudent['lastName'], email=singleStudent['email'],
                                       studentClass=singleStudent['studentClass'], age=singleStudent['age'])
        else:
            Student.objects.create(firstName=data['firstName'], lastName=data['lastName'], email=data['email'],
                                   studentClass=data['studentClass'], age=data['age'])

        return JsonResponse(data, safe=False);



