from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Drug
from .serializers import DrugSerializer, DrugUpdateSerializer
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.

class CreateDrugView(APIView):
    @swagger_auto_schema(
        request_body=DrugSerializer,
        responses={
            200: openapi.Response('Drug created successfully.'),
            400: openapi.Response('Bad Request')
        }
    )
    def post(self, request):
        serializer = DrugSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    

