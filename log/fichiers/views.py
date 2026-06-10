import json
import os
import re
import shutil
import tempfile
import threading
import uuid

import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from django.http import FileResponse, JsonResponse
from django.shortcuts import render
from urllib.parse import urlparse, parse_qs
import mimetypes

from .forms import UploadFileForm

# Nom exact de la colonne contenant les liens
COLONNE_FICHES = "Fiche sanitaire (nouvelle) - A télécharger dans le menu  [ Accueil > Documents ]"

# Délai max (en secondes) pour télécharger une fiche
TIMEOUT_TELECHARGEMENT = 30

# Nombre de téléchargements simultanés
TELECHARGEMENTS_PARALLELES = 8

JOB_ID_VALIDE = re.compile(r"^[a-f0-9]{32}$")


def _chemin_job(job_id, suffixe):
    return os.path.join(tempfile.gettempdir(), f"fiches_job_{job_id}{suffixe}")


def _ecrire_progression(job_id, data):
    # Écriture atomique pour qu'un poll ne lise jamais un JSON à moitié écrit
    chemin = _chemin_job(job_id, ".json")
    chemin_tmp = chemin + ".tmp"
    with open(chemin_tmp, "w") as f:
        json.dump(data, f)
    os.replace(chemin_tmp, chemin)


def _lire_progression(job_id):
    try:
        with open(_chemin_job(job_id, ".json")) as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


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


def _traiter_export(job_id, liens):
    """Télécharge toutes les fiches (en parallèle), construit le ZIP et
    tient à jour le fichier de progression lu par la vue de polling."""
    dossier_temp = tempfile.mkdtemp(prefix="fiches_sanitaires_")
    try:
        total = len(liens)
        fait = 0
        ok = 0
        with ThreadPoolExecutor(max_workers=TELECHARGEMENTS_PARALLELES) as pool:
            futures = [
                pool.submit(telecharger_fichier, lien, dossier_temp, index)
                for index, lien in enumerate(liens)
            ]
            for future in as_completed(futures):
                fait += 1
                if future.result():
                    ok += 1
                _ecrire_progression(job_id, {
                    "statut": "en_cours", "fait": fait, "total": total, "ok": ok,
                })

        if ok == 0:
            _ecrire_progression(job_id, {
                "statut": "erreur",
                "message": f"Aucun des {total} fichiers n'a pu être téléchargé. "
                           "Les liens ont peut-être expiré ou nécessitent une connexion.",
            })
            return

        shutil.make_archive(_chemin_job(job_id, ""), "zip", dossier_temp)
        _ecrire_progression(job_id, {
            "statut": "termine", "fait": total, "total": total, "ok": ok,
        })
    except Exception:
        _ecrire_progression(job_id, {
            "statut": "erreur",
            "message": "Erreur interne pendant la préparation du ZIP.",
        })
    finally:
        shutil.rmtree(dossier_temp, ignore_errors=True)


# Vue Django pour traiter l'upload
def upload_excel(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if not form.is_valid():
            return JsonResponse({"erreur": "Aucun fichier reçu."}, status=400)

        fichier_excel = request.FILES["fichier"]

        try:
            df = pd.read_excel(fichier_excel, engine="openpyxl")
        except ImportError:
            return JsonResponse({
                "erreur": "Le module openpyxl n'est pas installé sur le serveur. "
                          "Exécuter : pip install openpyxl, puis redémarrer le service.",
            }, status=500)
        except Exception:
            return JsonResponse({
                "erreur": "Impossible de lire ce fichier. Vérifie qu'il s'agit bien d'un export Excel (.xlsx).",
            }, status=400)

        if COLONNE_FICHES not in df.columns:
            return JsonResponse({
                "erreur": f"Colonne « {COLONNE_FICHES} » introuvable dans le fichier. "
                          "Vérifie que c'est bien l'export contenant les fiches sanitaires.",
            }, status=400)

        liens = [
            lien for lien in df[COLONNE_FICHES].dropna().unique()
            if isinstance(lien, str) and lien.startswith("http")
        ]
        if not liens:
            return JsonResponse({
                "erreur": "Aucun lien de fiche sanitaire trouvé dans la colonne.",
            }, status=400)

        job_id = uuid.uuid4().hex
        _ecrire_progression(job_id, {
            "statut": "en_cours", "fait": 0, "total": len(liens), "ok": 0,
        })
        threading.Thread(target=_traiter_export, args=(job_id, liens), daemon=True).start()

        return JsonResponse({"job_id": job_id, "total": len(liens)})

    return render(request, 'upload.html', {"form": UploadFileForm()})


def progression_export(request, job_id):
    if not JOB_ID_VALIDE.match(job_id):
        return JsonResponse({"erreur": "Identifiant invalide."}, status=400)
    progression = _lire_progression(job_id)
    if progression is None:
        return JsonResponse({"erreur": "Export introuvable ou expiré."}, status=404)
    return JsonResponse(progression)


def telecharger_export(request, job_id):
    if not JOB_ID_VALIDE.match(job_id):
        return JsonResponse({"erreur": "Identifiant invalide."}, status=400)
    chemin_zip = _chemin_job(job_id, ".zip")
    if not os.path.exists(chemin_zip):
        return JsonResponse({"erreur": "Export introuvable ou expiré."}, status=404)

    # On ouvre le ZIP puis on le supprime du disque : le descripteur reste
    # valide et FileResponse diffuse le contenu sans le charger en mémoire
    zip_file = open(chemin_zip, "rb")
    os.remove(chemin_zip)
    try:
        os.remove(_chemin_job(job_id, ".json"))
    except OSError:
        pass

    return FileResponse(
        zip_file,
        content_type="application/zip",
        as_attachment=True,
        filename="fiches_sanitaires.zip",
    )
