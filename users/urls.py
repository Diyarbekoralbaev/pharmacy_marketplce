from django.urls import path

from .views import CreateUserView, LoginView, UserMeView, UserListView, UserDetailView

urlpatterns = [
    path('', UserListView.as_view()),
    path('<int:pk>/', UserDetailView.as_view()),
    path('me/', UserMeView.as_view()),
    path('create/', CreateUserView.as_view()),
    path('login/', LoginView.as_view()),
]
