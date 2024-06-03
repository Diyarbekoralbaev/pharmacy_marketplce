from django.urls import path

from .views import CreateUserView, LoginView, UserMeView, UserListView, UserDetailView, UserChangePasswordView, UserForgotPasswordView, UserResetPasswordView

urlpatterns = [
    path('', UserListView.as_view()),
    path('<int:pk>/', UserDetailView.as_view()),
    path('me/', UserMeView.as_view()),
    path('signup/', CreateUserView.as_view()),
    path('login/', LoginView.as_view()),
    path('change-password/', UserChangePasswordView.as_view()),
    path('forgot-password/', UserForgotPasswordView.as_view()),
    path('reset-password/', UserResetPasswordView.as_view()),
]
