import os
import pandas as pd
import requests
import shutil
from django.shortcuts import render
from django.http import HttpResponse
from .forms import UploadFileForm
from urllib.parse import urlparse, parse_qs
import mimetypes

# Dossier temporaire pour stocker les fichiers téléchargés
DOSSIER_TEMP = "media/fiches_sanitaires"
ZIP_PATH = "media/fiches_sanitaires.zip"

# Nom exact de la colonne contenant les liens
COLONNE_FICHES = "Fiche sanitaire - à télécharger sur la page d'inscription"

# Assurer que le dossier existe avant toute opération
if not os.path.exists(DOSSIER_TEMP):
    os.makedirs(DOSSIER_TEMP, exist_ok=True)

# Fonction pour télécharger les fichiers
def telecharger_fichier(url, dossier):
    try:
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        nom_fichier = query_params.get("id", [None])[0]  # Prend l'ID du document comme nom de fichier

        if not nom_fichier:
            nom_fichier = os.path.basename(parsed_url.path)

        chemin_fichier = os.path.join(dossier, nom_fichier)

        response = requests.get(url, stream=True)
        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "")
        extension = mimetypes.guess_extension(content_type) or ""

        if "pdf" in content_type:
            extension = ".pdf"
        elif "jpeg" in content_type or "jpg" in content_type:
            extension = ".jpg"
        elif "png" in content_type:
            extension = ".png"

        chemin_fichier += extension

        with open(chemin_fichier, "wb") as fichier:
            for chunk in response.iter_content(chunk_size=1024):
                fichier.write(chunk)

        return chemin_fichier
    except Exception as e:
        return None

# Vue Django pour traiter l'upload
def upload_excel(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fichier_excel = request.FILES["fichier"]

            df = pd.read_excel(fichier_excel, engine="openpyxl")

            if COLONNE_FICHES not in df.columns:
                return HttpResponse(f"Erreur : Colonne '{COLONNE_FICHES}' introuvable.", status=400)

            liens = df[COLONNE_FICHES].dropna().unique()
            fichiers_telecharges = []

            for lien in liens:
                if isinstance(lien, str) and lien.startswith("http"):
                    fichier = telecharger_fichier(lien, DOSSIER_TEMP)
                    if fichier:
                        fichiers_telecharges.append(fichier)

            # Créer un fichier ZIP du dossier téléchargé
            chemin_zip = shutil.make_archive(DOSSIER_TEMP, "zip", DOSSIER_TEMP)

            with open(chemin_zip, "rb") as f:
                response = HttpResponse(f.read(), content_type="application/zip")
                response["Content-Disposition"] = f'attachment; filename="fiches_sanitaires.zip"'
            
            # Supprimer le contenu du dossier sans supprimer le dossier lui-même
            for fichier in os.listdir(DOSSIER_TEMP):
                fichier_path = os.path.join(DOSSIER_TEMP, fichier)
                if os.path.isfile(fichier_path) or os.path.islink(fichier_path):
                    os.unlink(fichier_path)
                elif os.path.isdir(fichier_path):
                    shutil.rmtree(fichier_path)
            
            # Supprimer le fichier ZIP après téléchargement
            if os.path.exists(ZIP_PATH):
                os.remove(ZIP_PATH)
            
            return response

    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {"form": form})
