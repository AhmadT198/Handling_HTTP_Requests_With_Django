from django.http import HttpRequest, JsonResponse, HttpResponse
from django.shortcuts import render
import json

from .models import Student
from django.core import serializers
from django.views import View


class SingleStudent(View):
    '''
    Class for handling HTTP Requests for the endpoint 'localhost:8000/api/<int:id>
    '''

    def get(self, request, *args, **kwargs):
        '''
        Handling GET Requests for the endpoint 'localhost:8000/api/<int:id>'
        :param request:
        :param args:
        :param kwargs:
        :return: Returns the data of the student with the provided ID as a JSON Object
        '''
        id = kwargs['id'] ## ID from URL

        try:
            data = Student.objects.filter(studentID=id) ## Reading Student DATA
            ## Making the output in the form of a JSON object
            data = serializers.serialize('json', data)
            data = json.loads(data)
            data[0]['fields']['studentID'] = data[0]['pk']
            data[0] = data[0]['fields']
        except Exception as e:
            data = {"message" : str(e)}


        return JsonResponse(data, safe=False);

    def put(elf, request, *args, **kwargs):
        '''
                Handling PUT Requests for the endpoint 'localhost:8000/api/<int:id>'
        :param request:
        :param args:
        :param kwargs:
        :return: Returns the Updated data of the student with the provided ID as a JSON Object
        '''
        id = kwargs['id']
        data = json.loads(request.body)


        try:
            ## Reading the current Data
            student = Student.objects.get(studentID=id)
            ## Updating
            student.firstName = data['firstName']
            student.lastName = data['lastName']
            student.age = data['age']
            student.email = data['email']
            student.studentClass = data['studentClass']
            student.save()
        except Exception as e:
            data = {"message" : str(e)}


        return JsonResponse(data);

    def delete(elf, request, *args, **kwargs):
        '''
                Handling DELETE Requests for the endpoint 'localhost:8000/api/<int:id>'
        :param request:
        :param args:
        :param kwargs:
        :return: Returns Message in the form of a JSON Object {"message" : Msg} , Msg contains the string "Deleted" if it succeeded or contains the Error body.
        '''
        id = kwargs['id']
        Msg = ""

        try:
            Student.objects.get(studentID=id).delete()
        except Exception as e:
            Msg = str(e)
        else:
            Msg = "Deleted"

        return JsonResponse({"message": Msg});


class MultipleStudents(View):
    '''
        Class for handling HTTP Requests for the endpoint 'localhost:8000/api/'
    '''
    def get(self, request):
        '''
            Handling GET Requests for the endpoint 'localhost:8000/api/' to Read Data from the database 'student'
        :param request:
        :return: Returns The Required Data in the form of a JSON Object
        '''

        ## Read and Put data in the form of a JSON Object
        data = Student.objects.all()
        data = serializers.serialize('json', data)
        data = json.loads(str(data));

        for student in range(len(data)):
            data[student]['fields']['studentID'] = data[student]['pk']
            data[student] = data[student]['fields']

        return JsonResponse(data, safe=False);

    def post(self, request):
        '''
                    Handling POST Requests for the endpoint 'localhost:8000/api/' and Adding sent data to the database 'student'
        :param request:
        :return: Returns the newly added Data in the form of a JSON Object
        '''

        data = json.loads(request.body)


        if isinstance(data, list): ## if the sent data is a list :
            for singleStudent in data:
                Student.objects.create(firstName=singleStudent['firstName'], lastName=singleStudent['lastName'],
                                       email=singleStudent['email'],
                                       studentClass=singleStudent['studentClass'], age=singleStudent['age'])
        else: ##if it is a single JSON Object
            Student.objects.create(firstName=data['firstName'], lastName=data['lastName'], email=data['email'],
                                   studentClass=data['studentClass'], age=data['age'])

        return JsonResponse(data, safe=False);
