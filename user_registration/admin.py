from django.contrib import admin

# Register your models here.

from .models import UserDetail , UserPaymentModel


from django.contrib import admin

class UserDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'password', 'email', 'phone', 'wallet', 'created_at', 'updated_at', 'is_active')
    search_fields = ('id', 'username', 'password', 'email', 'phone', 'wallet', 'created_at', 'updated_at', 'is_active')
    list_filter = ('id', 'username', 'password', 'email', 'phone', 'wallet', 'created_at', 'updated_at', 'is_active')

admin.site.register(UserDetail, UserDetailAdmin)

class UserPaymentModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'amount', 'upi_id', 'status', 'created_at', 'updated_at', 'is_active')
    search_fields = ('upi_id', 'user_id')
    list_filter =('upi_id', 'user_id')

admin.site.register(UserPaymentModel, UserPaymentModelAdmin)