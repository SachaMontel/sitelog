from django.core.management.base import BaseCommand
from camps.models import Camp
import re


class Command(BaseCommand):
    help = 'Met à jour les adresses email de tous les camps au format camp2026.{branche}{numero}@eeif.org'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Affiche ce qui sera fait sans modifier la base de données',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        # Récupérer tous les camps
        camps = Camp.objects.all()
        total_camps = camps.count()
        
        self.stdout.write(f'Nombre de camps à traiter : {total_camps}')
        
        if dry_run:
            self.stdout.write(self.style.WARNING('Mode DRY-RUN : aucune modification ne sera effectuée'))
        
        updated_count = 0
        skipped_count = 0
        
        for camp in camps:
            if not camp.numero:
                self.stdout.write(self.style.WARNING(f'  ⚠ Camp sans numéro (ID: {camp.id}) - ignoré'))
                skipped_count += 1
                continue
            
            # Extraire la branche et le numéro depuis le champ numero
            # Format attendu : "BC 1", "BM 1", "BB 1", "BP 1", etc.
            match = re.match(r'^([A-Z]+)\s+(\d+)$', camp.numero)
            
            if not match:
                self.stdout.write(self.style.WARNING(f'  ⚠ Format de numéro invalide pour {camp.numero} (ID: {camp.id}) - ignoré'))
                skipped_count += 1
                continue
            
            branche = match.group(1).lower()  # "BC" -> "bc"
            numero = match.group(2)  # "1" -> "1"
            
            # Générer la nouvelle adresse email
            new_email = f'camp2026.{branche}{numero}@eeif.org'
            
            old_email = camp.mail or '(vide)'
            
            if dry_run:
                self.stdout.write(f'  [DRY-RUN] Camp {camp.numero}: {old_email} → {new_email}')
                updated_count += 1
            else:
                camp.mail = new_email
                camp.save()
                self.stdout.write(self.style.SUCCESS(f'  ✓ Camp {camp.numero}: {old_email} → {new_email}'))
                updated_count += 1
        
        if dry_run:
            self.stdout.write(self.style.WARNING(f'\nMode DRY-RUN terminé.'))
            self.stdout.write(f'  - {updated_count} camps seraient mis à jour')
            self.stdout.write(f'  - {skipped_count} camps ignorés')
            self.stdout.write(self.style.WARNING('Utilisez sans --dry-run pour appliquer les modifications.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'\n✓ {updated_count} camps mis à jour avec succès !'))
            if skipped_count > 0:
                self.stdout.write(self.style.WARNING(f'  ⚠ {skipped_count} camps ignorés'))
