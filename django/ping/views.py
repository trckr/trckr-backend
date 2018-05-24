from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response


class Ping(APIView):
    '''
    Returns a pong response on request to verify that the server is up
    '''

    def get(self, request, format=None):
        return Response("pong")
