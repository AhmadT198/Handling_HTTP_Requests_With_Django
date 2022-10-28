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
    def authenticate(self, request):
        dt = datetime.now()
        ts = datetime.timestamp(dt)

        try:
            data = jwt.decode(request.headers.get('jwt'), SECRET_KEY, algorithms=["HS256"])
        except Exception as e:
            data = {
                "isLoggedIn": 0,
                "username": "-1",
                "timestamp": ts
            }

        duration = (ts - data['timestamp'])

        if data["isLoggedIn"]:
            token = loginTokens.objects.filter(token=request.headers.get('jwt'))
            if len(token) == 0:
                raise exceptions.NotAuthenticated("Invalid Token.")

            if duration > 100 * 60:
                print("session expired")
                loginTokens.objects.get(token=request.headers.get('jwt')).delete()
                raise exceptions.AuthenticationFailed("Your session has expired", redirect(url + 'login'))
            else:
                if "login" in request.path.split('/'):
                    raise exceptions.NotAcceptable("You are already Logged In as " + data['username'], redirect(url + 'login'))
                else:
                    return (True,None)


        else:
            return (True, None)


class UserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        data = jwt.decode(request.headers.get('jwt'), SECRET_KEY, algorithms=["HS256"])
        data = AccountsSerializer(Accounts.objects.get(username=data['username']))
        data = data.data

        userId = data['id']  ## ID of the user Account in the token
        pathList = ((request._request.path).split('/'))
        attempted_pk = view.kwargs.get('pk', None)  ##ID in the URL Param

        if data['type'] == "PRNT" and 'parents' in pathList:

            pId = ParentSerializer(Parent.objects.get(login_id=userId))[
                'parentID'].value  ## Get the parentID through the Account ID
            print(pId, " ", attempted_pk)
            if pId == attempted_pk:  ##if the Attempted ID Equals the ID of the user in the token , Return True
                return True
            else:
                self.message = "You Dont have access to this User"
                return False
        elif data['type'] == "STUD" and 'students' in pathList:
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



# {
#     "username" : "AhmadsasaSr2198",
#     "password" : "Paswraaaaaod",
#     "type": "PRNT"
# }