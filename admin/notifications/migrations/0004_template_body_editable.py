# Generated by Django 3.2 on 2023-09-08 09:11

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0003_rename_user_id_usergroupmembership_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='template',
            name='body_editable',
            field=ckeditor.fields.RichTextField(null=True),
        ),
    ]