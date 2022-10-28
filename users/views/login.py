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


class login(APIView):
    authentication_classes = [SessionAuth]

    def post(self, request):
        dt = datetime.now()
        ts = datetime.timestamp(dt)

        data = AccountsSerializer(request.data)
        if data.data['type'] == 'PRNT':
            try:
                user = AccountsSerializer(
                    Accounts.objects.get(username=data.data['username'], password=data.data['password']))
                data = ParentSerializer(Parent.objects.get(login_id=user.data['id']))

                token = {
                    "user": user.data['id'],
                    "token":
                        jwt.encode({
                            "isLoggedIn": 1,
                            "username": user.data['username'],
                            "timestamp": ts
                        }, SECRET_KEY)}

                try:
                    tokenUpdate = TokenSerializer(data=token, instance=loginTokens.objects.get(user=user.data['id']))
                    if tokenUpdate.is_valid():
                        tokenUpdate.save()
                        print("Update")
                        return Response(tokenUpdate.data)
                    return Response(tokenUpdate.errors)
                except:
                    print("create")
                    tokenCreate = TokenSerializer(data=token)
                    if tokenCreate.is_valid():
                        tokenCreate.save()
                        return Response(tokenCreate.data)
                    return Response(tokenCreate.errors)

            except Accounts.DoesNotExist:
                return Response(status.HTTP_404_NOT_FOUND)
        else:
            try:
                user = AccountsSerializer(
                    Accounts.objects.get(username=data.data['username'], password=data.data['password']))
                data = StudentSerializer(Student.objects.get(login_id=user.data['id']))
                token = {
                    "user": user.data['id'],
                    "token":
                        jwt.encode({
                            "isLoggedIn": 1,
                            "username": user.data['username'],
                            "timestamp": ts
                        }, SECRET_KEY)}

                try:
                    tokenUpdate = TokenSerializer(data=token, instance=loginTokens.objects.get(user=user.data['id']))
                    if tokenUpdate.is_valid():
                        tokenUpdate.save()
                        print("Update")
                        return Response(tokenUpdate.data)

                    return Response(tokenUpdate.errors)
                except:
                    print("create")
                    tokenCreate = TokenSerializer(data=token)
                    if tokenCreate.is_valid():
                        tokenCreate.save()
                        return Response(tokenCreate.data)
                    return Response(tokenCreate.errors)

            except Accounts.DoesNotExist:
                return Response(status.HTTP_404_NOT_FOUND)
