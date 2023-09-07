import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from notifications import enums, utils


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TimestampedModel(BaseModel):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Context(TimestampedModel):
    name = models.CharField(max_length=255)
    context_vars = models.JSONField()

    class Meta:
        db_table = 'notifications"."context'
        verbose_name = _("Context")
        verbose_name_plural = _("Contexts")


class Template(TimestampedModel):
    name = models.CharField(max_length=255)
    mime_type = models.CharField(max_length=255, choices=enums.MimeType.choices)
    body = models.FileField(upload_to=utils.template_path)
    context = models.ForeignKey(Context, on_delete=models.CASCADE)

    class Meta:
        db_table = 'notifications"."template'
        verbose_name = _("Template")
        verbose_name_plural = _("Templates")


class Notification(TimestampedModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    channels = models.JSONField()

    class Meta:
        db_table = 'notifications"."notification'
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")


class EventNotification(TimestampedModel):
    event = models.CharField(unique=True, max_length=255, choices=enums.Event.choices)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)

    class Meta:
        db_table = 'notifications"."event_notification'
        verbose_name = _("EventNotification")
        verbose_name_plural = _("EventNotifications")


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        managed = False
        db_table = 'users"."user'


class UserGroup(TimestampedModel):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'notifications"."user_group'
        verbose_name = _("UserGroup")
        verbose_name_plural = _("UserGroups")


class UserGroupMembership(TimestampedModel):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(UserGroup, on_delete=models.CASCADE)

    class Meta:
        db_table = 'notifications"."user_group_membership'
        verbose_name = _("UserGroupMembership")
        verbose_name_plural = _("UserGroupMemberships")


class UserSettings(TimestampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    default = models.CharField(
        max_length=255, choices=enums.NotificationChannels.choices
    )
    email_enabled = models.BooleanField(default=True)  # type: ignore

    class Meta:
        db_table = 'notifications"."user_settings'
        verbose_name = _("UserSettings")
        verbose_name_plural = _("UsersSettings")


class NotificationSettings(TimestampedModel):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    email_disabled = models.JSONField()  # type: ignore

    class Meta:
        db_table = 'notifications"."notification_settings'
        verbose_name = _("NotificationSettings")
        verbose_name_plural = _("NotificationsSettings")


class NotificationCron(TimestampedModel):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    cron_str = models.CharField(max_length=6)
    status = models.CharField(
        max_length=255, choices=enums.Status.choices, default=enums.Status.PENDING
    )

    class Meta:
        db_table = 'notifications"."notification_cron'
        verbose_name = _("NotificationCron")
        verbose_name_plural = _("NotificationCrons")
