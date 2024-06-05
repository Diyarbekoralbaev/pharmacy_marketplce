from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, LoginSerializer, UserChangeProfileSerializer, UserForgotPasswordSerializer, UserResetPasswordSerializer, \
    OrderSerializer, OrderItemSerializer
from .models import CustomUser, OrderModel, OrderItemModel
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .utils import generate_otp, verify_otp
from drugs.models import Drug


class CreateUserView(APIView):
    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={
            201: openapi.Response('User created successfully.'),
            400: openapi.Response('Bad Request')
        }
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserMeView(APIView):
    permission_classes = (IsAuthenticated,)
    @swagger_auto_schema(
        responses={
            200: openapi.Response('User details fetched successfully.'),
            400: openapi.Response('Bad Request'),
            401: openapi.Response('Authentication failed.')
        }
    )
    def get(self, request):
        try:
            request_user = request.user
        except Exception as e:
            return Response({'error': 'Authentication failed.', 'message': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = UserSerializer(request_user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @swagger_auto_schema(
        request_body=UserChangeProfileSerializer,
        responses={
            200: openapi.Response('User details updated successfully.'),
            400: openapi.Response('Bad Request'),
            401: openapi.Response('Authentication failed.')
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
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListView(APIView):
    permission_classes = (IsAuthenticated,)
    @swagger_auto_schema(
        responses={
            200: openapi.Response('User list fetched successfully.'),
            400: openapi.Response('Bad Request'),
            401: openapi.Response('Authentication failed.'),
            404: openapi.Response('No users found.'),
            500: openapi.Response('An error occurred.')
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
                return Response({'error': 'No users found.'}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({'error': 'An error occurred.', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response('You are not authorized to view this page.', status=status.HTTP_401_UNAUTHORIZED)


class UserDetailView(APIView):
    permission_classes = (IsAuthenticated,)
    @swagger_auto_schema(
        responses={
            200: openapi.Response('User details fetched successfully.'),
            400: openapi.Response('Bad Request'),
            401: openapi.Response('Authentication failed.'),
            404: openapi.Response('User not found.'),
            500: openapi.Response('An error occurred.')
        }
    )
    def get(self, request, pk):
        request_user = request.user
        try:
            user = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'An error occurred.', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if request_user.role == 'admin' or request_user == user:
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response('You are not authorized to view this page.', status=status.HTTP_401_UNAUTHORIZED)
    @swagger_auto_schema(
        request_body=UserChangeProfileSerializer,
        responses={
            200: openapi.Response('User details updated successfully.'),
            400: openapi.Response('Bad Request'),
            401: openapi.Response('Authentication failed.'),
            404: openapi.Response('User not found.')
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
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response('You are not authorized to view this page.', status=status.HTTP_401_UNAUTHORIZED)
    @swagger_auto_schema(
        responses={
            200: openapi.Response('User deleted successfully.'),
            400: openapi.Response('Bad Request'),
            401: openapi.Response('Authentication failed.'),
            404: openapi.Response('User not found.'),
            500: openapi.Response('An error occurred.')
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
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'An error occurred.', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if request_user.role == 'admin' or request_user == user:
            user.delete()
            return Response('User deleted successfully.', status=status.HTTP_200_OK)
        return Response('You are not authorized to view this page.', status=status.HTTP_401_UNAUTHORIZED)


class UserChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)
    @swagger_auto_schema(
        request_body=UserChangeProfileSerializer,
        responses={
            200: openapi.Response('Password changed successfully.'),
            400: openapi.Response('Bad Request'),
            401: openapi.Response('Authentication failed.')
        }
    )
    def post(self, request):
        try:
            request_user = request.user
        except Exception as e:
            return Response({'error': 'Authentication failed.', 'message': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = UserChangeProfileSerializer(request_user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserForgotPasswordView(APIView):
    permission_classes = (AllowAny,)
    @swagger_auto_schema(
        request_body=UserForgotPasswordSerializer,
        responses={
            200: openapi.Response('OTP sent successfully.'),
            400: openapi.Response('Bad Request')
        }
    )
    def post(self, request):
        serializer = UserForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            otp = generate_otp(phone)
            return Response({'otp': otp}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserResetPasswordView(APIView):
    permission_classes = (AllowAny,)
    @swagger_auto_schema(
        request_body=UserResetPasswordSerializer,
        responses={
            200: openapi.Response('Password reset successfully.'),
            400: openapi.Response('Bad Request')
        }
    )
    def post(self, request):
        serializer = UserResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            otp = serializer.validated_data['otp']
            password = serializer.validated_data['password']
            if verify_otp(phone, otp):
                user = CustomUser.objects.get(phone=phone)
                user.set_password(password)
                user.save()
                return Response('Password reset successfully.', status=status.HTTP_200_OK)
            return Response('Invalid OTP.', status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderListCreateView(APIView):
    permission_classes = (IsAuthenticated,)
    @swagger_auto_schema(
        responses={
            200: openapi.Response('Order list fetched successfully.'),
            400: openapi.Response('Bad Request'),
            401: openapi.Response('Authentication failed.'),
            404: openapi.Response('No orders found.'),
            500: openapi.Response('An error occurred.')
        },
        tags=['Orders']
    )
    def get(self, request):
        try:
            request_user = request.user
        except Exception as e:
            return Response({'error': 'Authentication failed.', 'message': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            orders = OrderModel.objects.filter(user=request_user)
        except OrderModel.DoesNotExist:
            return Response({'error': 'No orders found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'An error occurred.', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @swagger_auto_schema(
        request_body=OrderSerializer,
        responses={
            201: openapi.Response('Order created successfully.'),
            400: openapi.Response('Bad Request')
        },
        tags=['Orders']
    )
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            order = OrderModel.objects.get(pk=serializer.data['id'])
            items = serializer.data['items']
            for item in items:
                OrderItemModel.objects.create(order=order, drug_id=item['drug'], quantity=item['quantity'], price=item['price'])
                Drug.objects.update(quantity=Drug.objects.get(pk=item['drug']).quantity - item['quantity'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailView(APIView):
    permission_classes = (IsAuthenticated,)
    @swagger_auto_schema(
        responses={
            200: openapi.Response('Order details fetched successfully.'),
            400: openapi.Response('Bad Request'),
            401: openapi.Response('Authentication failed.'),
            404: openapi.Response('Order not found.'),
            500: openapi.Response('An error occurred.')
        },
        tags=['Orders']
    )
    def get(self, request, pk):
        try:
            request_user = request.user
        except Exception as e:
            return Response({'error': 'Authentication failed.', 'message': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            order = OrderModel.objects.get(pk=pk)
        except OrderModel.DoesNotExist:
            return Response({'error': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'An error occurred.', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if request_user.role == 'admin' or request_user == order.user:
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response('You are not authorized to view this page.', status=status.HTTP_401_UNAUTHORIZED)
    @swagger_auto_schema(
        request_body=OrderSerializer,
        responses={
            200: openapi.Response('Order details updated successfully.'),
            400: openapi.Response('Bad Request'),
            401: openapi.Response('Authentication failed.'),
            404: openapi.Response('Order not found.')
        },
        tags=['Orders']
    )
    def put(self, request, pk):
        try:
            request_user = request.user
        except Exception as e:
            return Response({'error': 'Authentication failed.', 'message': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        order = OrderModel.objects.get(pk=pk)
        if request_user.role == 'admin' or request_user == order.user:
            serializer = OrderSerializer(order, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response('You are not authorized to view this page.', status=status.HTTP_401_UNAUTHORIZED)
    @swagger_auto_schema(
        responses={
            200: openapi.Response('Order deleted successfully.'),
            400: openapi.Response('Bad Request'),
            401: openapi.Response('Authentication failed.'),
            404: openapi.Response('Order not found.'),
            500: openapi.Response('An error occurred.')
        },
        tags=['Orders']
    )
    def delete(self, request, pk):
        try:
            request_user = request.user
        except Exception as e:
            return Response({'error': 'Authentication failed.', 'message': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            order = OrderModel.objects.get(pk=pk)
        except OrderModel.DoesNotExist:
            return Response({'error': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'An error occurred.', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if request_user.role == 'admin' or request_user == order.user:
            order.delete()
            return Response('Order deleted successfully.', status=status.HTTP_200_OK)
        return Response('You are not authorized to view this page.', status=status.HTTP_401_UNAUTHORIZED)
