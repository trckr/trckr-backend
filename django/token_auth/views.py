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
        user_tokens = Token.objects.filter(user__id=request.user.id)

        if user_tokens.count() > 0:
            user_tokens.delete()
            return Response("success", status=status.HTTP_200_OK)

        return Response("token not found", status=status.HTTP_404_NOT_FOUND)
