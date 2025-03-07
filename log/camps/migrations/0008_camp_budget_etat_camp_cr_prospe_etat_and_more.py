# Generated by Django 5.1.4 on 2025-01-06 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('camps', '0007_alter_camp_budget_alter_camp_cr_prospe_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='camp',
            name='Budget_etat',
            field=models.CharField(blank=True, choices=[('Rendu', 'Rendu'), ('Validé', 'Validé'), ('Refusé', 'Refusé'), ('Non rendu', 'Non rendu')], default='Non rendu', max_length=50, null=True, verbose_name='État du budget'),
        ),
        migrations.AddField(
            model_name='camp',
            name='CR_prospe_etat',
            field=models.CharField(blank=True, choices=[('Rendu', 'Rendu'), ('Validé', 'Validé'), ('Refusé', 'Refusé'), ('Non rendu', 'Non rendu')], default='Non rendu', max_length=50, null=True, verbose_name='État du CR prospection'),
        ),
        migrations.AddField(
            model_name='camp',
            name='chemins_explo_etat',
            field=models.CharField(blank=True, choices=[('Rendu', 'Rendu'), ('Validé', 'Validé'), ('Refusé', 'Refusé'), ('Non rendu', 'Non rendu')], default='Non rendu', max_length=50, null=True, verbose_name="État des chemins d'exploitation"),
        ),
        migrations.AddField(
            model_name='camp',
            name='contrat_location_etat',
            field=models.CharField(blank=True, choices=[('Rendu', 'Rendu'), ('Validé', 'Validé'), ('Refusé', 'Refusé'), ('Non rendu', 'Non rendu')], default='Non rendu', max_length=50, null=True, verbose_name='État du contrat de location'),
        ),
        migrations.AddField(
            model_name='camp',
            name='fiche_sncf_etat',
            field=models.CharField(blank=True, choices=[('Rendu', 'Rendu'), ('Validé', 'Validé'), ('Refusé', 'Refusé'), ('Non rendu', 'Non rendu')], default='Non rendu', max_length=50, null=True, verbose_name='État de la fiche SNCF'),
        ),
        migrations.AddField(
            model_name='camp',
            name='fil_bleu_etat',
            field=models.CharField(blank=True, choices=[('Rendu', 'Rendu'), ('Validé', 'Validé'), ('Refusé', 'Refusé'), ('Non rendu', 'Non rendu')], default='Non rendu', max_length=50, null=True, verbose_name='État du fil bleu'),
        ),
        migrations.AddField(
            model_name='camp',
            name='fil_rouge_etat',
            field=models.CharField(blank=True, choices=[('Rendu', 'Rendu'), ('Validé', 'Validé'), ('Refusé', 'Refusé'), ('Non rendu', 'Non rendu')], default='Non rendu', max_length=50, null=True, verbose_name='État du fil rouge'),
        ),
        migrations.AddField(
            model_name='camp',
            name='fil_vert_etat',
            field=models.CharField(blank=True, choices=[('Rendu', 'Rendu'), ('Validé', 'Validé'), ('Refusé', 'Refusé'), ('Non rendu', 'Non rendu')], default='Non rendu', max_length=50, null=True, verbose_name='État du fil vert'),
        ),
        migrations.AddField(
            model_name='camp',
            name='grille_assurance_etat',
            field=models.CharField(blank=True, choices=[('Rendu', 'Rendu'), ('Validé', 'Validé'), ('Refusé', 'Refusé'), ('Non rendu', 'Non rendu')], default='Non rendu', max_length=50, null=True, verbose_name="État de la grille d'assurance"),
        ),
        migrations.AddField(
            model_name='camp',
            name='grille_ddcs_etat',
            field=models.CharField(blank=True, choices=[('Rendu', 'Rendu'), ('Validé', 'Validé'), ('Refusé', 'Refusé'), ('Non rendu', 'Non rendu')], default='Non rendu', max_length=50, null=True, verbose_name='État de la grille DDCS'),
        ),
        migrations.AddField(
            model_name='camp',
            name='grille_intendance_etat',
            field=models.CharField(blank=True, choices=[('Rendu', 'Rendu'), ('Validé', 'Validé'), ('Refusé', 'Refusé'), ('Non rendu', 'Non rendu')], default='Non rendu', max_length=50, null=True, verbose_name='État de la grille intendance'),
        ),
        migrations.AddField(
            model_name='camp',
            name='procuration_banque_etat',
            field=models.CharField(blank=True, choices=[('Rendu', 'Rendu'), ('Validé', 'Validé'), ('Refusé', 'Refusé'), ('Non rendu', 'Non rendu')], default='Non rendu', max_length=50, null=True, verbose_name='État de la procuration bancaire'),
        ),
        migrations.AddField(
            model_name='camp',
            name='recepisse_etat',
            field=models.CharField(blank=True, choices=[('Rendu', 'Rendu'), ('Validé', 'Validé'), ('Refusé', 'Refusé'), ('Non rendu', 'Non rendu')], default='Non rendu', max_length=50, null=True, verbose_name='État du récépissé'),
        ),
        migrations.AlterField(
            model_name='camp',
            name='numero',
            field=models.CharField(blank=True, choices=[('BC 1', 'BC 1'), ('BC 2', 'BC 2'), ('BC 3', 'BC 3'), ('BC 4', 'BC 4'), ('BC 5', 'BC 5'), ('BC 6', 'BC 6'), ('BC 7', 'BC 7'), ('BC 8', 'BC 8'), ('BC 9', 'BC 9'), ('BC 10', 'BC 10'), ('BC 11', 'BC 11'), ('BC 12', 'BC 12'), ('BC 13', 'BC 13'), ('BC 14', 'BC 14'), ('BC 15', 'BC 15'), ('BC 16', 'BC 16'), ('BC 17', 'BC 17'), ('BC 18', 'BC 18'), ('BC 19', 'BC 19'), ('BC 20', 'BC 20'), ('BC 21', 'BC 21'), ('BC 22', 'BC 22'), ('BC 23', 'BC 23'), ('BC 24', 'BC 24'), ('BC 25', 'BC 25'), ('BM 1', 'BM 1'), ('BM 2', 'BM 2'), ('BM 3', 'BM 3'), ('BM 4', 'BM 4'), ('BM 5', 'BM 5'), ('BM 6', 'BM 6'), ('BM 7', 'BM 7'), ('BM 8', 'BM 8'), ('BM 9', 'BM 9'), ('BM 10', 'BM 10'), ('BM 11', 'BM 11'), ('BM 12', 'BM 12'), ('BM 13', 'BM 13'), ('BM 14', 'BM 14'), ('BM 15', 'BM 15'), ('BM 16', 'BM 16'), ('BM 17', 'BM 17'), ('BM 18', 'BM 18'), ('BM 19', 'BM 19'), ('BM 20', 'BM 20'), ('BM 21', 'BM 21'), ('BM 22', 'BM 22'), ('BM 23', 'BM 23'), ('BM 24', 'BM 24'), ('BM 25', 'BM 25'), ('BP 1', 'BP 1'), ('BP 2', 'BP 2'), ('BP 3', 'BP 3'), ('BP 4', 'BP 4'), ('BP 5', 'BP 5'), ('BP 6', 'BP 6'), ('BP 7', 'BP 7'), ('BP 8', 'BP 8'), ('BP 9', 'BP 9'), ('BP 10', 'BP 10')], max_length=30, null=True, unique=True, verbose_name='Numéro du camp'),
        ),
    ]
