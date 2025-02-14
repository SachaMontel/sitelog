import os
import django

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'log.settings')  # Remplacez 'your_project' par le nom de votre projet
django.setup()

from camps.models import Camp 

def create_deadline():
    for camp in Camp.objects.all():
        if camp.branche != 'BP':
            camp.PAF_deadline = '14 février'
            camp.save()
            print(f"DL créé pour {camp}")

def create_mail():
    for camp in Camp.objects.all():
        camp.mail= 'camp.' + camp.numero.replace(' ','').lower() + '@eeif.org'
        camp.save()
        print(f"Mail créé pour {camp}")

create_deadline()