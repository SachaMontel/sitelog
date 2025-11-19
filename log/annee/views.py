from django.shortcuts import render, redirect
from django.contrib import messages
import os
import random
import csv
import uuid
from django.conf import settings
from .forms import PhotoUploadForm, MessageForm
from .models import Message

# Create your views here.
def index(request):
    return render(request, 'index.html')

def gl(request):
    return render(request, 'gl.html')

def logout(request):
    return render(request, 'home.html')

def wall(request):
    """Page principale avec l'heure, photos aléatoires et messages"""
    try:
        # Récupérer les photos disponibles
        photos_dir = os.path.join(settings.MEDIA_ROOT, 'annee', 'photos')
        photos = []
        if os.path.exists(photos_dir):
            try:
                photos = [
                    f"annee/photos/{f}"
                    for f in os.listdir(photos_dir)
                    if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))
                ]
            except (OSError, PermissionError):
                photos = []
        
        # Récupérer les messages depuis le CSV
        messages_csv = []
        csv_path = os.path.join(settings.BASE_DIR, 'log', 'annee', 'static', 'messages.csv')
        if os.path.exists(csv_path):
            try:
                with open(csv_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    messages_csv = list(reader)
            except Exception:
                messages_csv = []
        
        # Récupérer aussi les messages de la base de données
        try:
            messages_db = Message.objects.all()
            messages_db_list = [{'texte': msg.texte, 'auteur': msg.auteur} for msg in messages_db]
        except Exception:
            messages_db_list = []
        
        # Sélectionner plusieurs messages et photos
        all_messages = messages_csv + messages_db_list
        max_messages = 4
        if all_messages and len(all_messages) > 0:
            selected_messages = random.sample(all_messages, min(len(all_messages), max_messages))
        else:
            selected_messages = []
        
        max_photos = 12
        if photos and len(photos) > 0:
            selected_photos = random.sample(photos, min(len(photos), max_photos))
        else:
            selected_photos = []
        
        context = {
            'selected_photos': selected_photos,
            'selected_messages': selected_messages,
            'photo_form': PhotoUploadForm(),
            'message_form': MessageForm(),
            'MEDIA_URL': settings.MEDIA_URL,
        }
        return render(request, 'annee/wall.html', context)
    except Exception as e:
        # En cas d'erreur, retourner une page avec des valeurs par défaut
        import traceback
        print(f"Erreur dans wall(): {e}")
        print(traceback.format_exc())
        context = {
            'selected_photos': [],
            'selected_messages': [],
            'photo_form': PhotoUploadForm(),
            'message_form': MessageForm(),
            'MEDIA_URL': settings.MEDIA_URL,
        }
        return render(request, 'annee/wall.html', context)

def upload_photo(request):
    """Gérer l'upload d'une photo"""
    MAX_FILE_SIZE_MB = 5  # Taille maximale en Mo
    MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024  # Convertir en octets
    
    try:
        if request.method == 'POST':
            if not request.FILES.get('photo'):
                messages.error(request, 'Aucun fichier n\'a été sélectionné.')
                return redirect('annee:wall')
            
            form = PhotoUploadForm(request.POST, request.FILES)
            if form.is_valid():
                photo = request.FILES['photo']
                
                # Vérification de la taille du fichier
                if photo.size > MAX_FILE_SIZE_BYTES:
                    messages.error(request, f'Erreur : Le fichier est trop volumineux. Taille maximale autorisée : {MAX_FILE_SIZE_MB} Mo.')
                    return redirect('annee:wall')
                
                # Créer le dossier s'il n'existe pas
                photos_dir = os.path.join(settings.MEDIA_ROOT, 'annee', 'photos')
                try:
                    os.makedirs(photos_dir, exist_ok=True)
                except OSError as e:
                    messages.error(request, f'Erreur : Impossible de créer le dossier de stockage. {str(e)}')
                    return redirect('annee:wall')
                
                # Générer un nom de fichier unique pour éviter les collisions
                file_extension = os.path.splitext(photo.name)[1]
                if not file_extension:
                    file_extension = '.jpg'  # Extension par défaut
                unique_filename = f"{uuid.uuid4()}{file_extension}"
                photo_path = os.path.join(photos_dir, unique_filename)
                
                # Sauvegarder la photo
                try:
                    with open(photo_path, 'wb+') as destination:
                        for chunk in photo.chunks():
                            destination.write(chunk)
                    messages.success(request, 'Photo ajoutée avec succès!')
                except IOError as e:
                    messages.error(request, f'Erreur lors de l\'enregistrement de la photo : {str(e)}')
                except Exception as e:
                    messages.error(request, f'Erreur inattendue : {str(e)}')
            else:
                # Afficher les erreurs du formulaire
                error_msg = 'Erreur lors de l\'upload de la photo. '
                if form.errors:
                    error_msg += ' '.join([str(err) for err_list in form.errors.values() for err in err_list])
                else:
                    error_msg += 'Vérifiez que le fichier est une image valide.'
                messages.error(request, error_msg)
        else:
            messages.error(request, 'Méthode non autorisée.')
    except Exception as e:
        import traceback
        print(f"Erreur dans upload_photo(): {e}")
        print(traceback.format_exc())
        messages.error(request, f'Une erreur est survenue : {str(e)}')
    
    return redirect('annee:wall')

def add_message(request):
    """Ajouter un message (dans la base de données)"""
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            Message.objects.create(
                texte=form.cleaned_data['texte'],
                auteur=form.cleaned_data['auteur']
            )
            messages.success(request, 'Message ajouté avec succès!')
        else:
            messages.error(request, 'Erreur lors de l\'ajout du message.')
    return redirect('annee:wall')
