# Generated by Django 3.2.3 on 2025-02-15 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='media/avatars/'),
        ),
    ]
