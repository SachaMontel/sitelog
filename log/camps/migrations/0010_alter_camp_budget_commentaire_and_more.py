# Generated by Django 5.1.4 on 2025-01-07 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('camps', '0009_camp_budget_commentaire_camp_cr_prospe_commentaire_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='camp',
            name='Budget_commentaire',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Commentaire du budget'),
        ),
        migrations.AlterField(
            model_name='camp',
            name='CR_prospe_commentaire',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Commentaire du CR prospection'),
        ),
        migrations.AlterField(
            model_name='camp',
            name='chemins_explo_commentaire',
            field=models.TextField(blank=True, default='', null=True, verbose_name="Commentaire des chemins d'exploitation"),
        ),
        migrations.AlterField(
            model_name='camp',
            name='contrat_location_commentaire',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Commentaire du contrat de location'),
        ),
        migrations.AlterField(
            model_name='camp',
            name='fiche_sncf_commentaire',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Commentaire de la fiche SNCF'),
        ),
        migrations.AlterField(
            model_name='camp',
            name='fil_bleu_commentaire',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Commentaire du fil bleu'),
        ),
        migrations.AlterField(
            model_name='camp',
            name='fil_rouge_commentaire',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Commentaire du fil rouge'),
        ),
        migrations.AlterField(
            model_name='camp',
            name='fil_vert_commentaire',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Commentaire du fil vert'),
        ),
        migrations.AlterField(
            model_name='camp',
            name='grille_assurance_commentaire',
            field=models.TextField(blank=True, default='', null=True, verbose_name="Commentaire de la grille d'assurance"),
        ),
        migrations.AlterField(
            model_name='camp',
            name='grille_ddcs_commentaire',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Commentaire de la grille DDCS'),
        ),
        migrations.AlterField(
            model_name='camp',
            name='grille_intendance_commentaire',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Commentaire de la grille intendance'),
        ),
        migrations.AlterField(
            model_name='camp',
            name='procuration_banque_commentaire',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Commentaire de la procuration bancaire'),
        ),
        migrations.AlterField(
            model_name='camp',
            name='recepisse_commentaire',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Commentaire du récépissé'),
        ),
    ]
