from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, LoginSerializer, UserChangeProfileSerializer
from .models import CustomUser
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class CreateUserView(APIView):
    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={
            200: openapi.Response('User created successfully.'),
            400: openapi.Response('Bad Request')
        }
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class LoginView(APIView):
    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={
            200: openapi.Response('Login successful.'),
            400: openapi.Response('Bad Request')
        }
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)


class UserMeView(APIView):
    permission_classes = (IsAuthenticated,)
    @swagger_auto_schema(
        responses={
            200: openapi.Response('User details fetched successfully.'),
            400: openapi.Response('Bad Request')
        }
    )
    def get(self, request):
        try:
            request_user = request.user
        except Exception as e:
            return Response({'error': 'Authentication failed.', 'message': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = UserSerializer(request_user)
        return Response(serializer.data)
    @swagger_auto_schema(
        request_body=UserChangeProfileSerializer,
        responses={
            200: openapi.Response('User details updated successfully.'),
            400: openapi.Response('Bad Request')
        }
    )
    def put(self, request):
        try:
            request_user = request.user
        except Exception as e:
            return Response({'error': 'Authentication failed.', 'message': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = UserChangeProfileSerializer(request_user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class UserListView(APIView):
    permission_classes = (IsAuthenticated,)
    @swagger_auto_schema(
        responses={
            200: openapi.Response('User list fetched successfully.'),
            400: openapi.Response('Bad Request')
        }
    )
    def get(self, request):
        try:
            request_user = request.user
        except Exception as e:
            return Response({'error': 'Authentication failed.', 'message': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        if request_user.role == 'admin':
            try:
                users = CustomUser.objects.all()
            except CustomUser.DoesNotExist:
                return Response({'error': 'No users found.'}, status=404)
            except Exception as e:
                return Response({'error': 'An error occurred.', 'message': str(e)}, status=500)
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        return Response('You are not authorized to view this page.')


class UserDetailView(APIView):
    permission_classes = (IsAuthenticated,)
    @swagger_auto_schema(
        responses={
            200: openapi.Response('User details fetched successfully.'),
            400: openapi.Response('Bad Request')
        }
    )
    def get(self, request, pk):
        request_user = request.user
        try:
            user = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found.'}, status=404)
        except Exception as e:
            return Response({'error': 'An error occurred.', 'message': str(e)}, status=500)
        if request_user.role == 'admin' or request_user == user:
            serializer = UserSerializer(user)
            return Response(serializer.data)
        return Response('You are not authorized to view this page.')
    @swagger_auto_schema(
        request_body=UserChangeProfileSerializer,
        responses={
            200: openapi.Response('User details updated successfully.'),
            400: openapi.Response('Bad Request')
        }
    )
    def put(self, request, pk):
        try:
            request_user = request.user
        except Exception as e:
            return Response({'error': 'Authentication failed.', 'message': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        user = CustomUser.objects.get(pk=pk)
        if request_user.role == 'admin' or request_user == user:
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        return Response('You are not authorized to view this page.')
    @swagger_auto_schema(
        responses={
            200: openapi.Response('User deleted successfully.'),
            400: openapi.Response('Bad Request')
        }
    )
    def delete(self, request, pk):
        try:
            request_user = request.user
        except Exception as e:
            return Response({'error': 'Authentication failed.', 'message': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            user = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found.'}, status=404)
        except Exception as e:
            return Response({'error': 'An error occurred.', 'message': str(e)}, status=500)
        if request_user.role == 'admin' or request_user == user:
            user.delete()
            return Response('User deleted successfully.')
        return Response('You are not authorized to view this page.')