# Generated by Django 5.1.2 on 2024-12-02 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Off_Axis_App", "0010_alter_gig_supporting_artists"),
    ]

    operations = [
        migrations.CreateModel(
            name="ContactInformation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=50)),
                ("last_name", models.CharField(max_length=50)),
                ("email", models.EmailField(max_length=254)),
                ("message_content", models.TextField(max_length=2000)),
                (
                    "message_type",
                    models.CharField(
                        choices=[
                            ("general_question", "General Question"),
                            ("cant_find_tickets", "I can't find my tickets"),
                            ("ticket_query", "Ticket Query"),
                            ("press_enquiry", "Press Enquiry"),
                        ],
                        max_length=20,
                    ),
                ),
            ],
        ),
    ]
