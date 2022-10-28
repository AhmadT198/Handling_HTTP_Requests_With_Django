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
from rest_framework.request import Request


class Register(APIView):

    def post(self, request):

        ## Pass the request body to the Accounts Serializer to validate the Accounts Data ("username", "password", "type")
        data = AccountsSerializer(data=request.data)

        ## If valid
        if data.is_valid():

            ## Extract the Student/Parent Data from the whole body

            userData = {}
            for key in data.initial_data:
                print(key)
                if key != 'type' and key != 'username' and key != 'password':
                    userData[key] = data.initial_data[key]

            ## if the Account is for a Parent,
            if data.validated_data['type'] == 'PRNT':

                ## Pass the Parent Data to the Parent Serializer to check its values
                p = ParentSerializer(data=userData)

                ## If the values are valid,
                if p.is_valid():
                    ## Save the Account info, Update the login_id then save the Parent
                    try:
                        data.save()
                        p.validated_data['login_id'] = data.data['id']
                        p.save()
                    except Exception as e: ## Return suitable Errors
                        return Response(e)

                    return Response(p.data) ## If it succeeded return the newly added data
                else:
                    return Response(p.errors) ## ELse, Return Suitable Errors
            else: ## SAME THING With Students
                s = StudentSerializer(data=userData)
                if s.is_valid():
                    try:
                        data.save()
                        s.validated_data['login_id'] = data.data['id']
                        s.save()
                    except Exception as e:
                        return Response(e)
                    return Response(s.data)
                else:
                    return Response(s.errors)
        else:
            return Response(data.errors)

# {
#      "username": "ASASAaaaaaaaS",
#     "password": "Paswraaaaaod",
#     "type": "PRNT", "firstName" : "Ahmad", "lastName" : "Tamer","email" : "aaa@aa.com", "job":"sdasdsad"
# }

# {
#      "username": "AhmadSr2198",
#     "password": "Paswraaaaaod",
#     "type": "PRNT", "firstName" : "AhmadJr", "lastName" : "Tamer","email" : "aaa@aa.com", "job":"sdasdsad", "parentID":1
# }

