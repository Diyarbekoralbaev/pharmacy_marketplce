from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Drug
from .serializers import DrugSerializer, DrugUpdateSerializer
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.core.cache import cache


class CreateDrugView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated,)
    @swagger_auto_schema(
        request_body=DrugSerializer,
        responses={
            201: openapi.Response('Drug created successfully.'),
            400: openapi.Response('Bad Request'),
            403: openapi.Response('Forbidden'),
            500: openapi.Response('Internal Server Error'),
        }
    )
    def post(self, request):
        cache.delete('drugs')
        try:
            request_user = request.user
        except Exception as e:
            return Response({'error': 'An error occurred.', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if request_user.role == 'buyer':
            return Response({'error': 'You do not have permission to create a drug.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = DrugSerializer(data=request.data)
        if serializer.is_valid():
            if request_user.role == 'seller' or request_user.role == 'admin':
                serializer.save(seller=request_user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({'error': 'You do not have permission to create a drug.'}, status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class UpdateDrugView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated,)
    @swagger_auto_schema(
        request_body=DrugUpdateSerializer,
        responses={
            200: openapi.Response('Drug updated successfully.'),
            400: openapi.Response('Bad Request'),
            403: openapi.Response('Forbidden'),
            404: openapi.Response('Not Found'),
            500: openapi.Response('Internal Server Error'),
        }
    )
    def put(self, request, pk):
        cache.delete('drugs')
        cache.delete(f'drug-{pk}')
        try:
            request_user = request.user
        except Exception as e:
            return Response({'error': 'An error occurred.', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if request_user.role == 'buyer':
            return Response({'error': 'You do not have permission to update a drug.'}, status=status.HTTP_403_FORBIDDEN)
        try:
            drug = Drug.objects.get(pk=pk)
        except Drug.DoesNotExist:
            return Response({'error': 'Drug does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'An error occurred.', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer = DrugUpdateSerializer(drug, data=request.data)
        if serializer.is_valid():
            serializer.save(seller=request_user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteDrugView(APIView):
    permission_classes = (IsAuthenticated,)
    @swagger_auto_schema(
        responses={
            200: openapi.Response('Drug deleted successfully.'),
            400: openapi.Response('Bad Request'),
            403: openapi.Response('Forbidden'),
            404: openapi.Response('Not Found'),
        }
    )
    def delete(self, request, pk):
        cache.delete('drugs')
        cache.delete(f'drug-{pk}')
        try:
            request_user = request.user
        except Exception as e:
            return Response({'error': 'An error occurred.', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if request_user.role == 'buyer':
            return Response({'error': 'You do not have permission to delete a drug.'}, status=status.HTTP_403_FORBIDDEN)
        try:
            drug = Drug.objects.get(pk=pk)
        except Drug.DoesNotExist:
            return Response({'error': 'Drug does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'An error occurred.', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        drug.delete()
        return Response({'message': 'Drug deleted successfully.'})


class ListDrugView(APIView):
    @swagger_auto_schema(
        responses={
            200: openapi.Response('List of drugs fetched successfully.'),
            400: openapi.Response('Bad Request'),
            404: openapi.Response('Not Found'),
        }
    )
    def get(self, request):
        cache_key = 'drugs'
        data = cache.get(cache_key)
        if data:
            return Response(data)
        else:
            try:
                drugs = Drug.objects.all()
            except Exception as e:
                return Response({'error': 'An error occurred.', 'message': str(e)}, status=500)
            serializer = DrugSerializer(drugs, many=True)
            cache.set(cache_key, serializer.data, timeout=600)  # 10 minutes
            return Response(serializer.data)


class DrugDetailView(APIView):
    @swagger_auto_schema(
        responses={
            200: openapi.Response('Drug details fetched successfully.'),
            400: openapi.Response('Bad Request'),
            404: openapi.Response('Not Found'),
        }
    )
    def get(self, request, pk):
        cache_key = f'drug-{pk}'
        data = cache.get(cache_key)
        if data:
            return Response(data)
        try:
            drug = Drug.objects.get(pk=pk)
        except Drug.DoesNotExist:
            return Response({'error': 'Drug not found.'}, status=404)
        except Exception as e:
            return Response({'error': 'An error occurred.', 'message': str(e)}, status=500)
        serializer = DrugSerializer(drug)
        cache.set(cache_key, serializer.data, timeout=600)  # 10 minutes
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
    
