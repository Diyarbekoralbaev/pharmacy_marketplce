from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, LoginSerializer, UserChangeProfileSerializer, UserForgotPasswordSerializer, UserResetPasswordSerializer, \
    OrderSerializer, OrderItemSerializer, DeleteItemFromOrderSerializer
from .models import CustomUser, OrderModel, OrderItemModel
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .utils import generate_otp, verify_otp
from drugs.models import Drug


class CreateUserView(APIView):
    @swagger_auto_schema(
        request_body=UserSerializer,
        operation_summary='Sign Up',
        operation_description='For signing up a new user.',
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
        operation_summary='Login',
        operation_description='For logging in a user.',
        responses={
            200: openapi.Response('Login successful.'),
            400: openapi.Response('Bad Request')
        }
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserMeView(APIView):
    permission_classes = (IsAuthenticated,)
    @swagger_auto_schema(
        operation_summary='Get user details',
        operation_description='For fetching the details of the logged-in user.',
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
        operation_summary='Update user details',
        operation_description='For updating the details of the logged-in user.',
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
        operation_summary='Get user list',
        operation_description='For fetching the list of all users.',
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
        operation_summary='Get user details',
        operation_description='For fetching the details of a user.',
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
        operation_summary='Update user details',
        operation_description='For updating the details of a user.',
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
        operation_summary='Delete user',
        operation_description='For deleting a user.',
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
        operation_summary='Change Password',
        operation_description='For changing the password of the logged-in user.',
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
        operation_summary='Forgot Password',
        operation_description='For sending an OTP to the user for resetting the password.',
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
        operation_summary='Reset Password',
        operation_description='For resetting the password of the user.',
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
        operation_summary='Get order list',
        operation_description='For fetching the list of all orders.',
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
        operation_summary='Create order',
        operation_description='For creating a new order.',
        responses={
            201: openapi.Response('Order created successfully.'),
            400: openapi.Response('Bad Request')
        },
        tags=['Orders']
    )
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save(user=request.user)
            for item in serializer.validated_data['items']:
                drug = Drug.objects.get(pk=item['drug'].id)
                if drug.quantity < item['quantity']:
                    order.delete()
                    return Response({f"error": f"Insufficient quantity of {drug.drug_name}. Available quantity is {drug.quantity}."}, status=status.HTTP_400_BAD_REQUEST)
                drug.quantity -= item['quantity']
                drug.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailView(APIView):
    permission_classes = (IsAuthenticated,)
    @swagger_auto_schema(
        operation_summary='Get order details',
        operation_description='For fetching the details of an order.',
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
        operation_summary='Update order details',
        operation_description='For updating the details of an order.',
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
        operation_summary='Delete order',
        operation_description='For deleting an order.',
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


class DeleteItemFromOrderView(APIView):
    permission_classes = (IsAuthenticated,)
    @swagger_auto_schema(
        request_body=DeleteItemFromOrderSerializer,
        operation_summary='Delete item from order',
        operation_description='For deleting an item from an order.',
        responses={
            200: openapi.Response('Item deleted successfully.'),
            400: openapi.Response('Bad Request'),
            401: openapi.Response('Authentication failed.'),
            404: openapi.Response('Order not found.'),
            500: openapi.Response('An error occurred.')
        },
        tags=['Orders']
    )
    def post(self, request):
        try:
            request_user = request.user
        except Exception as e:
            return Response({'error': 'Authentication failed.', 'message': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = DeleteItemFromOrderSerializer(data=request.data)
        if serializer.is_valid():
            if request_user.role in ['admin', 'seller']:
                order_id = serializer.validated_data['order_id']
                item_id = serializer.validated_data['item_id']
                try:
                    order = OrderModel.objects.get(pk=order_id)
                except OrderModel.DoesNotExist:
                    return Response({'error': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)
                except Exception as e:
                    return Response({'error': 'An error occurred.', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                try:
                    item = OrderItemModel.objects.get(pk=item_id)
                except OrderItemModel.DoesNotExist:
                    return Response({'error': 'Item not found.'}, status=status.HTTP_404_NOT_FOUND)
                except Exception as e:
                    return Response({'error': 'An error occurred.', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                if order.user != request_user and request_user.role != 'admin':
                    return Response('This is not your order.', status=status.HTTP_401_UNAUTHORIZED)
                order.total_price -= item.price
                order.save()
                item.delete()
                return Response('Item deleted successfully.', status=status.HTTP_200_OK)
            return Response('You are not authorized to view this page.', status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)