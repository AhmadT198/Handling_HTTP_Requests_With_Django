
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.shortcuts import render
import json
from ..serializers import *
from ..forms import *
from ..models import Student
from django.core import serializers
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, mixins


class SingleStudent(generics.GenericAPIView,
                    mixins.UpdateModelMixin,  ## For PUT Request
                    mixins.DestroyModelMixin,  ## For DELETE Request
                    mixins.RetrieveModelMixin):  ## For GET Request
    '''
        Class for handling HTTP Requests for the endpoint 'localhost:8000/api/school/students/<int:pk>'
    '''
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get(self, request, *args, **kwargs):
        '''
        Handling GET Requests for the endpoint 'localhost:8000/api/school/students/<int:id>'
            Returns the data of the student with the provided ID as a JSON Object
        '''
        return self.retrieve(request, *args, *kwargs)

    def put(self, request, *args, **kwargs):
        '''
                Handling PUT Requests for the endpoint 'localhost:8000/api/school/students/<int:id>'
        Returns the Updated data of the student with the provided ID as a JSON Object
        '''
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        '''
                Handling DELETE Requests for the endpoint 'localhost:8000/api/school/students/<int:id>'
        Returns Message in the form of a JSON Object {"message" : Msg} , Msg contains the string "Deleted" if it succeeded or contains the Error body.
        '''
        return self.delete(request, *args, **kwargs)


class MultipleStudents(generics.GenericAPIView,
                       mixins.CreateModelMixin,
                       mixins.ListModelMixin
                       ):
    '''
        Class for handling HTTP Requests for the endpoint 'localhost:8000/api/school/students'
    '''

    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    def get(self, request, *args, **kwargs):
        '''
            Handling GET Requests for the endpoint 'localhost:8000/api/school/students' to Read Data from the database 'Student'
        Returns The Required Data in the form of a JSON Object
        '''

        return self.list(request, *args, **kwargs)

    def post(self, request, *arg, **kwargs):
        '''
                    Handling POST Requests for the endpoint 'localhost:8000/api/school/students' and Adding sent data to the database 'student'
        Returns the newly added Data in the form of a JSON Object
        '''

        return self.create(request, *arg, **kwargs)

