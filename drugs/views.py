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
    
class UpdateDrugView(APIView):
    @swagger_auto_schema(
        request_body=DrugUpdateSerializer,
        responses={
            200: openapi.Response('Drug updated successfully.'),
            400: openapi.Response('Bad Request')
        }
    )
    def put(self, request, pk):
        try:
            drug = Drug.objects.get(pk=pk)
        except Drug.DoesNotExist:
            return Response({'error': 'Drug does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = DrugUpdateSerializer(drug, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class DeleteDrugView(APIView):
    @swagger_auto_schema(
        responses={
            200: openapi.Response('Drug deleted successfully.'),
            400: openapi.Response('Bad Request')
        }
    )
    def delete(self, request, pk):
        try:
            drug = Drug.objects.get(pk=pk)
        except Drug.DoesNotExist:
            return Response({'error': 'Drug does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        drug.delete()
        return Response({'message': 'Drug deleted successfully.'})
    
class ListDrugView(APIView):
    @swagger_auto_schema(
        responses={
            200: openapi.Response('List of drugs fetched successfully.'),
            400: openapi.Response('Bad Request')
        }
    )
    def get(self):
        drugs = Drug.objects.all()
        serializer = DrugSerializer(drugs, many=True)
        return Response(serializer.data)
    
class DrugDetailView(APIView):
    @swagger_auto_schema(
        responses={
            200: openapi.Response('Drug details fetched successfully.'),
            400: openapi.Response('Bad Request')
        }
    )
    def get(self, request, pk):
        try:
            drug = Drug.objects.get(pk=pk)
        except Drug.DoesNotExist:
            return Response({'error': 'Drug not found.'}, status=404)
        serializer = DrugSerializer(drug)
        return Response(serializer.data)
    
class DrugSearchView(APIView):
    @swagger_auto_schema(
        responses={
            200: openapi.Response('List of drugs fetched successfully.'),
            400: openapi.Response('Bad Request')
        }
    )
    def get(self, request):
        query = request.query_params.get('query')
        drugs = Drug.objects.filter(name__icontains=query)
        serializer = DrugSerializer(drugs, many=True)
        return Response(serializer.data)
    
