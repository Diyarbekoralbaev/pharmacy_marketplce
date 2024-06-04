from django.urls import path

from .views import CreateUserView, LoginView, UserMeView, UserListView, UserDetailView, UserChangePasswordView, UserForgotPasswordView, UserResetPasswordView

urlpatterns = [
    path('', UserListView.as_view(), name='user-list'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('me/', UserMeView.as_view()),
    path('signup/', CreateUserView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('change-password/', UserChangePasswordView.as_view(), name='change-password'),
    path('forgot-password/', UserForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/', UserResetPasswordView.as_view(), name='reset-password'),
]
