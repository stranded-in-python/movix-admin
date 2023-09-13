import os
import uuid

from cronfield.models import CronField
from django import dispatch
from django.core.files.base import ContentFile
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _
from django_jsonform.models.fields import JSONField
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
    CONTEXT_VARS_SCHEMA = {
        "type": "object",
        "properties": {
            key: {"type": "string"} for key, _ in enums.ContextVariables.choices
        },
    }
    name = models.CharField(_("Name"), max_length=255)
    context_vars = JSONField(schema=CONTEXT_VARS_SCHEMA)

    class Meta:
        db_table = 'notifications"."context'
        verbose_name = _("Context")
        verbose_name_plural = _("Contexts")

    def __str__(self) -> str:
        return str(self.name)


class Template(TimestampedModel):
    name = models.CharField(_("Template name"), max_length=255)
    mime_type = models.CharField(
        _("Template media type"), max_length=255, choices=enums.MimeType.choices
    )
    # dirty hack to easily edit the body
    body_editable = models.TextField(_("Template body"), null=True)
    body = models.FileField(upload_to=utils.template_path)  # type: ignore
    context = models.ForeignKey(Context, on_delete=models.CASCADE)

    class Meta:
        db_table = 'notifications"."template'
        verbose_name = _("Template")
        verbose_name_plural = _("Templates")

    def __str__(self) -> str:
        return str(self.name)

    def save(self, *args, **kwargs):
        # store body_editable in body
        if self.body_editable:  # check if body_editable is not empty
            content = str(self.body_editable).encode("utf-8")
            file_name = (
                slugify(self.name)
                + "."
                + utils.get_file_extension_by_mime_type(str(self.mime_type))
            )  # create a file name from the name field
            self.body = ContentFile(
                content, name=file_name
            )  # save the file to the body field
        super().save(*args, **kwargs)  # call the parent save method


@dispatch.receiver(models.signals.post_delete, sender=Template)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Document` object is deleted.
    """
    if instance.body:
        if os.path.isfile(instance.body.path):
            os.remove(instance.body.path)


class ActiveUserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_verified=True)


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(unique=True, max_length=20)
    is_verified = models.BooleanField()
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    objects = ActiveUserManager()

    class Meta:
        managed = False
        db_table = 'notifications"."user'

    def __str__(self) -> str:
        return str(self.username)


class UserGroup(TimestampedModel):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'notifications"."user_group'
        verbose_name = _("UserGroup")
        verbose_name_plural = _("UserGroups")

    def __str__(self) -> str:
        return str(self.name)


class UserGroupMembership(TimestampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(UserGroup, on_delete=models.CASCADE)

    class Meta:
        db_table = 'notifications"."user_group_membership'
        verbose_name = _("UserGroupMembership")
        verbose_name_plural = _("UserGroupMemberships")

    def __str__(self) -> str:
        return f"Group: {self.group}, User: {self.user}"


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


class Notification(TimestampedModel):
    CHANNELS_SCHEMA = {
        "type": "array",
        "items": {
            "type": "string",
            "choices": [
                {"title": title, "value": value}
                for value, title in enums.NotificationChannels.choices
            ],
            "widget": "multiselect",
        },
    }
    title = models.CharField(max_length=255)
    description = models.TextField()
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    channels = JSONField(schema=CHANNELS_SCHEMA)
    recipients = models.ForeignKey(UserGroup, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'notifications"."notification'
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")

    def __str__(self) -> str:
        return str(self.title)


class EventNotification(TimestampedModel):
    event = models.CharField(unique=True, max_length=255, choices=enums.Event.choices)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)

    class Meta:
        db_table = 'notifications"."event_notification'
        verbose_name = _("EventNotification")
        verbose_name_plural = _("EventNotifications")


class NotificationSettings(TimestampedModel):

    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    email_disabled = models.JSONField(_("No email for them"))

    class Meta:
        db_table = 'notifications"."notification_settings'
        verbose_name = _("NotificationSettings")
        verbose_name_plural = _("NotificationsSettings")


class NotificationCron(TimestampedModel):
    # Instead of just deleting an entry,
    # we mark it as enums.Status.STALE to be deleted later by scheduler
    notification = models.ForeignKey(Notification, on_delete=models.DO_NOTHING)
    cron_str = CronField(_("Cron"))
    status = models.CharField(
        max_length=255, choices=enums.Status.choices, default=enums.Status.PENDING
    )

    class Meta:
        db_table = 'notifications"."notification_cron'
        verbose_name = _("NotificationCron")
        verbose_name_plural = _("NotificationCrons")

    def __str__(self) -> str:
        return str(self.notification)

    # Instead of just deleting an entry,
    # we mark it as enums.Status.STALE to be deleted later by scheduler
    def delete(self, *args, **kwargs):
        self.status = enums.Status.STALE
        self.save()
