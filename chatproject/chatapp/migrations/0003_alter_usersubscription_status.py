# Generated by Django 5.1.4 on 2025-01-10 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chatapp", "0002_alter_usersubscription_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usersubscription",
            name="status",
            field=models.CharField(
                choices=[
                    ("active", "Active"),
                    ("inactive", "Inactive"),
                    ("cancelled", "Cancelled"),
                ],
                default="active",
                max_length=50,
            ),
        ),
    ]
