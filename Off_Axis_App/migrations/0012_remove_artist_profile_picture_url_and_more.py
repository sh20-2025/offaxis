# Generated by Django 5.1.2 on 2024-12-04 00:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Off_Axis_App", "0011_contactinformation"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name="artist",
            name="profile_picture_url",
        ),
        migrations.AddField(
            model_name="artist",
            name="profile_picture",
            field=models.ImageField(blank=True, upload_to="profile_pictures/"),
        ),
        migrations.AlterField(
            model_name="artist",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="artist",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="gig",
            name="artist",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="gigs",
                to="Off_Axis_App.artist",
            ),
        ),
        migrations.CreateModel(
            name="Festival",
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
                ("name", models.TextField(max_length=256)),
                ("description", models.TextField(max_length=1024)),
                ("start_date", models.DateTimeField()),
                ("end_date", models.DateTimeField()),
                ("youtube_video_url", models.URLField(blank=True)),
                ("slug", models.SlugField(default="", unique=True)),
                ("is_active", models.BooleanField(default=True)),
                ("festival_photo_url", models.URLField(blank=True)),
                (
                    "artists",
                    models.ManyToManyField(blank=True, to="Off_Axis_App.artist"),
                ),
            ],
        ),
    ]
