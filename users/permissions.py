from rest_framework import authentication
from rest_framework import exceptions
import jwt
from django.shortcuts import redirect
from rest_framework import permissions

from task4.settings import SECRET_KEY
from datetime import datetime

from users.models import loginTokens, Parent, Accounts, Student
from users.serializers import ParentSerializer, AccountsSerializer, StudentSerializer

url = '/api/school/'


class SessionAuth(authentication.BaseAuthentication):
    '''
    Class for Authenticating whether the current Session is expired or not
    '''

    def authenticate(self, request):

        ## Get the Current TimeStamp
        dt = datetime.now()
        ts = datetime.timestamp(dt)

        try:  ## try to decode the token in the header
            data = jwt.decode(request.headers.get('jwt'), SECRET_KEY, algorithms=["HS256"])
        except Exception as e:  ## if failed add an empty token
            data = {
                "isLoggedIn": 0,
                "username": "-1",
                "timestamp": ts
            }

        duration = (ts - data['timestamp'])  ## Age of the token

        if data["isLoggedIn"]:  ## If the token says he's logged In,

            ## Validate whether this token exists or not
            token = loginTokens.objects.filter(token=request.headers.get('jwt'))
            if len(token) == 0:  ## if not , raise an exception
                raise exceptions.NotAuthenticated("Invalid Token.")

            ## if the token is valid but its duration ended
            if duration > 100 * 60:
                loginTokens.objects.get(token=request.headers.get('jwt')).delete()  ## Delete Token
                raise exceptions.AuthenticationFailed("Your session has expired")  ## Raise an exception
            else:  ## Else,

                if "login" in request.path.split(
                        '/'):  ## Check if a user is trying to access the login page while logged in
                    raise exceptions.NotAcceptable("You are already Logged In as " + data['username'],
                                                   redirect(url + 'login'))
                else:
                    return (True, None)
        else:
            return (True, None)


class UserPermission(permissions.BasePermission):
    '''
    Class to check if a user has a permission to access the endpoints or not
    '''

    def has_permission(self, request, view):

        ## Extract data from Token
        data = jwt.decode(request.headers.get('jwt'), SECRET_KEY, algorithms=["HS256"])
        data = AccountsSerializer(Accounts.objects.get(username=data['username']))
        data = data.data

        userId = data['id']  ## ID of the user Account in the token
        pathList = ((request._request.path).split('/'))  ## Getting the current Path
        attempted_pk = view.kwargs.get('pk', None)  ##ID in the URL Param

        if data['type'] == "PRNT" and 'parents' in pathList:  ## If the user is a Parent and trying to access a Parent

            pId = ParentSerializer(Parent.objects.get(login_id=userId))[
                'parentID'].value  ## Get the parentID through the Account ID


            if pId == attempted_pk:  ##if the Attempted ID Equals the ID of the Authenticated user in the token , Return True
                return True
            else:
                self.message = "You Dont have access to this User"
                return False
        elif data[
            'type'] == "STUD" and 'students' in pathList:  ## If the user is a Student and trying to access a Student
            ## SAME AS PARENT
            sId = StudentSerializer(Student.objects.get(login_id=userId))['studentID'].value
            if sId == attempted_pk:
                return True
            else:
                self.message = "You Dont have access to this User"
                return False
        else:
            self.message = "You Dont have access to this User"
            return False

    def has_object_permission(self, request, view, obj):
        return True

