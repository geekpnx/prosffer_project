# Generated by Django 5.0.6 on 2024-10-14 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Product",
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
                (
                    "store",
                    models.CharField(
                        choices=[
                            ("aldi süd", "Aldi Süd"),
                            ("netto", "Netto"),
                            ("kaufland", "Kaufland"),
                        ],
                        max_length=30,
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "description",
                    models.CharField(blank=True, max_length=150, null=True),
                ),
                ("price", models.FloatField()),
                ("currency", models.CharField(max_length=5)),
                ("category", models.CharField(blank=True, max_length=100, null=True)),
                ("image", models.URLField(max_length=255)),
                ("link", models.URLField(max_length=255)),
                ("id_tag", models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
    ]
