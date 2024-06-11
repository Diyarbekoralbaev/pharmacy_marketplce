from django.urls import path

from .views import CreateDrugView, UpdateDrugView, DeleteDrugView, ListDrugView, DrugDetailView, DrugGetCategoriesView, DrugSellersDrugsView

urlpatterns = [
    path('', ListDrugView.as_view()),
    path('<int:pk>/', DrugDetailView.as_view()),
    path('create/', CreateDrugView.as_view()),
    path('update/<int:pk>/', UpdateDrugView.as_view()),
    path('delete/<int:pk>/', DeleteDrugView.as_view()),
    path('categories/', DrugGetCategoriesView.as_view()),
    path('my_drugs/', DrugSellersDrugsView.as_view()),
]
