from billing import models
from django.contrib import admin


class TariffInline(admin.TabularInline):
    model = models.Tariff


class AccountInline(admin.TabularInline):
    model = models.Account


class InvoiceInline(admin.TabularInline):
    model = models.Invoice


class RefundInline(admin.TabularInline):
    model = models.Refund


@admin.register(models.Subscription)
class SubsAdmin(admin.ModelAdmin):
    inlines = [TariffInline, AccountInline, InvoiceInline]
    list_display = ("id", "name")


@admin.register(models.Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    inlines = [RefundInline]
    list_display = ("id", "amount", "currency", "status")
    search_fields = ("id", "user_id", "subscription_id")
    list_filter = ["currency", "status"]
