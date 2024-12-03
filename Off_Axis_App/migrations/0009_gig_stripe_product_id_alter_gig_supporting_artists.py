# Generated by Django 5.1.2 on 2024-12-01 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Off_Axis_App", "0008_gig_is_approved"),
    ]

    operations = [
        migrations.AddField(
            model_name="gig",
            name="stripe_product_id",
            field=models.TextField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name="gig",
            name="supporting_artists",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="supporting_artists",
                to="Off_Axis_App.artist",
            ),
        ),
    ]
