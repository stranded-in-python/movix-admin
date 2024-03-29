from billing import models
from django.contrib import admin


class ReadonlyInline(admin.TabularInline):
    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_model_perms(self, request, obj):
        return {'view': True}


class InvoiceInline(ReadonlyInline):
    model = models.Invoice
    readonly_fields = [
        "status",
        "user_id",
        "subscription",
        "acquiring_provider",
        "payment_type",
        "amount",
        "currency",
        "transaction_id",
    ]


class RefundInline(ReadonlyInline):
    model = models.Refund


class TransactionLogInline(ReadonlyInline):
    model = models.AcquiringLog


class AccountStatusInline(admin.TabularInline):
    model = models.AccountStatus
    fields = ["status"]


@admin.register(models.Account)
class AccountAdmin(admin.ModelAdmin):
    inlines = [AccountStatusInline, InvoiceInline]
    list_display = ["user_id", "subscription"]
    search_fields = ["user_id", "subscription"]


@admin.register(models.Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    actions = None
    inlines = [RefundInline, TransactionLogInline]
    list_display = ("id", "amount", "currency", "status")
    search_fields = ("id", "user_id", "subscription_id")
    list_filter = ["currency", "status"]
    readonly_fields = [
        "status",
        "user_id",
        "subscription",
        "acquiring_provider",
        "payment_type",
        "amount",
        "currency",
        "transaction_id",
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_model_perms(self, request):
        return {'view': True}
