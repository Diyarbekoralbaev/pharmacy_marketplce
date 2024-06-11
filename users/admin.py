from django.contrib import admin
from .models import CustomUser, OrderModel, OrderItemModel


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'role', 'is_active', 'is_staff']
    search_fields = ['username', 'first_name', 'last_name', 'phone']
    list_filter = ['role', 'is_active', 'is_staff']
    list_per_page = 10
    ordering = ['username']


class OrderModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'status', 'total_price']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'user__phone']
    list_filter = ['status']
    list_per_page = 10
    ordering = ['-created_at']


class OrderItemModelAdmin(admin.ModelAdmin):
    list_display = ['order', 'drug', 'quantity', 'price']
    search_fields = ['order__user__username', 'order__user__first_name', 'order__user__last_name', 'order__user__phone']
    list_per_page = 10
    ordering = ['order']


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(OrderModel, OrderModelAdmin)
admin.site.register(OrderItemModel, OrderItemModelAdmin)