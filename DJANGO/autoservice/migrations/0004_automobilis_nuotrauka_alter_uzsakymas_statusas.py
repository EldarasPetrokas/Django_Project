# Generated by Django 5.1.3 on 2024-12-06 09:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("autoservice", "0003_uzsakymas_statusas"),
    ]

    operations = [
        migrations.AddField(
            model_name="automobilis",
            name="nuotrauka",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="automobiliai/",
                verbose_name="Nuotrauka",
            ),
        ),
        migrations.AlterField(
            model_name="uzsakymas",
            name="statusas",
            field=models.CharField(
                choices=[
                    ("nepradetas", "Nepradėtas"),
                    ("vykdomas", "Vykdomas"),
                    ("uzbaigtas", "Užbaigtas"),
                    ("atsauktas", "Atšauktas"),
                ],
                default="nepradetas",
                max_length=20,
            ),
        ),
    ]