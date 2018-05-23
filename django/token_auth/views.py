from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token 


class InvalidateAuthToken(APIView):
    """
    Logout a user by deleting the token
    """

    def post(self, request):
        token_key = request.auth.key
        user_token = Token.objects.get(user=request.user, key=token_key)
        user_token.delete()
        return Response("success", status=status.HTTP_200_OK)
