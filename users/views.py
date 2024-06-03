from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, LoginSerializer
from .models import CustomUser
from rest_framework.permissions import IsAuthenticated, AllowAny


class CreateUserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class UserMeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class UserListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        request_user = request.user
        if request_user.role == 'admin':
            users = CustomUser.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        return Response('You are not authorized to view this page.')


class UserDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        request_user = request.user
        user = CustomUser.objects.get(pk=pk)
        if request_user.role == 'admin' or request_user == user:
            serializer = UserSerializer(user)
            return Response(serializer.data)
        return Response('You are not authorized to view this page.')

    def put(self, request, pk):
        request_user = request.user
        user = CustomUser.objects.get(pk=pk)
        if request_user.role == 'admin' or request_user == user:
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        return Response('You are not authorized to view this page.')

    def delete(self, request, pk):
        request_user = request.user
        user = CustomUser.objects.get(pk=pk)
        if request_user.role == 'admin' or request_user == user:
            user.delete()
            return Response('User deleted successfully.')
        return Response('You are not authorized to view this page.')