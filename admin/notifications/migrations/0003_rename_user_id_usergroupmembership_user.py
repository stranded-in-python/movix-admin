# Generated by Django 3.2 on 2023-09-07 19:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_auto_20230907_1249'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usergroupmembership',
            old_name='user_id',
            new_name='user',
        ),
    ]