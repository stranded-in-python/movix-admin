# Generated by Django 3.2 on 2023-09-10 13:00

from django.db import migrations, models
import django_jsonform.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0007_auto_20230909_0944'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='context',
            name='context_vars_editable',
        ),
        migrations.AlterField(
            model_name='context',
            name='context_vars',
            field=django_jsonform.models.fields.JSONField(),
        ),
        migrations.AlterField(
            model_name='eventnotification',
            name='event',
            field=models.CharField(choices=[('Registered', 'registered')], max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='channels',
            field=django_jsonform.models.fields.JSONField(),
        ),
        migrations.AlterField(
            model_name='notificationcron',
            name='status',
            field=models.CharField(choices=[('In progress', 'in_progress'), ('Pending', 'pending')], default='Pending', max_length=255),
        ),
        migrations.AlterField(
            model_name='notificationsettings',
            name='email_disabled',
            field=models.JSONField(verbose_name='No email for them'),
        ),
        migrations.AlterField(
            model_name='template',
            name='mime_type',
            field=models.CharField(choices=[('HTML', 'text/html'), ('Текст', 'text/plain')], max_length=255, verbose_name='Template media type'),
        ),
        migrations.AlterField(
            model_name='usersettings',
            name='default',
            field=models.CharField(choices=[('Адрес электронной почты', 'email')], max_length=255),
        ),
    ]