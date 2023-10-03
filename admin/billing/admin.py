from billing import models
from django.contrib import admin


@admin.register(models.Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "amount", "currency", "status")
    search_fields = ("id", "user_id", "amount")


@admin.register(models.Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ("id", "amount", "currency", "status")
    search_fields = ("id", "invoice_id", "amount")


@admin.register(models.AcquiringLog)
class AcqiringLogAdmin(admin.ModelAdmin):
    list_display = ("transaction_id", "invoice_id", "acq_provider", "acq_message")
    search_fields = ("transaction_id", "invoice_id", "acq_provider")
