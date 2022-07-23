# Generated by Django 4.0.6 on 2022-07-23 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email_verified',
            field=models.BooleanField(default=False, help_text="Designates whether this user's email is verified.", verbose_name='active'),
        ),
    ]
