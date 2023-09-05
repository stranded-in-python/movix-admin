from django.contrib import admin
from notifications import models


class TemplateInline(admin.TabularInline):
    model = models.Template


class ContextInline(admin.TabularInline):
    model = models.Context


@admin.register(models.Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "template", "channels")
    search_fields = ("title", "description", "channels")


@admin.register(models.EventNotification)
class EventNotificationAdmin(admin.ModelAdmin):
    list_display = ("event", "notification")


@admin.register(models.Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "mime_type", "body")
    search_fields = ("name", "mime_type", "id")


@admin.register(models.Context)
class ContextAdmin(admin.ModelAdmin):
    list_display = ("name", "context_vars")


@admin.register(models.NotificationCron)
class NotificationCronAdmin(admin.ModelAdmin):
    list_display = ("notification", "cron_str", "status")
    search_fields = ("notification", "status")
