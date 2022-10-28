from django.http import HttpRequest, JsonResponse, HttpResponse
from django.shortcuts import render
import json

from task4.settings import SECRET_KEY
from ..permissions import SessionAuth
from ..serializers import *
from ..forms import *
from ..models import Student
from django.core import serializers
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, mixins
from rest_framework.request import Request
import jwt
from datetime import datetime


class Logout(APIView):

    def get(self,request):
        currentToken = request.headers.get('jwt')
        try:
            loginTokens.objects.get(token=currentToken).delete()
            return Response("Logged out Successfully.")
        except loginTokens.DoesNotExist:
            return Response("Invalid Token, You shoudnt be here.")

