from django.contrib import admin

# Register your models here.
from django.utils.html import format_html
from django.http import HttpResponse
import csv
from .models import *


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

from django.contrib import admin
from django.utils.html import format_html
from .models import UserwithdrawHistory, UserBankDetails

class UserwithdrawHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'bank_info', 'amount', 'status_colored', 'created_at', 'updated_at', 'is_active')
    search_fields = ('id','status')  # Assuming 'username' is a field in UserDetail model
    list_filter = ('status', 'created_at', 'updated_at', 'is_active')
    actions = ['mark_as_done', 'mark_as_reject' , 'download_csv']

    def bank_info(self, obj):
        return f"{obj.bank_id.bank_name},AC No: {obj.bank_id.account_number}, IFSC: {obj.bank_id.ifsc_code}"

    bank_info.short_description = 'Bank Details'

    
    def status_colored(self, obj):
        if obj.status == 'In Process':
            return format_html('<span style="color: orange;">{}</span>', obj.status)
        elif obj.status == 'done':
            return format_html('<span style="color: green;">{}</span>', obj.status)
        elif obj.status == 'reject':
            return format_html('<span style="color: red;">{}</span>', obj.status)
        else:
            return format_html('<span style="color: orange;">{}</span>', obj.status)

    status_colored.short_description = 'Status'

    def mark_as_done(self, request, queryset):
        rows_updated = 0
        for obj in queryset:
            if obj.status != 'reject':
                obj.status = 'done'
                obj.save()
                rows_updated += 1
        self.message_user(request, f'{rows_updated} record(s) marked as Done.')

    mark_as_done.short_description = 'Mark selected as Done'

    def mark_as_reject(self, request, queryset):
        rows_updated = 0
        for obj in queryset:
            if obj.status != 'done':
                obj.status = 'reject'
                obj.is_active = False
                obj.save()
                rows_updated += 1
                # Update user's wallet balance if status is rejected
                if obj.status == 'reject':
                    user = obj.user_id
                    user.wallet += obj.amount
                    user.save()
        self.message_user(request, f'{rows_updated} record(s) marked as Reject.')
    mark_as_reject.short_description = 'Mark selected as Reject'

    def download_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="user_withdraw_history.csv"'

        writer = csv.writer(response)
        writer.writerow(['ID', 'User ID', 'Bank Name', 'Amount', 'Status', 'Created At', 'Updated At'])

        for obj in queryset:
            writer.writerow([
                obj.id,
                obj.user_id.username,
                f"{obj.bank_id.bank_name},AC No: {obj.bank_id.account_number}, IFSC: {obj.bank_id.ifsc_code}",
                obj.amount,
                obj.status,
                obj.created_at,
                obj.updated_at
            ])

        return response

    download_csv.short_description = "Download CSV"

admin.site.register(UserwithdrawHistory, UserwithdrawHistoryAdmin)

class UserGameDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'game_type', 'game_id', 'type_of_bet', 'bet', 'amount', 'user_id', 'created_at', 'updated_at', 'is_active', 'win_or_lose', 'winning_amount', 'winning_number', 'winning_color', 'winning_ball')
    list_filter = ('game_type', 'type_of_bet', 'user_id', 'is_active')
    search_fields = ('game_type', 'type_of_bet', 'bet', 'user_id__username')

admin.site.register(UserGameData, UserGameDataAdmin)


class UserDepositwHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'upi_id', 'utr_number', 'amount', 'status_colored', 'created_at', 'updated_at', 'is_active')
    search_fields = ('id','status')  # Assuming 'username' is a field in UserDetail model
    list_filter = ('status', 'created_at', 'updated_at', 'is_active')
    actions = ['mark_as_done', 'mark_as_reject' ]

    # def bank_info(self, obj):
    #     return f"{obj.bank_id.bank_name},AC No: {obj.bank_id.account_number}, IFSC: {obj.bank_id.ifsc_code}"

    # bank_info.short_description = 'Bank Details'

    
    def status_colored(self, obj):
        if obj.status == 'In Process':
            return format_html('<span style="color: orange;">{}</span>', obj.status)
        elif obj.status == 'done':
            return format_html('<span style="color: green;">{}</span>', obj.status)
        elif obj.status == 'reject':
            return format_html('<span style="color: red;">{}</span>', obj.status)
        else:
            return format_html('<span style="color: orange;">{}</span>', obj.status)

    status_colored.short_description = 'Status'

    def mark_as_done(self, request, queryset):
        rows_updated = 0
        for obj in queryset:
            if obj.status != 'reject':
                obj.status = 'done'
                obj.save()
                rows_updated += 1
                user = obj.user_id
                user.wallet += obj.amount
                user.save()
        self.message_user(request, f'{rows_updated} record(s) marked as Done.')

    mark_as_done.short_description = 'Mark selected as Done'

    def mark_as_reject(self, request, queryset):
        rows_updated = 0
        for obj in queryset:
            if obj.status != 'done':
                obj.status = 'reject'
                obj.is_active = False
                obj.save()
                rows_updated += 1
                # Update user's wallet balance if status is rejected
                # if obj.status == 'reject':
                #     user = obj.user_id
                #     user.wallet += obj.amount
                #     user.save()
        self.message_user(request, f'{rows_updated} record(s) marked as Reject.')
    mark_as_reject.short_description = 'Mark selected as Reject'
admin.site.register(Userdeposithistory, UserDepositwHistoryAdmin)