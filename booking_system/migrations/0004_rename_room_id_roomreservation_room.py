# Generated by Django 4.2 on 2023-04-21 10:33

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("booking_system", "0003_roomreservation"),
    ]

    operations = [
        migrations.RenameField(
            model_name="roomreservation",
            old_name="room_id",
            new_name="room",
        ),
    ]
