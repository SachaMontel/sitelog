import os
import django

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'log.settings')  # Remplacez 'your_project' par le nom de votre projet
django.setup()

from camps.models import Camp  # Remplacez 'camps' par le nom de votre app

Camp.objects.all().delete()

def create_camps():
    branches = ['BB', 'BC', 'BM', 'BP']
    for branche in branches:
        if branche == 'BP':
            p = 12
        if branche == 'BM':
            p = 25
        if branche == 'BC':
            p = 17
        if branche == 'BB':
            p = 6
        for i in range(1, p):
            numero = f"{branche} {i}"
            camp = Camp.objects.create(numero=numero, branche=branche)
            print(f"Camp créé : {camp}")

def create_mail():
    for camp in Camp.objects.all():
        camp.mail= camp.numero.replace(' ','').lower() + '@eeif.org'
        camp.save()
        print(f"Mail créé pour {camp}")

create_camps()
create_mail()
