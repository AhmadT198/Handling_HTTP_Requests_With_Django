from django.http import HttpRequest, JsonResponse, HttpResponse
from django.shortcuts import render
import json
from .serializers import *
from .forms import *
from .models import Student
from django.core import serializers
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, mixins



class SingleStudent(generics.GenericAPIView,
                    mixins.UpdateModelMixin,  ## For PUT Request
                    mixins.DestroyModelMixin, ## For DELETE Request
                    mixins.RetrieveModelMixin): ## For GET Request
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

class SingleParent(APIView):
    '''
    Class for handling HTTP Requests for the endpoint 'localhost:8000/api/<int:id>
    '''

    def get(self, request, *args, **kwargs):
        '''
            Handling GET Requests for the endpoint 'localhost:8000/api/school/parents/<int:id>'
        Returns the data of the student with the provided ID as a JSON Object
        '''
        id = kwargs['id']  ## ID from URL

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
        id = kwargs['id']  ## Extracting ID

        data = ParentSerializer(data=request.data, instance=Parent.objects.get(parentID=id))
        if data.is_valid():
            data.save()
            return Response(data.data)
        else:
            return Response(data.errors)


def delete(elf, request, *args, **kwargs):
    '''
            Handling DELETE Requests for the endpoint 'localhost:8000/school/parents/<int:id>'
    Returns Message in the form of a JSON Object {"message" : Msg} , Msg contains the string "Deleted" if it succeeded or contains the Error body.
    '''

    id = kwargs['id']  ## Extracting ID

    Msg = ""
    ## Try and delete, and return a suitable message.
    try:
        Parent.objects.get(parentID=id).delete()
    except Exception as e:
        Msg = str(e)
    else:
        Msg = "Deleted"

    return JsonResponse({"message": Msg});


class MultipleParents(APIView):
    '''
        Class for handling HTTP Requests for the endpoint 'localhost:8000/api/school/parents'
    '''

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


class MultipleSubjects(generics.ListCreateAPIView):
    '''
        Class for handling HTTP Requests for the endpoint 'localhost:8000/school/subjects'
    '''
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class SingleSubject(generics.DestroyAPIView,
                    generics.RetrieveAPIView,
                    generics.UpdateAPIView):
    '''
        Class for handling HTTP Requests for the endpoint 'localhost:8000/school/subjects/<int:id>'
    '''
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class ModifySubjects(APIView):
    '''
        A Class to Check, Add, or Delete the relationship between a specific Subject and a specific Student
    '''

    def get(self, request, *args, **kwargs):
        '''
            Returns whether the student has this subject or not.
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''

        ## Extracting IDs
        studID = kwargs['studentID']
        subID = kwargs['subjectID']

        Msg = {}
        try:
            ## Get the desired Records from the tables
            stud = Student.objects.get(studentID=studID)
            sub = Subject.objects.get(subjectID=subID)

            ## If the student has the subject, Return a Message. Else, Return another message
            if sub in stud.subjects.all():
                Msg = {"message": f"Student {stud} has the subject {sub}", "code": 200}
            else:
                Msg = {"message": f"Student {stud} doesnt have the subject {sub}", "code": 204}


        except Exception as e:  ## Return the error message and type, incase an error occurs
            Msg = {"type": str(e.__class__.__name__), "message": str(e), 'code': 500}

        return Response(Msg, status=Msg['code']);

    def post(self, request, *args, **kwargs):
        '''
            Creates a Relationship between the given Student and the given Subject.

        :param request:
        :param args:
        :param kwargs:
        :return: Returns a JSON Objecst with a message that indicates whether the subject already exists, was added successfully or an Error occured.
        '''

        ## Extracting IDs
        studID = kwargs['studentID'];
        subID = kwargs['subjectID']

        Msg = {}
        try:

            ## GEtting the desired records
            stud = Student.objects.get(studentID=studID)
            sub = Subject.objects.get(subjectID=subID)

            ## If the subject already exists, return a message indicating that.
            if sub in stud.subjects.all():
                Msg = {"message": f"Student {stud} already has the subject {sub}", "code": 200}
            else:  ## Else, Add the subject and return a suitable message
                stud.subjects.add(sub)
                Msg = {"message": f"the subject {sub} has been add successfully to the Student {stud}.", "code": 204}

        except Exception as e:  ## Return the error message and exception type, incase an error occurs
            Msg = {"type": str(e.__class__.__name__), "message": str(e), 'code': 500}

        return Response(Msg, status=Msg['code']);

    def delete(self, request, *args, **kwargs):
        '''
            Deletes the Relationship between the given Student and the given Subject if it exists.
        :param request:
        :param args:
        :param kwargs:
        :return: Returns a JSON object with a message that indicate whether the subject was deleted or if there is no such relationship.
        '''

        ## Extracting IDs
        studID = kwargs['studentID'];
        subID = kwargs['subjectID']

        Msg = {}
        try:

            ## Getting desired records
            stud = Student.objects.get(studentID=studID)
            sub = Subject.objects.get(subjectID=subID)

            ## If the subject exists, Delete it and return a suitable message.
            if sub in stud.subjects.all():
                stud.subjects.remove(sub)
                Msg = {"message": f"Deleted Successfully !", "code": 200}
            else:  ## If the relationship does not exist, Return a suitable message.
                Msg = {"message": f"the Student {stud} does not have the subject {sub}.", "code": 204}

        except Exception as e:  ## Return the error message and exception type, incase an error occurs
            Msg = {"type": str(e.__class__.__name__), "message": str(e), 'code': 500}

        return Response(Msg, status=Msg['code']);
