# Generated by Django 4.2.1 on 2023-05-23 14:38

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="VoteCandidate",
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
                ("name", models.CharField(max_length=100)),
                (
                    "phone",
                    phonenumber_field.modelfields.PhoneNumberField(
                        max_length=128, region=None
                    ),
                ),
                ("position", models.CharField(max_length=255, null=True)),
                ("votes", models.PositiveIntegerField(default=10, editable=False)),
                ("password", models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name="Voter",
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
                ("name", models.CharField(max_length=100)),
                ("photo", models.ImageField(upload_to="voters/")),
                (
                    "phone",
                    phonenumber_field.modelfields.PhoneNumberField(
                        max_length=128, region=None
                    ),
                ),
                ("email", models.EmailField(max_length=254)),
                ("bio", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="Nomination",
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
                    "nomination",
                    models.CharField(
                        choices=[
                            ("VER", "За верность профессии"),
                            ("ACT", "За активную жизненную позицию"),
                            ("OBJ", "Мастер объектива"),
                            ("RUR", "Лучшее освещение сельской тематики"),
                            ("SOC", "Лучшее освещение социальной тематики"),
                            ("IND", "Лучшее освещение производственной тематики"),
                            ("SUC", "За первые успехи"),
                            ("WOR", "Лучшая творческая работа года"),
                            ("STY", "За стиль и функциональность"),
                            (
                                "NET",
                                "За лучшее освещение актуальных проблем в социальных сетях",
                            ),
                        ],
                        max_length=3,
                    ),
                ),
                (
                    "voter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="nominations",
                        to="voting.voter",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Material",
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
                ("info", models.TextField()),
                ("links", models.URLField()),
                (
                    "voter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="materials",
                        to="voting.voter",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Vote",
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
                    "nomination",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="voting.nomination",
                    ),
                ),
                (
                    "vote_candidate",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="voting.votecandidate",
                    ),
                ),
                (
                    "voter",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="voting.voter"
                    ),
                ),
            ],
            options={
                "unique_together": {("voter", "nomination")},
            },
        ),
    ]
