from django.core.management.base import BaseCommand
from camps.models import Camp
from django.db import models


class Command(BaseCommand):
    help = 'Réinitialise tous les attributs des camps sauf numero, branche et mail'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Affiche ce qui sera fait sans modifier la base de données',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        # Liste des champs à conserver
        fields_to_keep = ['numero', 'branche', 'mail', 'id']
        
        # Récupérer tous les camps
        camps = Camp.objects.all()
        total_camps = camps.count()
        
        self.stdout.write(f'Nombre de camps à traiter : {total_camps}')
        
        if dry_run:
            self.stdout.write(self.style.WARNING('Mode DRY-RUN : aucune modification ne sera effectuée'))
        
        for camp in camps:
            self.stdout.write(f'\nTraitement du camp : {camp.numero} ({camp.branche})')
            
            # Sauvegarder les valeurs à conserver
            numero = camp.numero
            branche = camp.branche
            mail = camp.mail
            
            # Réinitialiser tous les champs sauf ceux à conserver
            # Utiliser get_fields() avec include_parents=False pour éviter les relations inverses
            for field in Camp._meta.get_fields(include_parents=False):
                field_name = field.name
                
                # Ignorer les champs à conserver
                if field_name in fields_to_keep:
                    continue
                
                # Ignorer les relations inverses (reverse relations) - elles ont auto_created=True
                if field.auto_created:
                    continue
                
                # Ignorer les relations (ForeignKey, ManyToManyField, OneToOneField)
                if isinstance(field, (models.ForeignKey, models.ManyToManyField, models.OneToOneField)):
                    continue
                
                # Vérifier que le champ existe vraiment sur le modèle
                if not hasattr(Camp, field_name):
                    continue
                
                # Réinitialiser selon le type de champ
                if isinstance(field, models.FileField):
                    # Pour les FileField, on met à None
                    if not dry_run:
                        if getattr(camp, field_name):
                            # Supprimer le fichier s'il existe
                            file_field = getattr(camp, field_name)
                            if file_field:
                                try:
                                    file_field.delete(save=False)
                                except:
                                    pass
                            setattr(camp, field_name, None)
                elif isinstance(field, models.CharField) or isinstance(field, models.TextField):
                    # Pour les champs texte, on met à la valeur par défaut ou ''/None
                    if not dry_run:
                        if hasattr(field, 'default') and field.default != models.NOT_PROVIDED:
                            setattr(camp, field_name, field.default() if callable(field.default) else field.default)
                        else:
                            setattr(camp, field_name, '' if field.blank else None)
                elif isinstance(field, models.DateField) or isinstance(field, models.DateTimeField):
                    # Pour les dates, on met à None
                    if not dry_run:
                        setattr(camp, field_name, None)
                elif isinstance(field, models.IntegerField) or isinstance(field, models.BooleanField):
                    # Pour les entiers et booléens, on met à la valeur par défaut ou None/0/False
                    if not dry_run:
                        if hasattr(field, 'default') and field.default != models.NOT_PROVIDED:
                            setattr(camp, field_name, field.default() if callable(field.default) else field.default)
                        elif field.null:
                            setattr(camp, field_name, None)
                        else:
                            setattr(camp, field_name, 0 if isinstance(field, models.IntegerField) else False)
                else:
                    # Pour les autres types, on met à None si possible
                    if not dry_run:
                        if field.null:
                            setattr(camp, field_name, None)
            
            # Restaurer les valeurs à conserver
            if not dry_run:
                camp.numero = numero
                camp.branche = branche
                camp.mail = mail
                camp.save()
                self.stdout.write(self.style.SUCCESS(f'  ✓ Camp {camp.numero} réinitialisé'))
            else:
                self.stdout.write(f'  [DRY-RUN] Camp {camp.numero} serait réinitialisé')
        
        if dry_run:
            self.stdout.write(self.style.WARNING('\nMode DRY-RUN terminé. Utilisez sans --dry-run pour appliquer les modifications.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'\n✓ {total_camps} camps réinitialisés avec succès !'))
