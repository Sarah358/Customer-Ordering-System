# Generated by Django 4.2.5 on 2023-09-12 06:36

import uuid

import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "pkid",
                    models.BigAutoField(editable=False, primary_key=True, serialize=False),
                ),
                (
                    "id",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now_add=True)),
                (
                    "phone_number",
                    phonenumber_field.modelfields.PhoneNumberField(
                        default="+254799757242",
                        max_length=30,
                        region=None,
                        verbose_name="Phone number",
                    ),
                ),
                (
                    "profile_photo",
                    models.ImageField(
                        default="/profile_default.png",
                        upload_to="",
                        verbose_name="profile photo",
                    ),
                ),
                (
                    "city",
                    models.CharField(default="Nairobi", max_length=180, verbose_name="City"),
                ),
                (
                    "address",
                    models.CharField(default="Roysambu", max_length=180, verbose_name="Address"),
                ),
            ],
        ),
    ]
