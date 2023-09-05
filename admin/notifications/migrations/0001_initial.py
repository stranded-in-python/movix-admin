# Generated by Django 3.2 on 2023-09-05 16:42

from django.db import migrations, models
import django.db.models.deletion
import notifications.utils
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.RunSQL(
            sql="CREATE SCHEMA IF NOT EXISTS notifications;",
            reverse_sql="DROP SCHEMA IF EXISTS notifications;",
        ),
        migrations.CreateModel(
            name='Context',
            fields=[
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('context_vars', models.JSONField()),
            ],
            options={
                'verbose_name': 'Context',
                'verbose_name_plural': 'Contexts',
                'db_table': 'notifications"."context',
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('channels', models.JSONField()),
            ],
            options={
                'verbose_name': 'Notification',
                'verbose_name_plural': 'Notifications',
                'db_table': 'notifications"."notification',
            },
        ),
        migrations.CreateModel(
            name='UserSettings',
            fields=[
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.UUIDField(unique=True)),
                (
                    'default',
                    models.CharField(choices=[('email', 'Email')], max_length=255),
                ),
                ('email_enabled', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'UserSettings',
                'verbose_name_plural': 'UsersSettings',
                'db_table': 'notifications"."user_settings',
            },
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                (
                    'mime_type',
                    models.CharField(
                        choices=[
                            ('text/html', 'Text Html'),
                            ('text/plain', 'Text Plain'),
                        ],
                        max_length=255,
                    ),
                ),
                ('body', models.FileField(upload_to=notifications.utils.template_path)),
                (
                    'context',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='notifications.context',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Template',
                'verbose_name_plural': 'Templates',
                'db_table': 'notifications"."template',
            },
        ),
        migrations.CreateModel(
            name='NotificationSettings',
            fields=[
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('email_disabled', models.JSONField()),
                (
                    'notification',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='notifications.notification',
                    ),
                ),
            ],
            options={
                'verbose_name': 'NotificationSettings',
                'verbose_name_plural': 'NotificationsSettings',
                'db_table': 'notifications"."notification_settings',
            },
        ),
        migrations.CreateModel(
            name='NotificationCron',
            fields=[
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cron_str', models.CharField(max_length=6)),
                (
                    'status',
                    models.CharField(
                        choices=[
                            ('in_progress', 'In Progress'),
                            ('pending', 'Pending'),
                        ],
                        default='pending',
                        max_length=255,
                    ),
                ),
                (
                    'notification',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='notifications.notification',
                    ),
                ),
            ],
            options={
                'verbose_name': 'NotificationCron',
                'verbose_name_plural': 'NotificationCrons',
                'db_table': 'notifications"."notification_cron',
            },
        ),
        migrations.AddField(
            model_name='notification',
            name='template',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to='notifications.template'
            ),
        ),
        migrations.CreateModel(
            name='EventNotification',
            fields=[
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                (
                    'event',
                    models.CharField(
                        choices=[('registered', 'Registered')],
                        max_length=255,
                        unique=True,
                    ),
                ),
                (
                    'notification',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='notifications.notification',
                    ),
                ),
            ],
            options={
                'verbose_name': 'EventNotification',
                'verbose_name_plural': 'EventNotifications',
                'db_table': 'notifications"."event_notification',
            },
        ),
    ]
