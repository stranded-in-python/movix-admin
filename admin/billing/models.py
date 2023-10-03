import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TimestampedModel(BaseModel):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class FinancialMixin(TimestampedModel):
    amount = models.FloatField(_("amount"), null=True)
    currency = models.CharField(_("currency"), max_length=3, null=True)
    transaction_id = models.TextField(_("transaction_id"), null=True)

    class Meta:
        abstract = True


class Invoice(FinancialMixin):
    status = models.CharField(_("status"), max_length=20, null=True)
    user_id = models.UUIDField(_("user_id"), default=uuid.uuid4, null=True)
    subscription_id = models.UUIDField(
        _("subscription_id"), default=uuid.uuid4, null=True
    )
    acquiring_provider = models.TextField(_("acquiring_provider"), null=True)
    payment_type = models.CharField(_("currency"), max_length=20, null=True)

    class Meta:
        db_table = 'payments"."invoice'
        verbose_name = _("Invoice")
        verbose_name_plural = _("Invoices")

    def __str__(self) -> str:
        return str(self.id)


class Refund(FinancialMixin):
    invoice_id = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    status = models.CharField(_("status"), max_length=20, null=True)

    class Meta:
        db_table = 'payments"."refund'
        verbose_name = _("Refund")
        verbose_name_plural = _("Refunds")

    def __str__(self) -> str:
        return str(self.id, "for invoice", self.invoice_id)


class AcquiringLog(BaseModel):
    transaction_id = models.TextField(_("transaction_id"), null=True)
    invoice_id = models.UUIDField(_("invoice_id"), default=uuid.uuid4, null=True)
    transaction_type = models.CharField(_("transaction_type"), max_length=20, null=True)
    acq_message = models.TextField(_("acq_error"), null=True)
    acq_code = models.IntegerField(_("acq_code"), null=True)
    acq_provider = models.TextField(_("acq_provider"), null=True)

    class Meta:
        db_table = 'payments"."acq_status_log'
        verbose_name = _("AcquiringLog")
        verbose_name_plural = _("AcquiringLogs")

    def __str__(self) -> str:
        return str(self.id, "for invoice", self.invoice_id)
