import os
import shutil
import tempfile

import pandas as pd
import requests
from django.http import FileResponse
from django.shortcuts import render
from urllib.parse import urlparse, parse_qs
import mimetypes

from .forms import UploadFileForm

# Nom exact de la colonne contenant les liens
COLONNE_FICHES = "Fiche sanitaire (nouvelle) - A télécharger dans le menu  [ Accueil > Documents ]"

# Délai max (en secondes) pour télécharger une fiche
TIMEOUT_TELECHARGEMENT = 30


# Fonction pour télécharger les fichiers
def telecharger_fichier(url, dossier, index):
    try:
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        nom_fichier = query_params.get("id", [None])[0]  # Prend l'ID du document comme nom de fichier

        if not nom_fichier:
            nom_fichier = os.path.basename(parsed_url.path) or f"fiche_{index}"

        chemin_fichier = os.path.join(dossier, nom_fichier)

        response = requests.get(url, stream=True, timeout=TIMEOUT_TELECHARGEMENT)
        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "")
        extension = mimetypes.guess_extension(content_type) or ""

        if "pdf" in content_type:
            extension = ".pdf"
        elif "jpeg" in content_type or "jpg" in content_type:
            extension = ".jpg"
        elif "png" in content_type:
            extension = ".png"

        if extension and not chemin_fichier.lower().endswith(extension.lower()):
            chemin_fichier += extension

        # Évite d'écraser un fichier déjà téléchargé portant le même nom
        if os.path.exists(chemin_fichier):
            base, ext = os.path.splitext(chemin_fichier)
            chemin_fichier = f"{base}_{index}{ext}"

        with open(chemin_fichier, "wb") as fichier:
            for chunk in response.iter_content(chunk_size=8192):
                fichier.write(chunk)

        return chemin_fichier
    except Exception:
        return None


# Vue Django pour traiter l'upload
def upload_excel(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fichier_excel = request.FILES["fichier"]

            try:
                df = pd.read_excel(fichier_excel, engine="openpyxl")
            except ImportError:
                return render(request, "upload.html", {
                    "form": form,
                    "error": "Le module openpyxl n'est pas installé sur le serveur. "
                             "Exécuter : pip install openpyxl, puis redémarrer le service.",
                })
            except Exception:
                return render(request, "upload.html", {
                    "form": form,
                    "error": "Impossible de lire ce fichier. Vérifie qu'il s'agit bien d'un export Excel (.xlsx).",
                })

            if COLONNE_FICHES not in df.columns:
                return render(request, "upload.html", {
                    "form": form,
                    "error": f"Colonne « {COLONNE_FICHES} » introuvable dans le fichier. "
                             "Vérifie que c'est bien l'export contenant les fiches sanitaires.",
                })

            liens = df[COLONNE_FICHES].dropna().unique()

            # Dossier temporaire propre à cette requête (pas de collision entre
            # deux utilisateurs, pas de dépendance au répertoire courant du process)
            dossier_temp = tempfile.mkdtemp(prefix="fiches_sanitaires_")
            try:
                nb_total = 0
                nb_ok = 0
                for index, lien in enumerate(liens):
                    if isinstance(lien, str) and lien.startswith("http"):
                        nb_total += 1
                        if telecharger_fichier(lien, dossier_temp, index):
                            nb_ok += 1

                if nb_total == 0:
                    return render(request, "upload.html", {
                        "form": form,
                        "error": "Aucun lien de fiche sanitaire trouvé dans la colonne.",
                    })

                if nb_ok == 0:
                    return render(request, "upload.html", {
                        "form": form,
                        "error": f"Aucun des {nb_total} fichiers n'a pu être téléchargé. "
                                 "Les liens ont peut-être expiré ou nécessitent une connexion.",
                    })

                # Créer le ZIP dans un emplacement temporaire distinct du dossier source
                base_zip = tempfile.mktemp(prefix="fiches_sanitaires_")
                chemin_zip = shutil.make_archive(base_zip, "zip", dossier_temp)

                # On ouvre le ZIP puis on le supprime du disque : le descripteur
                # reste valide et FileResponse diffuse le contenu sans le charger en mémoire
                zip_file = open(chemin_zip, "rb")
                os.remove(chemin_zip)

                response = FileResponse(
                    zip_file,
                    content_type="application/zip",
                    as_attachment=True,
                    filename="fiches_sanitaires.zip",
                )
                return response
            finally:
                shutil.rmtree(dossier_temp, ignore_errors=True)

    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {"form": form})
