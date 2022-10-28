from ..forms import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class Logout(APIView):
    '''
    a Class for Logging Out through the endpoint 'api/school/logout'
    '''
    def get(self,request):
        '''
        Logging out
        Returns a Respinse with "Logged out Successfully." incase of a valid token or "Invalid Token, You shoudnt be here." incase of an invalid token
        '''
        currentToken = request.headers.get('jwt')
        try: ## Attempt to delete the Token
            loginTokens.objects.get(token=currentToken).delete()
            return Response("Logged out Successfully.", status.HTTP_200_OK)
        except loginTokens.DoesNotExist:
            return Response("Invalid Token, You shoudnt be here.", status.HTTP_400_BAD_REQUEST)

