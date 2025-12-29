from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Account, Card, Transaction


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone_number', 'date_of_birth', 'address')}),
    )


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['account_number', 'user', 'account_type', 'balance', 'status', 'created_at']
    list_filter = ['account_type', 'status', 'created_at']
    search_fields = ['account_number', 'user__username', 'user__email']
    readonly_fields = ['account_number', 'created_at', 'updated_at']


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ['card_number', 'account', 'card_type', 'status', 'expiry_date', 'created_at']
    list_filter = ['card_type', 'status', 'created_at']
    search_fields = ['card_number', 'account__account_number']
    readonly_fields = ['card_number', 'cvv', 'created_at']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'account', 'transaction_type', 'amount', 'status', 'created_at']
    list_filter = ['transaction_type', 'status', 'created_at']
    search_fields = ['transaction_id', 'account__account_number']
    readonly_fields = ['transaction_id', 'created_at']
