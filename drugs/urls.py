from django.urls import path

from .views import CreateDrugView, UpdateDrugView, DeleteDrugView, ListDrugView, DrugDetailView

urlpatterns = [
    path('', ListDrugView.as_view()),
    path('<int:pk>/', DrugDetailView.as_view()),
    path('create/', CreateDrugView.as_view()),
    path('update/<int:pk>/', UpdateDrugView.as_view()),
    path('delete/<int:pk>/', DeleteDrugView.as_view()),
]
