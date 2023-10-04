from billing import models
from django.contrib import admin


class AccountStatusInline(admin.TabularInline):
    model = models.AccountStatus
    fields = ["status"]


class InvoiceInline(admin.TabularInline):
    model = models.Invoice


class RefundInline(admin.TabularInline):
    model = models.Refund


class TransactionLogInline(admin.TabularInline):
    model = models.AcquiringLog


@admin.register(models.Account)
class AccountAdmin(admin.ModelAdmin):
    inlines = [AccountStatusInline, InvoiceInline]
    list_display = ["user_id", "subscription"]
    search_fields = ["user_id", "subscription"]


@admin.register(models.Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    inlines = [RefundInline, TransactionLogInline]
    list_display = ("id", "amount", "currency", "status")
    search_fields = ("id", "user_id", "subscription_id")
    list_filter = ["currency", "status"]
