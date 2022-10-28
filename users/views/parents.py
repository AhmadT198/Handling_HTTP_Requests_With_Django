
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.shortcuts import render
import json

from ..permissions import *
from ..serializers import *
from ..forms import *
from ..models import Student
from django.core import serializers
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, mixins


class SingleParent(APIView):
    '''
    Class for handling HTTP Requests for the endpoint 'localhost:8000/api/<int:id>
    '''
    authentication_classes = [SessionAuth]
    permission_classes = [UserPermission]
    def get(self, request, *args, **kwargs):
        '''
            Handling GET Requests for the endpoint 'localhost:8000/api/school/parents/<int:id>'
        Returns the data of the student with the provided ID as a JSON Object
        '''
        id = kwargs['pk']  ## ID from URL

        try:
            data = ParentSerializer(Parent.objects.get(parentID=id))
            return Response(data.data)
        except Parent.DoesNotExist:  ## Handling Error
            return Response(status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        '''
                Handling PUT Requests for the endpoint 'localhost:8000/api/school/parents/<int:id>'
        Returns the Updated data of the student with the provided ID as a JSON Object
        '''
        id = kwargs['pk']  ## Extracting ID

        data = ParentSerializer(data=request.data, instance=Parent.objects.get(parentID=id))
        if data.is_valid():
            data.save()
            return Response(data.data)
        else:
            return Response(data.errors)


    def delete(self, request, *args, **kwargs):
        '''
                Handling DELETE Requests for the endpoint 'localhost:8000/school/parents/<int:id>'
        Returns Message in the form of a JSON Object {"message" : Msg} , Msg contains the string "Deleted" if it succeeded or contains the Error body.
        '''

        id = kwargs['pk']

        try:

            accId = ParentSerializer(Parent.objects.get(parentID=id)).data['login']
            Accounts.objects.get(id=accId).delete()

            return Response("Deleted!")
        except Parent.DoesNotExist:
            return Response("Not Found")


class MultipleParents(APIView):
    '''
        Class for handling HTTP Requests for the endpoint 'localhost:8000/api/school/parents'
    '''
    authentication_classes = [SessionAuth]
    permission_classes = [UserPermission]

    def get(self, request):
        '''
            Handling GET Requests for the endpoint 'localhost:8000/api/school/parents' to Read Data from the database 'Parent'
        Returns The Required Data in the form of a JSON Object
        '''

        ## Read and Return Data
        data = ParentSerializer(Parent.objects.all(), many=True)
        return Response(data.data)

    def post(self, request):
        '''
                    Handling POST Requests for the endpoint 'localhost:8000/api/school/parents' and Adding sent data to the database 'Parent'
        Returns the newly added Data in the form of a JSON Object.
        '''

        data = ParentSerializer(data=request.data, many=True)
        if data.is_valid():
            data.save()
            return Response(data.data)
        else:
            return Response(data.errors)
