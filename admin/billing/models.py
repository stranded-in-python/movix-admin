import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TimestampedModel(BaseModel):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class FinancialMixin(TimestampedModel):
    amount = models.FloatField(_("amount"), null=True)
    currency = models.CharField(_("currency"), max_length=3, null=True)
    transaction_id = models.TextField(_("transaction id"), null=True)

    class Meta:
        abstract = True


class Invoice(FinancialMixin):
    status = models.CharField(_("status"), max_length=20, null=True)
    user_id = models.ForeignKey(
        "Account", on_delete=models.CASCADE, db_column="user_id"
    )
    subscription = models.ForeignKey("Subscription", on_delete=models.CASCADE)
    acquiring_provider = models.TextField(_("acquiring provider"), null=True)
    payment_type = models.CharField(_("payment type"), max_length=20, null=True)

    class Meta:
        managed = False
        db_table = 'payments"."invoice'
        verbose_name = _("Invoice")
        verbose_name_plural = _("Invoices")


class Refund(FinancialMixin):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    status = models.CharField(_("status"), max_length=20, null=True)

    class Meta:
        managed = False
        db_table = 'payments"."refund'
        verbose_name = _("Refund")
        verbose_name_plural = _("Refunds")


class AcquiringLog(BaseModel):
    transaction_id = models.TextField(_("transaction_id"), null=True)
    invoice = models.ForeignKey("Invoice", on_delete=models.CASCADE)
    transaction_type = models.CharField(_("transaction_type"), max_length=20, null=True)
    acq_message = models.TextField(_("acq message"), null=True, db_column="acq_error")
    acq_code = models.IntegerField(_("acq code"), null=True)
    acq_provider = models.TextField(_("acq provider"), null=True)

    class Meta:
        managed = False
        db_table = 'payments"."acq_status_log'
        verbose_name = _("AcquiringLog")
        verbose_name_plural = _("AcquiringLogs")


class Subscription(BaseModel):
    name = models.CharField(_("name"), max_length=255, null=True)

    class Meta:
        managed = False
        db_table = 'subscriptions"."subscription'
        verbose_name = _("Subscription")
        verbose_name_plural = _("Subscriptions")


class Tariff(BaseModel):
    subscription_id = models.ForeignKey(
        Subscription, on_delete=models.CASCADE, db_column="subscription"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField(_("amount"), null=True)
    currency = models.CharField(_("currency"), max_length=3, null=True)

    class Meta:
        managed = False
        db_table = 'subscriptions"."tariff'
        verbose_name = _("Tariff")
        verbose_name_plural = _("Tariffs")


class Account(BaseModel):
    created_at = models.DateTimeField(auto_now_add=True)
    subscription = models.ForeignKey(
        Subscription, on_delete=models.CASCADE, db_column="subscription"
    )
    user_id = models.UUIDField(
        _("user_id"), default=uuid.uuid4, null=True, db_column="user"
    )

    class Meta:
        managed = False
        db_table = 'subscriptions"."account'
        verbose_name = _("Account")
        verbose_name_plural = _("Accounts")


class AccountStatus(BaseModel):
    account_id = models.ForeignKey(
        Account, on_delete=models.CASCADE, db_column="account"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(_("status"), max_length=255, null=True)

    class Meta:
        managed = False
        db_table = 'subscriptions"."account_status'
        verbose_name = _("Account Status")
        verbose_name_plural = _("Accounts Status")
