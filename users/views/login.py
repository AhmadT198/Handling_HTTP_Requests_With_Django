from drf_yasg.utils import swagger_auto_schema
from task4.settings import SECRET_KEY
from ..permissions import SessionAuth
from ..serializers import *
from ..forms import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import jwt
from datetime import datetime


class login(APIView):
    '''
    Class To handle Logging in through the endpoint 'api/school/login'
    '''
    authentication_classes = [SessionAuth]

    @swagger_auto_schema(request_body=AccountsSerializer)
    def post(self, request):

        ## Get Current TimeStamp
        dt = datetime.now()
        ts = datetime.timestamp(dt)

        data = AccountsSerializer(request.data)  ## Get data in the form of JSON Object
        try:
            if data.data['type'] == 'PRNT': ## If it is a Parent Login
                try:

                    user = AccountsSerializer(
                        Accounts.objects.get(username=data.data['username'], password=data.data['password'])) ## Check if the Account exists

                    ## Create a Log in Token for the user
                    token = {
                        "user": user.data['id'],
                        "token":
                            jwt.encode({
                                "isLoggedIn": 1,
                                "username": user.data['username'],
                                "timestamp": ts
                            }, SECRET_KEY)}


                    try: ## If the user already has a token, Update it
                        tokenUpdate = TokenSerializer(data=token,
                                                      instance=loginTokens.objects.get(user=user.data['id']))
                        if tokenUpdate.is_valid():
                            tokenUpdate.save()
                            return Response(tokenUpdate.data) ## Return the new Token
                        return Response(tokenUpdate.errors) ## Return Errors if they occur
                    except: ## If the user doesnt have any tokens, Create One
                        tokenCreate = TokenSerializer(data=token)
                        if tokenCreate.is_valid():
                            tokenCreate.save()
                            return Response(tokenCreate.data) ## Return the new Token
                        return Response(tokenCreate.errors) ## Return Errors if they occur

                except Accounts.DoesNotExist: ## Return Error Message
                    return Response("Incorrect Username and/or Password", status.HTTP_401_UNAUTHORIZED)

            else: ## Same thing for students
                try:
                    user = AccountsSerializer(
                        Accounts.objects.get(username=data.data['username'], password=data.data['password']))

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
                            return Response(tokenUpdate.data)

                        return Response(tokenUpdate.errors)
                    except:
                        tokenCreate = TokenSerializer(data=token)
                        if tokenCreate.is_valid():
                            tokenCreate.save()
                            return Response(tokenCreate.data)
                        return Response(tokenCreate.errors)

                except Accounts.DoesNotExist:

                    return Response("Incorrect Username and/or Password", status.HTTP_401_UNAUTHORIZED)

        except Exception as e: ## Incase the request body is invalid
            return Response("Invalid Input.", status.HTTP_400_BAD_REQUEST)
