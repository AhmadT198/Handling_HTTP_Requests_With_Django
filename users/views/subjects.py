
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



class MultipleSubjects(generics.ListCreateAPIView):
    '''
        Class for handling HTTP Requests for the endpoint 'localhost:8000/api/school/subjects'
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


################################################################################ MODIFYING RELATIONSHIPS
class ModifySubjects(APIView):
    '''
        A Class to Check, Add, or Delete the relationship between a specific Subject and a specific Student
    '''

    def get(self, request, *args, **kwargs):
        '''
            Returns whether the student has this subject or not.
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
        Returns a JSON Objecst with a message that indicates whether the subject already exists, was added successfully or an Error occured.
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
        Returns a JSON object with a message that indicate whether the subject was deleted or if there is no such relationship.
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
