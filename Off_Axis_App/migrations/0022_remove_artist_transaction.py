# Generated by Django 5.1.2 on 2025-02-25 22:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("Off_Axis_App", "0021_alter_credittransaction_from_artist_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="artist",
            name="transaction",
        ),
    ]
