# Generated by Django 5.1.6 on 2025-02-24 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('camps', '0026_alter_camp_grille_intendance_deadline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='camp',
            name='fiche_sncf_deadline',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Date limite de la fiche SNCF'),
        ),
    ]
