import logging

import backoff
import httpx
from django.conf import settings
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from notifications import enums, forms, models


class UserGroupMembershipInline(admin.TabularInline):
    model = models.UserGroupMembership


@backoff.on_exception(backoff.expo, httpx.HTTPError, max_tries=5)
def send_notification(notification_id: str):
    httpx.post(f"{settings.NOTIFICATIONS_URL}/{notification_id}")


@admin.action(description=_("Send notifications"))
def send_notifications(modeladmin, request, queryset):  # type: ignore
    for notification in queryset:
        try:
            send_notification(str(notification.id))
        except httpx.HTTPError:
            logging.exception("Failed to send notification: %s", notification.id)


@admin.register(models.Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "template", "channels")
    search_fields = ("title", "description", "channels")
    actions = [send_notifications]


@admin.register(models.EventNotification)
class EventNotificationAdmin(admin.ModelAdmin):
    list_display = ("event", "notification")


@admin.register(models.Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "mime_type")
    search_fields = ("name", "mime_type", "id")
    form = forms.TemplateAdminForm


@admin.register(models.UserGroup)
class UserGroupAdmin(admin.ModelAdmin):
    inlines = (UserGroupMembershipInline,)

    list_dispaly = ("name",)
    search_fields = ("name",)


@admin.register(models.Context)
class ContextAdmin(admin.ModelAdmin):
    fields = ("name", "context_vars")
    list_display = ("name",)


@admin.action(description=_("Mark as to be removed"))
def mark_as_stale(modeladmin, request, queryset):  # type: ignore
    for cron in queryset:
        cron.status = enums.Status.STALE
        cron.save()


@admin.register(models.NotificationCron)
class NotificationCronAdmin(admin.ModelAdmin):
    list_display = ("notification", "cron_str", "status")
    search_fields = ("notification", "status")
    exclude = ("status",)
    actions = [mark_as_stale]

    # Disabling simple delete to avoid CRON hoarding
    def has_delete_permission(self, request, obj=None):
        return False
