# Generated by Django 5.1.6 on 2025-02-24 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('camps', '0031_alter_camp_budget_deadline'),
    ]

    operations = [
        migrations.AddField(
            model_name='camp',
            name='Budgereal_etat',
            field=models.CharField(blank=True, choices=[('Rendu', 'Rendu'), ('Validé', 'Validé'), ('Refusé', 'Refusé'), ('Non rendu', 'Non rendu'), ('Retour fait', 'Retour fait'), ('En cours', 'En cours')], default='Non rendu', max_length=50, null=True, verbose_name='État du budget'),
        ),
        migrations.AddField(
            model_name='camp',
            name='Budgetreal',
            field=models.FileField(blank=True, null=True, upload_to='media/fichiers_camps/Budgetreal/'),
        ),
        migrations.AddField(
            model_name='camp',
            name='Budgetreal_commentaire',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Commentaire du budget'),
        ),
        migrations.AddField(
            model_name='camp',
            name='Budgetreal_deadline',
            field=models.CharField(blank=True, default='Debut mai', max_length=50, null=True, verbose_name='Date limite du budget'),
        ),
    ]
