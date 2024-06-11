from django.contrib import admin
from .models import Drug


class DrugAdmin(admin.ModelAdmin):
    list_display = ['drug_name', 'price', 'quantity', 'expiration_date', 'category', 'seller']
    list_filter = ['category', 'seller']
    search_fields = ['drug_name', 'category', 'seller']


admin.site.register(Drug, DrugAdmin)