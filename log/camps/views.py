
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import user_passes_test  # Importez le nouveau formulaire
from .models import Camp
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.decorators import user_passes_test


def get_document_slugs(documents):
    return [doc['slug'] for doc in documents]

def logout(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Connecte automatiquement l'utilisateur après l'inscription
            return redirect('home')  # Redirige vers une page d'accueil ou autre
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def group_required(groups):
    if not isinstance(groups, (list, tuple)):
        groups = [groups]
    
    def in_groups(user):
        if user.is_authenticated:
            return user.groups.filter(name__in=groups).exists() or user.is_superuser
        return False
    
    return user_passes_test(in_groups)

def home(request):
    is_in_anbm = request.user.groups.filter(name="anbm").exists() if request.user.is_authenticated else False
    is_in_anbc = request.user.groups.filter(name="anbc").exists() if request.user.is_authenticated else False
    is_in_anbp = request.user.groups.filter(name="anbp").exists() if request.user.is_authenticated else False
    is_in_anbb = request.user.groups.filter(name="anbb").exists() if request.user.is_authenticated else False
    is_in_logistique = request.user.groups.filter(name="logistique").exists() if request.user.is_authenticated else False
    is_in_masai = request.user.groups.filter(name="masai").exists() if request.user.is_authenticated else False
    is_superuser = request.user.is_superuser if request.user.is_authenticated else False


    context = {
        'is_in_anbm': is_in_anbm,
        'is_in_anbc': is_in_anbc,
        'is_in_anbp': is_in_anbp,
        'is_in_anbb': is_in_anbb,
        'is_in_logistique': is_in_logistique,
        'is_in_masai': is_in_masai,
        'is_superuser': is_superuser,
    }
    return render(request, 'home.html', context)

def cdc(request):
    user = request.user
    camp = user.camp  # Récupération du camp associé à l'utilisateur
    
    if camp.branche == 'BC' or 'BM':
        documents = [
    {'name': 'Demande de prospection', 'slug': 'demande_prospe', 'deadline': camp.demande_prospe_deadline, 'file': camp.demande_prospe, 'state': camp.demande_prospe_etat, 'comment': camp.demande_prospe_commentaire},
    {'name': 'Compte-Rendu Prospection', 'slug': 'CR_prospe', 'deadline': camp.CR_prospe_deadline, 'file': camp.CR_prospe, 'state': camp.CR_prospe_etat, 'comment': camp.CR_prospe_commentaire},
    {'name': 'Contrat de location', 'slug': 'contrat_location', 'deadline': camp.contrat_location_deadline, 'file': camp.contrat_location, 'state': camp.contrat_location_etat, 'comment': camp.contrat_location_commentaire},
    {'name': 'Upload des prio', 'slug': 'PAF', 'deadline': camp.PAF_deadline, 'state': camp.PAF_etat},
    {'name': 'Maitrise', 'slug': 'grille_ddcs', 'deadline': camp.grille_ddcs_deadline, 'file': camp.grille_ddcs, 'state': camp.grille_ddcs_etat, 'comment': camp.grille_ddcs_commentaire},
    {'name': 'Grille de Camp', 'slug': 'grille_camp', 'deadline': camp.grille_camp_deadline, 'file': camp.grille_camp, 'state': camp.grille_camp_etat, 'comment': camp.grille_camp_commentaire},
    {'name': 'Projet pédagogique V1', 'slug': 'projetv1', 'deadline': camp.projetv1_deadline, 'file': camp.projetv1, 'file_retour': camp.projetv1_retour, 'state': camp.projetv1_etat, 'comment': camp.projetv1_commentaire},
    {'name': 'Infos JN', 'slug': 'JN', 'deadline': camp.JN_deadline, 'file': camp.JN, 'state': camp.JN_etat, 'comment': camp.JN_commentaire},
    {'name': 'Fiche SNCF / Cars', 'slug': 'fiche_sncf', 'deadline': camp.fiche_sncf_deadline, 'file': camp.fiche_sncf, 'state': camp.fiche_sncf_etat, 'comment': camp.fiche_sncf_commentaire},
    {'name': 'Grille Intendance', 'slug': 'grille_intendance', 'deadline': camp.grille_intendance_deadline, 'file': camp.grille_intendance, 'state': camp.grille_intendance_etat, 'comment': camp.grille_intendance_commentaire},
    {'name': 'Commandes Intendance', 'slug': 'intendance2', 'deadline': camp.intendance2_deadline, 'file': camp.intendance2, 'state': camp.intendance2_etat, 'comment': camp.intendance2_commentaire},
    {'name': 'Grille Assurance', 'slug': 'grille_assurance', 'deadline': camp.grille_assurance_deadline, 'file': camp.grille_assurance, 'state': camp.grille_assurance_etat, 'comment': camp.grille_assurance_commentaire},
    #{'name': 'Projet d activité', 'slug': 'fil_rouge', 'deadline': camp.fil_rouge_deadline, 'file': camp.fil_rouge, 'file_retour': camp.fil_rouge_retour, 'state': camp.fil_rouge_etat, 'comment': camp.fil_rouge_commentaire},
    #{'name': 'Projet vie juive', 'slug': 'fil_bleu', 'deadline': camp.fil_bleu_deadline, 'file': camp.fil_bleu, 'file_retour': camp.fil_bleu_retour, 'state': camp.fil_bleu_etat, 'comment': camp.fil_bleu_commentaire},
    #{'name': 'Projet vie de camp', 'slug': 'fil_vert', 'deadline': camp.fil_vert_deadline, 'file': camp.fil_vert, 'file_retour': camp.fil_vert_retour, 'state': camp.fil_vert_etat, 'comment': camp.fil_vert_commentaire},
    {'name': 'Budget prévisionnel', 'slug': 'Budget', 'deadline': camp.Budget_deadline, 'file': camp.Budget, 'state': camp.Budget_etat, 'comment': camp.Budget_commentaire},
    {'name': 'Voiture', 'slug': 'voiture', 'deadline': camp.voiture_deadline, 'file': camp.voiture, 'state': camp.voiture_etat, 'comment': camp.voiture_commentaire},
    {'name': 'Projet pédagogique VF', 'slug': 'projetvf', 'deadline': camp.projetvf_deadline, 'file': camp.projetvf, 'file_retour': camp.projetvf_retour, 'state': camp.projetvf_etat, 'comment': camp.projetvf_commentaire},
    {'name': 'Budget réel', 'slug': 'Budgetreal', 'deadline': camp.Budgetreal_deadline, 'file': camp.Budgetreal, 'state': camp.Budgetreal_etat, 'comment': camp.Budgetreal_commentaire},
    {'name': 'Documents obligatoires en ACM', 'slug': 'docACM', 'deadline': camp.docACM_deadline, 'file': camp.docACM, 'state': camp.docACM_etat, 'comment': camp.docACM_commentaire},
    {'name': 'Récepissé', 'slug': 'recepisse', 'deadline': camp.recepisse_deadline, 'file': camp.recepisse, 'state': camp.recepisse_etat, 'comment': camp.recepisse_commentaire},
    {'name': 'Procuration Banque', 'slug': 'procuration_banque', 'deadline': camp.procuration_banque_deadline, 'file': camp.procuration_banque, 'state': camp.procuration_banque_etat, 'comment': camp.procuration_banque_commentaire},
    ]


    if camp.branche== 'BP':
        # Nouveaux documents ajoutés
        documents=[{'name': 'Budget prévisionnel', 'slug': 'BP', 'deadline': '4 Février', 'file': camp.BP, 'state': camp.BP_etat, 'comment': camp.BP_commentaire},
            {'name': 'V1 Grille de camp', 'slug': 'V1GC', 'deadline': '04 Février', 'file': camp.V1GC, 'state': camp.V1GC_etat, 'comment': camp.V1GC_commentaire},
            {'name': 'PPT du point de validation', 'slug': 'PPTPV', 'deadline': '04 Février', 'file': camp.PPTPV, 'state': camp.PPTPV_etat, 'comment': camp.PPTPV_commentaire},
            {'name': 'Proposition de casting accompagnateurs', 'slug': 'casting', 'deadline': '21 Février', 'file': camp.casting, 'state': camp.casting_etat, 'comment': camp.casting_commentaire},
            {'name': 'Devis des Billet', 'slug': 'devisbillet', 'deadline': '9 Mars', 'file': camp.devisbillet, 'state': camp.devisbillet_etat, 'comment': camp.devisbillet_commentaire},
            {'name': 'PPP', 'slug': 'PPP', 'deadline': '20 Mars', 'file': camp.PPP, 'state': camp.PPP_etat, 'comment': camp.PPP_commentaire},
            {'name': 'Devis des logement', 'slug': 'devislogement', 'deadline': '20 Mars', 'file': camp.devislogement, 'state': camp.devislogement_etat, 'comment': camp.devislogement_commentaire},
            {'name': 'PPP corrigé', 'slug': 'PPPc', 'deadline': 'Avant les JN', 'file': camp.PPPc, 'state': camp.PPPc_etat, 'comment': camp.PPPc_commentaire},
            {'name': 'V2 Grille de Camp', 'slug': 'V2GC', 'deadline': '1er Mai', 'file': camp.V2GC, 'state': camp.V2GC_etat, 'comment': camp.V2GC_commentaire},
            {'name': 'Grille intendance', 'slug': 'GI', 'deadline': '1er Mai', 'file': camp.GI, 'state': camp.GI_etat, 'comment': camp.GI_commentaire},
            {'name': 'VF grille de camp', 'slug': 'VFGC', 'deadline': '1er Juin', 'file': camp.VFGC, 'state': camp.VFGC_etat, 'comment': camp.VFGC_commentaire}
            ]
    
    return render(request, 'cdc.html', {'camp': camp, 'documents': documents})

@group_required(['logistique','masai' ,'superuser'])
def logistique(request):
    return render(request, 'logistique.html')

@group_required(['anbb', 'logistique', 'superuser', 'masai'])
def anbb(request):
    camps_bb = Camp.objects.filter(branche="BB")
    return render(request, 'anbb.html', {'camps_bb': camps_bb})

@group_required(['logistique','masai' ,'superuser','anbc'])
def anbc(request):
    camps_bc = Camp.objects.filter(branche="BC")
    return render(request, 'anbc.html', {'camps_bc': camps_bc})

@group_required(['logistique','masai' ,'superuser','anbm'])
def anbm(request):
    camps_bm = Camp.objects.filter(branche="BM")  # Récupère tous les camps ayant pour branche "BM"
    return render(request, 'anbm.html', {'camps_bm': camps_bm})

@group_required(['logistique','masai' ,'superuser','anbp'])
def anbp(request):
    camps_bp = Camp.objects.filter(branche="BP")
    return render(request, 'anbp.html', {'camps_bp': camps_bp})

@group_required(['logistique','masai' ,'superuser','anbb'])
def statbb(request):
    documents = [
        {'name': 'Demande de prospection', 'slug': 'demande_prospe'},
        {'name': 'Compte-Rendu Prospection', 'slug': 'CR_prospe'},
        {'name': 'Contrat de location', 'slug': 'contrat_location'},
        {'name': 'Upload des prio', 'slug': 'PAF'},
        {'name': 'Maitrise', 'slug': 'grille_ddcs'},
        {'name': 'Grille de Camp', 'slug': 'grille_camp'},
        {'name': 'Projet pédagogique V1', 'slug': 'projetv1'},
        {'name': 'Grille Intendance', 'slug': 'grille_intendance'},
        {'name': 'Fiche SNCF / Cars', 'slug': 'fiche_sncf'},
        {'name': 'Commandes Intendance', 'slug': 'intendance2'},
        {'name': 'Grille Assurance', 'slug': 'grille_assurance'},
        {'name': 'Infos JN', 'slug': 'JN'},
        {'name': 'Projet d activité', 'slug': 'fil_rouge'},
        {'name': 'Projet vie juive', 'slug': 'fil_bleu'},
        {'name': 'Projet vie de camp', 'slug': 'fil_vert'},
        {'name': 'Budget prévisionnel', 'slug': 'Budget'},
        {'name': 'Voiture', 'slug': 'voiture'},
        {'name': 'Projet pédagogique VF', 'slug': 'projetvf'},
        {'name': 'Budget réel', 'slug': 'Budgetreal'},
        {'name': 'Documents obligatoires en ACM', 'slug': 'docACM'},
        {'name': 'Récepissé', 'slug': 'recepisse'},
        {'name': 'Chemins Explo', 'slug': 'chemins_explo'},
        {'name': 'Procuration Banque', 'slug': 'procuration_banque'}
    ]

    # Liste des slugs pour accès rapide
    docs = [doc['slug'] for doc in documents]

    # Récupération des camps filtrés
    camps_bb = Camp.objects.filter(branche="BB")

    # Définition des états possibles
    etats = ["Rendu", "Non rendu", "Validé", "Refusé", "Retour fait", "En cours"]

    # Initialisation des compteurs
    compteurs = {
        doc: {"data": [0] * len(etats), "camps": {etat: [] for etat in etats}}
        for doc in docs
    }

    # Remplissage des compteurs
    for camp in camps_bb:
        for doc in docs:
            doc_etat = getattr(camp, f"{doc}_etat", None)  # Récupération dynamique
            if doc_etat in etats:  # Vérification pour éviter une KeyError
                index = etats.index(doc_etat)
                compteurs[doc]["data"][index] += 1
                compteurs[doc]["camps"][doc_etat].append(camp.numero)

    # Création du dictionnaire lisible pour le template
    compteurs_readable = {
        doc["name"]: {
            "data": compteurs[doc["slug"]]["data"],
            "camps": compteurs[doc["slug"]]["camps"],
            "id": doc["slug"]
        }
        for doc in documents
    }

    return render(request, 'statbb.html', {'camps_bb': camps_bb, 'compteurs': compteurs_readable})


@group_required(['logistique','masai' ,'superuser','anbc'])
def statbc(request):
    documents = [
        {'name': 'Demande de prospection', 'slug': 'demande_prospe'},
        {'name': 'Compte-Rendu Prospection', 'slug': 'CR_prospe'},
        {'name': 'Contrat de location', 'slug': 'contrat_location'},
        {'name': 'Maitrise', 'slug': 'grille_ddcs'},
        {'name': 'Grille de Camp', 'slug': 'grille_camp'},
        {'name': 'Projet pédagogique V1', 'slug': 'projetv1'},
        {'name': 'Grille Intendance', 'slug': 'grille_intendance'},
        {'name': 'Fiche SNCF / Cars', 'slug': 'fiche_sncf'},
        {'name': 'Commandes Intendance', 'slug': 'intendance2'},
        {'name': 'Grille Assurance', 'slug': 'grille_assurance'},
        {'name': 'Infos JN', 'slug': 'JN'},
        {'name': 'Projet d activité', 'slug': 'fil_rouge'},
        {'name': 'Projet vie juive', 'slug': 'fil_bleu'},
        {'name': 'Projet vie de camp', 'slug': 'fil_vert'},
        {'name': 'Budget prévisionnel', 'slug': 'Budget'},
        {'name': 'Voiture', 'slug': 'voiture'},
        {'name': 'Projet pédagogique VF', 'slug': 'projetvf'},
        {'name': 'Budget réel', 'slug': 'Budgetreal'},
        {'name': 'Documents obligatoires en ACM', 'slug': 'docACM'},
        {'name': 'Récepissé', 'slug': 'recepisse'},
        {'name': 'Procuration Banque', 'slug': 'procuration_banque'}
    ]

    # Liste des slugs pour accès rapide
    docs = [doc['slug'] for doc in documents]

    # Récupération des camps filtrés
    camps_bb = Camp.objects.filter(branche="BC")

    # Définition des états possibles
    etats = ["Rendu", "Non rendu", "Validé", "Refusé", "Retour fait", "En cours"]

    # Initialisation des compteurs
    compteurs = {
        doc: {"data": [0] * len(etats), "camps": {etat: [] for etat in etats}}
        for doc in docs
    }

    # Remplissage des compteurs
    for camp in camps_bb:
        for doc in docs:
            doc_etat = getattr(camp, f"{doc}_etat", None)  # Récupération dynamique
            if doc_etat in etats:  # Vérification pour éviter une KeyError
                index = etats.index(doc_etat)
                compteurs[doc]["data"][index] += 1
                compteurs[doc]["camps"][doc_etat].append(camp.numero)

    # Création du dictionnaire lisible pour le template
    compteurs_readable = {
        doc["name"]: {
            "data": compteurs[doc["slug"]]["data"],
            "camps": compteurs[doc["slug"]]["camps"],
            "id": doc["slug"]
        }
        for doc in documents
    }

    return render(request, 'statbc.html', {'camps_bb': camps_bb, 'compteurs': compteurs_readable})

@group_required(['logistique','masai' ,'superuser','anbm'])
def statbm(request):
    documents = [
        {'name': 'Demande de prospection', 'slug': 'demande_prospe'},
        {'name': 'Compte-Rendu Prospection', 'slug': 'CR_prospe'},
        {'name': 'Contrat de location', 'slug': 'contrat_location'},
        {'name': 'Maitrise', 'slug': 'grille_ddcs'},
        {'name': 'Grille de Camp', 'slug': 'grille_camp'},
        {'name': 'Projet pédagogique V1', 'slug': 'projetv1'},
        {'name': 'Grille Intendance', 'slug': 'grille_intendance'},
        {'name': 'Fiche SNCF / Cars', 'slug': 'fiche_sncf'},
        {'name': 'Commandes Intendance', 'slug': 'intendance2'},
        {'name': 'Grille Assurance', 'slug': 'grille_assurance'},
        {'name': 'Infos JN', 'slug': 'JN'},
        {'name': 'Projet d activité', 'slug': 'fil_rouge'},
        {'name': 'Projet vie juive', 'slug': 'fil_bleu'},
        {'name': 'Projet vie de camp', 'slug': 'fil_vert'},
        {'name': 'Budget prévisionnel', 'slug': 'Budget'},
        {'name': 'Voiture', 'slug': 'voiture'},
        {'name': 'Projet pédagogique VF', 'slug': 'projetvf'},
        {'name': 'Budget réel', 'slug': 'Budgetreal'},
        {'name': 'Documents obligatoires en ACM', 'slug': 'docACM'},
        {'name': 'Récepissé', 'slug': 'recepisse'},
        {'name': 'Procuration Banque', 'slug': 'procuration_banque'}
    ]

    # Liste des slugs pour accès rapide
    docs = [doc['slug'] for doc in documents]

    # Récupération des camps filtrés
    camps_bb = Camp.objects.filter(branche="BM")

    # Définition des états possibles
    etats = ["Rendu", "Non rendu", "Validé", "Refusé", "Retour fait", "En cours"]

    # Initialisation des compteurs
    compteurs = {
        doc: {"data": [0] * len(etats), "camps": {etat: [] for etat in etats}}
        for doc in docs
    }

    # Remplissage des compteurs
    for camp in camps_bb:
        for doc in docs:
            doc_etat = getattr(camp, f"{doc}_etat", None)  # Récupération dynamique
            if doc_etat in etats:  # Vérification pour éviter une KeyError
                index = etats.index(doc_etat)
                compteurs[doc]["data"][index] += 1
                compteurs[doc]["camps"][doc_etat].append(camp.numero)

    # Création du dictionnaire lisible pour le template
    compteurs_readable = {
        doc["name"]: {
            "data": compteurs[doc["slug"]]["data"],
            "camps": compteurs[doc["slug"]]["camps"],
            "id": doc["slug"]
        }
        for doc in documents
    }

    return render(request, 'statbm.html', {'camps_bb': camps_bb, 'compteurs': compteurs_readable})

@group_required(['logistique','masai' ,'superuser','anbp'])
def statbp(request):
    docs = [
    'BP', 'V1GC', 'PPTPV', 'casting', 'devisbillet', 'PPP', 
    'devislogement', 'PPPc', 'V2GC', 'GI', 'VFGC'
]
    camps_bb = Camp.objects.filter(branche="BP")
    compteurs = {}

    for doc in docs:
        compteurs[doc] = {
            "data": [0, 0, 0, 0, 0],  # [Rendu, Non rendu, En cours, Validé]
            "camps": {  # Associer les numéros des camps à chaque état
                "Rendu": [],
                "Non rendu": [],
                "Validé": [],
                "Refusé": [],
                "Retour fait": [],
            }
        }

    for camp in camps_bb:
        for doc in docs:
            doc_etat = getattr(camp, f"{doc}_etat", None)  # Récupérer l'état dynamiquement
            if doc_etat == 'Rendu':
                compteurs[doc]["data"][0] += 1
                compteurs[doc]["camps"]["Rendu"].append(camp.numero)
            elif doc_etat == 'Non rendu':
                compteurs[doc]["data"][1] += 1
                compteurs[doc]["camps"]["Non rendu"].append(camp.numero)
            elif doc_etat == 'Validé':
                compteurs[doc]["data"][2] += 1
                compteurs[doc]["camps"]["Validé"].append(camp.numero)
            elif doc_etat == 'Refusé':
                compteurs[doc]["data"][3] += 1
                compteurs[doc]["camps"]["Refusé"].append(camp.numero)
            elif doc_etat == 'Retour fait':
                compteurs[doc]["data"][4] += 1
                compteurs[doc]["camps"]["Retour fait"].append(camp.numero)

    # Préparer des titres lisibles pour le template
    compteurs_readable = {
        doc.replace("_", " ").capitalize(): {"data": details["data"], "camps": details["camps"], "id": doc}
        for doc, details in compteurs.items()
    }

    return render(request, 'statbp.html', {'camps_bb': camps_bb, 'compteurs': compteurs_readable})

def camp_detail(request, numero):
    camp = get_object_or_404(Camp, numero=numero)

    if camp.branche == 'BC' or 'BM':
    # Liste de tous les documents
        documents = [
    {'name': 'Demande de prospection', 'slug': 'demande_prospe', 'deadline': camp.demande_prospe_deadline, 'file': camp.demande_prospe, 'state': camp.demande_prospe_etat, 'comment': camp.demande_prospe_commentaire},
    {'name': 'Compte-Rendu Prospection', 'slug': 'CR_prospe', 'deadline': camp.CR_prospe_deadline, 'file': camp.CR_prospe, 'state': camp.CR_prospe_etat, 'comment': camp.CR_prospe_commentaire},
    {'name': 'Contrat de location', 'slug': 'contrat_location', 'deadline': camp.contrat_location_deadline, 'file': camp.contrat_location, 'state': camp.contrat_location_etat, 'comment': camp.contrat_location_commentaire},
    {'name': 'Upload des prio', 'slug': 'PAF', 'deadline': camp.PAF_deadline, 'state': camp.PAF_etat},
    {'name': 'Maitrise', 'slug': 'grille_ddcs', 'deadline': camp.grille_ddcs_deadline, 'file': camp.grille_ddcs, 'state': camp.grille_ddcs_etat, 'comment': camp.grille_ddcs_commentaire},
    {'name': 'Grille de Camp', 'slug': 'grille_camp', 'deadline': camp.grille_camp_deadline, 'file': camp.grille_camp, 'state': camp.grille_camp_etat, 'comment': camp.grille_camp_commentaire},
    {'name': 'Projet pédagogique V1', 'slug': 'projetv1', 'deadline': camp.projetv1_deadline, 'file': camp.projetv1, 'file_retour': camp.projetv1_retour, 'state': camp.projetv1_etat, 'comment': camp.projetv1_commentaire},
    {'name': 'Infos JN', 'slug': 'JN', 'deadline': camp.JN_deadline, 'file': camp.JN, 'state': camp.JN_etat, 'comment': camp.JN_commentaire},
    {'name': 'Fiche SNCF / Cars', 'slug': 'fiche_sncf', 'deadline': camp.fiche_sncf_deadline, 'file': camp.fiche_sncf, 'state': camp.fiche_sncf_etat, 'comment': camp.fiche_sncf_commentaire},
    {'name': 'Grille Intendance', 'slug': 'grille_intendance', 'deadline': camp.grille_intendance_deadline, 'file': camp.grille_intendance, 'state': camp.grille_intendance_etat, 'comment': camp.grille_intendance_commentaire},
    {'name': 'Commandes Intendance', 'slug': 'intendance2', 'deadline': camp.intendance2_deadline, 'file': camp.intendance2, 'state': camp.intendance2_etat, 'comment': camp.intendance2_commentaire},
    {'name': 'Grille Assurance', 'slug': 'grille_assurance', 'deadline': camp.grille_assurance_deadline, 'file': camp.grille_assurance, 'state': camp.grille_assurance_etat, 'comment': camp.grille_assurance_commentaire},
    {'name': 'Projet d activité', 'slug': 'fil_rouge', 'deadline': camp.fil_rouge_deadline, 'file': camp.fil_rouge, 'file_retour': camp.fil_rouge_retour, 'state': camp.fil_rouge_etat, 'comment': camp.fil_rouge_commentaire},
    {'name': 'Projet vie juive', 'slug': 'fil_bleu', 'deadline': camp.fil_bleu_deadline, 'file': camp.fil_bleu, 'file_retour': camp.fil_bleu_retour, 'state': camp.fil_bleu_etat, 'comment': camp.fil_bleu_commentaire},
    {'name': 'Projet vie de camp', 'slug': 'fil_vert', 'deadline': camp.fil_vert_deadline, 'file': camp.fil_vert, 'file_retour': camp.fil_vert_retour, 'state': camp.fil_vert_etat, 'comment': camp.fil_vert_commentaire},
    {'name': 'Budget prévisionnel', 'slug': 'Budget', 'deadline': camp.Budget_deadline, 'file': camp.Budget, 'state': camp.Budget_etat, 'comment': camp.Budget_commentaire},
    {'name': 'Voiture', 'slug': 'voiture', 'deadline': camp.voiture_deadline, 'file': camp.voiture, 'state': camp.voiture_etat, 'comment': camp.voiture_commentaire},
    {'name': 'Projet pédagogique VF', 'slug': 'projetvf', 'deadline': camp.projetvf_deadline, 'file': camp.projetvf, 'file_retour': camp.projetvf_retour, 'state': camp.projetvf_etat, 'comment': camp.projetvf_commentaire},
    {'name': 'Budget réel', 'slug': 'Budgetreal', 'deadline': camp.Budgetreal_deadline, 'file': camp.Budgetreal, 'state': camp.Budgetreal_etat, 'comment': camp.Budgetreal_commentaire},
    {'name': 'Documents obligatoires en ACM', 'slug': 'docACM', 'deadline': camp.docACM_deadline, 'file': camp.docACM, 'state': camp.docACM_etat, 'comment': camp.docACM_commentaire},
    {'name': 'Récepissé', 'slug': 'recepisse', 'deadline': camp.recepisse_deadline, 'file': camp.recepisse, 'state': camp.recepisse_etat, 'comment': camp.recepisse_commentaire},
    {'name': 'Procuration Banque', 'slug': 'procuration_banque', 'deadline': camp.procuration_banque_deadline, 'file': camp.procuration_banque, 'state': camp.procuration_banque_etat, 'comment': camp.procuration_banque_commentaire},
    ]
        
    if camp.branche == 'BP':
        documents=[{'name': 'Budget prévisionnel', 'slug': 'BP', 'deadline': '4 Février', 'file': camp.BP, 'state': camp.BP_etat, 'comment': camp.BP_commentaire},
            {'name': 'V1 Grille de camp', 'slug': 'V1GC', 'deadline': '04 Février', 'file': camp.V1GC, 'state': camp.V1GC_etat, 'comment': camp.V1GC_commentaire},
            {'name': 'PPT du point de validation', 'slug': 'PPTPV', 'deadline': '04 Février', 'file': camp.PPTPV, 'state': camp.PPTPV_etat, 'comment': camp.PPTPV_commentaire},
            {'name': 'Proposition de casting accompagnateurs', 'slug': 'casting', 'deadline': '21 Février', 'file': camp.casting, 'state': camp.casting_etat, 'comment': camp.casting_commentaire},
            {'name': 'Devis des Billet', 'slug': 'devisbillet', 'deadline': '9 Mars', 'file': camp.devisbillet, 'state': camp.devisbillet_etat, 'comment': camp.devisbillet_commentaire},
            {'name': 'PPP', 'slug': 'PPP', 'deadline': '20 Mars', 'file': camp.PPP, 'state': camp.PPP_etat, 'comment': camp.PPP_commentaire},
            {'name': 'Devis des logement', 'slug': 'devislogement', 'deadline': '20 Mars', 'file': camp.devislogement, 'state': camp.devislogement_etat, 'comment': camp.devislogement_commentaire},
            {'name': 'PPP corrigé', 'slug': 'PPPc', 'deadline': 'Avant les JN', 'file': camp.PPPc, 'state': camp.PPPc_etat, 'comment': camp.PPPc_commentaire},
            {'name': 'V2 Grille de Camp', 'slug': 'V2GC', 'deadline': '1er Mai', 'file': camp.V2GC, 'state': camp.V2GC_etat, 'comment': camp.V2GC_commentaire},
            {'name': 'Grille intendance', 'slug': 'GI', 'deadline': '1er Mai', 'file': camp.GI, 'state': camp.GI_etat, 'comment': camp.GI_commentaire},
            {'name': 'VF grille de camp', 'slug': 'VFGC', 'deadline': '1er Juin', 'file': camp.VFGC, 'state': camp.VFGC_etat, 'comment': camp.VFGC_commentaire}
            ]
    return render(request, 'camp_detail.html', {'camp': camp, 'documents': documents})

@login_required
def upload_file(request, file_type, camp_id):
    MAX_FILE_SIZE_MB = 5  # Taille maximale en Mo
    MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024  # Convertir en octets
    
    if request.method == "POST" and request.FILES.get('file'):
        camp = get_object_or_404(Camp, numero=camp_id)
        uploaded_file = request.FILES['file']

        # Vérification de la taille du fichier
        if uploaded_file.size > MAX_FILE_SIZE_BYTES:
            return HttpResponse(
                f"Erreur : Le fichier est trop volumineux. Taille maximale autorisée : {MAX_FILE_SIZE_MB} Mo.",
                status=400
            )

        # Liste des documents avec leurs attributs
        documents = [
            {'name': 'Demande de prospection', 'slug': 'demande_prospe'},
            {'name': 'Compte-Rendu Prospection', 'slug': 'CR_prospe'},
            {'name': 'Contrat de location', 'slug': 'contrat_location'},
            {'name': 'Upload des prio', 'slug': 'PAF'},
            {'name': 'Maitrise', 'slug': 'grille_ddcs'},
            {'name': 'Grille de Camp', 'slug': 'grille_camp'},
            {'name': 'Projet pédagogique V1', 'slug': 'projetv1'},
            {'name': 'Grille Intendance', 'slug': 'grille_intendance'},
            {'name': 'Fiche SNCF / Cars', 'slug': 'fiche_sncf'},
            {'name': 'Commandes Intendance', 'slug': 'intendance2'},
            {'name': 'Grille Assurance', 'slug': 'grille_assurance'},
            {'name': 'Infos JN', 'slug': 'JN'},
            {'name': 'Projet d activité', 'slug': 'fil_rouge'},
            {'name': 'Projet vie juive', 'slug': 'fil_bleu'},
            {'name': 'Projet vie de camp', 'slug': 'fil_vert'},
            {'name': 'Budget prévisionnel', 'slug': 'Budget'},
            {'name': 'Voiture', 'slug': 'voiture'},
            {'name': 'Projet pédagogique VF', 'slug': 'projetvf'},
            {'name': 'Budget réel', 'slug': 'Budgetreal'},
            {'name': 'Documents obligatoires en ACM', 'slug': 'docACM'},
            {'name': 'Récepissé', 'slug': 'recepisse'},
            {'name': 'Chemins Explo', 'slug': 'chemins_explo'},
            {'name': 'Procuration Banque', 'slug': 'procuration_banque'}
        ]

        # Vérification du fichier envoyé
        doc_info = next((doc for doc in documents if doc['slug'] == file_type), None)

        if not doc_info:
            return HttpResponse("Type de fichier invalide.", status=400)

        # Mise à jour du champ correspondant dans l'objet Camp
        camp.delete_old_file(file_type)  # Suppression du fichier précédent
        setattr(camp, file_type, uploaded_file)  # Assignation du fichier
        setattr(camp, f"{file_type}_etat", 'Rendu')  # Mise à jour de l'état
        file_label = doc_info['name']

        camp.save()

        # Définition des destinataires en fonction de la branche
        destinataires = {
            'BB': ['elie.nebot@eeif.org', 'ben.tubiana@eeif.org', 'chloe.studnia@eeif.org', 
                   'elsa.seksik@eeif.org', 'annaelle.seksik@eeif.org', 'responsablesnational@eeif.org'],
            'BC': ['raphael.jaoui@eeif.org', 'ronel.atlan@eeif.org', 'ben.tubiana@eeif.org', 
                   'chloe.studnia@eeif.org', 'elsa.seksik@eeif.org', 'annaelle.seksik@eeif.org', 
                   'responsablesnational@eeif.org'],
            'BM': ['david.allali@eeif.org', 'noam.tordjman@eeif.org', 'ben.tubiana@eeif.org', 
                   'chloe.studnia@eeif.org', 'elsa.seksik@eeif.org', 'annaelle.seksik@eeif.org', 
                   'responsablesnational@eeif.org'],
            'BP': ['emma.elkaim-weil@eeif.org', 'ben.tubiana@eeif.org', 'chloe.studnia@eeif.org', 
                   'elsa.seksik@eeif.org', 'annaelle.seksik@eeif.org', 'responsablesnational@eeif.org']
        }

        receveur = destinataires.get(camp.branche, [])

        # Envoi d'un email de notification
        send_mail(
            subject='Un fichier a été téléversé',
            message=f'Un fichier de type "{file_label}" a été téléversé pour le camp {camp.numero}. '
                    f'Connectez-vous sur https://eeif.rezel.net/home/',
            from_email='eeif@rezel.net',  # Remplacez par votre adresse e-mail
            recipient_list=receveur,
        )

        return redirect('cdc')

    return HttpResponse("Invalid request", status=400)

def upload_file_qg(request, file_type, camp_id):
    MAX_FILE_SIZE_MB = 5  # Taille maximale en Mo
    MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024  # Convertir en octets
    
    if request.method == "POST" and request.FILES.get('file'):
        camp = get_object_or_404(Camp, numero=camp_id)
        uploaded_file = request.FILES['file']

        # Vérification de la taille du fichier
        if uploaded_file.size > MAX_FILE_SIZE_BYTES:
            return HttpResponse(
                f"Erreur : Le fichier est trop volumineux. Taille maximale autorisée : {MAX_FILE_SIZE_MB} Mo.",
                status=400
            )

        # Liste des documents avec leurs attributs
        documents = [
            {'name': 'Demande de prospection', 'slug': 'demande_prospe'},
            {'name': 'Compte-Rendu Prospection', 'slug': 'CR_prospe'},
            {'name': 'Contrat de location', 'slug': 'contrat_location'},
            {'name': 'Upload des prio', 'slug': 'PAF'},
            {'name': 'Maitrise', 'slug': 'grille_ddcs'},
            {'name': 'Grille de Camp', 'slug': 'grille_camp'},
            {'name': 'Projet pédagogique V1', 'slug': 'projetv1'},
            {'name': 'Grille Intendance', 'slug': 'grille_intendance'},
            {'name': 'Fiche SNCF / Cars', 'slug': 'fiche_sncf'},
            {'name': 'Commandes Intendance', 'slug': 'intendance2'},
            {'name': 'Grille Assurance', 'slug': 'grille_assurance'},
            {'name': 'Infos JN', 'slug': 'JN'},
            {'name': 'Projet d activité', 'slug': 'fil_rouge'},
            {'name': 'Projet vie juive', 'slug': 'fil_bleu'},
            {'name': 'Projet vie de camp', 'slug': 'fil_vert'},
            {'name': 'Budget prévisionnel', 'slug': 'Budget'},
            {'name': 'Voiture', 'slug': 'voiture'},
            {'name': 'Projet pédagogique VF', 'slug': 'projetvf'},
            {'name': 'Budget réel', 'slug': 'Budgetreal'},
            {'name': 'Documents obligatoires en ACM', 'slug': 'docACM'},
            {'name': 'Récepissé', 'slug': 'recepisse'},
            {'name': 'Chemins Explo', 'slug': 'chemins_explo'},
            {'name': 'Procuration Banque', 'slug': 'procuration_banque'}
        ]

        # Vérification du fichier envoyé
        doc_info = next((doc for doc in documents if doc['slug'] == file_type), None)

        if not doc_info:
            return HttpResponse("Type de fichier invalide.", status=400)

        # Mise à jour du champ correspondant dans l'objet Camp
        retour_field = f"{file_type}_retour"
        camp.delete_old_file(retour_field)  # Suppression du fichier précédent
        setattr(camp, retour_field, uploaded_file)  # Assignation du fichier
        setattr(camp, f"{file_type}_etat", 'Retour fait')  # Mise à jour de l'état
        file_label = doc_info['name']

        camp.save()

        # Envoi d'un email de notification
        send_mail(
            subject='Retour QG',
            message=f'Un fichier de type "{file_label}" a été téléversé pour le camp {camp.numero}. '
                    f'Connectez-vous sur https://eeif.rezel.net/home/',
            from_email='eeif@rezel.net',  # Remplacez par votre adresse e-mail
            recipient_list=[camp.mail],
        )

        return redirect('camp_detail', numero=camp_id)

    return HttpResponse("Invalid request", status=400)

@login_required
def delete_file(request, file_type, camp_id):
    camp = get_object_or_404(Camp, numero=camp_id)

    # Liste des documents disponibles avec leurs slugs
    documents = [
        {'name': 'Demande de prospection', 'slug': 'demande_prospe'},
        {'name': 'Compte-Rendu Prospection', 'slug': 'CR_prospe'},
        {'name': 'Contrat de location', 'slug': 'contrat_location'},
        {'name': 'Upload des prio', 'slug': 'PAF'},
        {'name': 'Maitrise', 'slug': 'grille_ddcs'},
        {'name': 'Grille de Camp', 'slug': 'grille_camp'},
        {'name': 'Projet pédagogique V1', 'slug': 'projetv1'},
        {'name': 'Grille Intendance', 'slug': 'grille_intendance'},
        {'name': 'Fiche SNCF / Cars', 'slug': 'fiche_sncf'},
        {'name': 'Commandes Intendance', 'slug': 'intendance2'},
        {'name': 'Grille Assurance', 'slug': 'grille_assurance'},
        {'name': 'Infos JN', 'slug': 'JN'},
        {'name': 'Projet d activité', 'slug': 'fil_rouge'},
        {'name': 'Projet vie juive', 'slug': 'fil_bleu'},
        {'name': 'Projet vie de camp', 'slug': 'fil_vert'},
        {'name': 'Budget prévisionnel', 'slug': 'Budget'},
        {'name': 'Voiture', 'slug': 'voiture'},
        {'name': 'Projet pédagogique VF', 'slug': 'projetvf'},
        {'name': 'Budget réel', 'slug': 'Budgetreal'},
        {'name': 'Documents obligatoires en ACM', 'slug': 'docACM'},
        {'name': 'Récepissé', 'slug': 'recepisse'},
        {'name': 'Chemins Explo', 'slug': 'chemins_explo'},
        {'name': 'Procuration Banque', 'slug': 'procuration_banque'}
    ]

    # Vérifier si le type de fichier est valide
    slugs = {doc['slug'] for doc in documents}
    if file_type not in slugs:
        return HttpResponse("Type de fichier invalide.", status=400)

    # Supprimer le fichier et mettre à jour l'état
    camp.delete_old_file(file_type)
    setattr(camp, file_type, None)  # Supprimer le fichier
    setattr(camp, f"{file_type}_etat", 'Non rendu')  # Mettre l'état à "Non rendu"

    camp.save()
    return redirect('cdc')

def delete_file_qg(request, file_type, camp_id):
    camp = get_object_or_404(Camp, numero=camp_id)

    # Liste des documents disponibles avec leurs slugs
    documents = [
        {'name': 'Demande de prospection', 'slug': 'demande_prospe'},
        {'name': 'Compte-Rendu Prospection', 'slug': 'CR_prospe'},
        {'name': 'Contrat de location', 'slug': 'contrat_location'},
        {'name': 'Upload des prio', 'slug': 'PAF'},
        {'name': 'Maitrise', 'slug': 'grille_ddcs'},
        {'name': 'Grille de Camp', 'slug': 'grille_camp'},
        {'name': 'Projet pédagogique V1', 'slug': 'projetv1'},
        {'name': 'Grille Intendance', 'slug': 'grille_intendance'},
        {'name': 'Fiche SNCF / Cars', 'slug': 'fiche_sncf'},
        {'name': 'Commandes Intendance', 'slug': 'intendance2'},
        {'name': 'Grille Assurance', 'slug': 'grille_assurance'},
        {'name': 'Infos JN', 'slug': 'JN'},
        {'name': 'Projet d activité', 'slug': 'fil_rouge'},
        {'name': 'Projet vie juive', 'slug': 'fil_bleu'},
        {'name': 'Projet vie de camp', 'slug': 'fil_vert'},
        {'name': 'Budget prévisionnel', 'slug': 'Budget'},
        {'name': 'Voiture', 'slug': 'voiture'},
        {'name': 'Projet pédagogique VF', 'slug': 'projetvf'},
        {'name': 'Budget réel', 'slug': 'Budgetreal'},
        {'name': 'Documents obligatoires en ACM', 'slug': 'docACM'},
        {'name': 'Récepissé', 'slug': 'recepisse'},
        {'name': 'Chemins Explo', 'slug': 'chemins_explo'},
        {'name': 'Procuration Banque', 'slug': 'procuration_banque'}
    ]

    # Vérifier si le type de fichier est valide
    slugs = {doc['slug'] for doc in documents}
    if file_type not in slugs:
        return HttpResponse("Type de fichier invalide.", status=400)

    # Supprimer le fichier et mettre à jour l'état
    retour_field = f"{file_type}_retour"
    camp.delete_old_file(retour_field)
    setattr(camp, retour_field, None)  # Supprimer le fichier
    setattr(camp, f"{file_type}_etat", 'Rendu')  # Mettre l'état à "Non rendu"

    camp.save()
    return redirect('camp_detail', numero=camp_id)


def update_file_state_cdc(request, file_type, camp_id):
    if request.method == "POST":
        new_state = request.POST.get("new_state")
        camp = get_object_or_404(Camp, numero=camp_id)

        # Liste des documents disponibles avec leurs slugs
        documents = [
            {'name': 'Demande de prospection', 'slug': 'demande_prospe'},
            {'name': 'Compte-Rendu Prospection', 'slug': 'CR_prospe'},
            {'name': 'Contrat de location', 'slug': 'contrat_location'},
            {'name': 'Upload des prio', 'slug': 'PAF'},
            {'name': 'Maitrise', 'slug': 'grille_ddcs'},
            {'name': 'Grille de Camp', 'slug': 'grille_camp'},
            {'name': 'Projet pédagogique V1', 'slug': 'projetv1'},
            {'name': 'Grille Intendance', 'slug': 'grille_intendance'},
            {'name': 'Fiche SNCF / Cars', 'slug': 'fiche_sncf'},
            {'name': 'Commandes Intendance', 'slug': 'intendance2'},
            {'name': 'Grille Assurance', 'slug': 'grille_assurance'},
            {'name': 'Infos JN', 'slug': 'JN'},
            {'name': 'Projet d activité', 'slug': 'fil_rouge'},
            {'name': 'Projet vie juive', 'slug': 'fil_bleu'},
            {'name': 'Projet vie de camp', 'slug': 'fil_vert'},
            {'name': 'Budget prévisionnel', 'slug': 'Budget'},
            {'name': 'Voiture', 'slug': 'voiture'},
            {'name': 'Projet pédagogique VF', 'slug': 'projetvf'},
            {'name': 'Budget réel', 'slug': 'Budgetreal'},
            {'name': 'Documents obligatoires en ACM', 'slug': 'docACM'},
            {'name': 'Récepissé', 'slug': 'recepisse'},
            {'name': 'Chemins Explo', 'slug': 'chemins_explo'},
            {'name': 'Procuration Banque', 'slug': 'procuration_banque'}
        ]

        # Vérifier si le type de fichier est valide
        slugs = {doc['slug'] for doc in documents}
        if file_type not in slugs:
            return HttpResponse("Type de fichier invalide.", status=400)

        # Mettre à jour l'état du fichier dynamiquement
        setattr(camp, f"{file_type}_etat", new_state)

        # Sauvegarder les modifications
        camp.save()

        # Envoi d'un email de notification

        return redirect('cdc')

    return redirect('cdc')

@login_required
def update_file_state(request, file_type, camp_id):
    if request.method == "POST":
        new_state = request.POST.get("new_state")
        camp = get_object_or_404(Camp, numero=camp_id)

        # Liste des documents disponibles avec leurs slugs
        documents = [
            {'name': 'Demande de prospection', 'slug': 'demande_prospe'},
            {'name': 'Compte-Rendu Prospection', 'slug': 'CR_prospe'},
            {'name': 'Contrat de location', 'slug': 'contrat_location'},
            {'name': 'Upload des prio', 'slug': 'PAF'},
            {'name': 'Maitrise', 'slug': 'grille_ddcs'},
            {'name': 'Grille de Camp', 'slug': 'grille_camp'},
            {'name': 'Projet pédagogique V1', 'slug': 'projetv1'},
            {'name': 'Grille Intendance', 'slug': 'grille_intendance'},
            {'name': 'Fiche SNCF / Cars', 'slug': 'fiche_sncf'},
            {'name': 'Commandes Intendance', 'slug': 'intendance2'},
            {'name': 'Grille Assurance', 'slug': 'grille_assurance'},
            {'name': 'Infos JN', 'slug': 'JN'},
            {'name': 'Projet d activité', 'slug': 'fil_rouge'},
            {'name': 'Projet vie juive', 'slug': 'fil_bleu'},
            {'name': 'Projet vie de camp', 'slug': 'fil_vert'},
            {'name': 'Budget prévisionnel', 'slug': 'Budget'},
            {'name': 'Voiture', 'slug': 'voiture'},
            {'name': 'Projet pédagogique VF', 'slug': 'projetvf'},
            {'name': 'Budget réel', 'slug': 'Budgetreal'},
            {'name': 'Documents obligatoires en ACM', 'slug': 'docACM'},
            {'name': 'Récepissé', 'slug': 'recepisse'},
            {'name': 'Chemins Explo', 'slug': 'chemins_explo'},
            {'name': 'Procuration Banque', 'slug': 'procuration_banque'}
        ]

        # Vérifier si le type de fichier est valide
        slugs = {doc['slug'] for doc in documents}
        if file_type not in slugs:
            return HttpResponse("Type de fichier invalide.", status=400)

        # Mettre à jour l'état du fichier dynamiquement
        setattr(camp, f"{file_type}_etat", new_state)

        # Sauvegarder les modifications
        camp.save()

        # Envoi d'un email de notification
        send_mail(
            subject='Retour du QG',
            message=f"L'état du fichier {file_type} a été modifié pour le camp {camp.numero}. Connectez-vous sur https://eeif.rezel.net/home",
            from_email='eeif@rezel.net',  # Remplacez par votre adresse e-mail
            recipient_list=[camp.mail],
        )

        return redirect('camp_detail', numero=camp_id)

    return redirect('camp_detail', numero=camp_id)

def modifier_commentaire(request, file_type, camp_id):
    if request.method == 'POST':
        camp = get_object_or_404(Camp, numero=camp_id)
        nouveau_commentaire = request.POST.get('commentaire')

        # Liste des documents disponibles avec leurs slugs
        documents = [
            {'name': 'Demande de prospection', 'slug': 'demande_prospe'},
            {'name': 'Compte-Rendu Prospection', 'slug': 'CR_prospe'},
            {'name': 'Contrat de location', 'slug': 'contrat_location'},
            {'name': 'Upload des prio', 'slug': 'PAF'},
            {'name': 'Maitrise', 'slug': 'grille_ddcs'},
            {'name': 'Grille de Camp', 'slug': 'grille_camp'},
            {'name': 'Projet pédagogique V1', 'slug': 'projetv1'},
            {'name': 'Grille Intendance', 'slug': 'grille_intendance'},
            {'name': 'Fiche SNCF / Cars', 'slug': 'fiche_sncf'},
            {'name': 'Commandes Intendance', 'slug': 'intendance2'},
            {'name': 'Grille Assurance', 'slug': 'grille_assurance'},
            {'name': 'Infos JN', 'slug': 'JN'},
            {'name': 'Projet d activité', 'slug': 'fil_rouge'},
            {'name': 'Projet vie juive', 'slug': 'fil_bleu'},
            {'name': 'Projet vie de camp', 'slug': 'fil_vert'},
            {'name': 'Budget prévisionnel', 'slug': 'Budget'},
            {'name': 'Voiture', 'slug': 'voiture'},
            {'name': 'Projet pédagogique VF', 'slug': 'projetvf'},
            {'name': 'Budget réel', 'slug': 'Budgetreal'},
            {'name': 'Documents obligatoires en ACM', 'slug': 'docACM'},
            {'name': 'Récepissé', 'slug': 'recepisse'},
            {'name': 'Chemins Explo', 'slug': 'chemins_explo'},
            {'name': 'Procuration Banque', 'slug': 'procuration_banque'}
        ]

        # Vérifier si le type de fichier est valide
        slugs = {doc['slug'] for doc in documents}
        if file_type not in slugs:
            return HttpResponse("Type de fichier invalide.", status=400)

        # Mettre à jour dynamiquement le commentaire
        setattr(camp, f"{file_type}_commentaire", nouveau_commentaire)

        # Sauvegarder les modifications
        camp.save()

        # Envoi d'un email de notification
        send_mail(
            subject='Retour du QG',
            message=f"Le commentaire concernant le fichier {file_type} a été modifié pour le camp {camp.numero}. Connectez-vous sur https://eeif.rezel.net/home",
            from_email='eeif@rezel.net',  # Remplacez par votre adresse e-mail
            recipient_list=[camp.mail],
        )

    # Rediriger vers la page principale après la mise à jour
    return redirect('camp_detail', numero=camp_id)

from django.http import JsonResponse

def get_int_from_post(request, key):
    value = request.POST.get(key, '0')
    return int(value) if value.isdigit() else 0

def simulation(request):
    if request.method == "POST":
# views.py
        pfeu = get_int_from_post(request, 'pfeu')
        zfeu = get_int_from_post(request, 'zfeu')
        efeu = get_int_from_post(request, 'efeu')
        pbois = get_int_from_post(request, 'pbois')
        zbois = get_int_from_post(request, 'zbois')
        ebois = get_int_from_post(request, 'ebois')
        pterre = get_int_from_post(request, 'pterre')
        zterre = get_int_from_post(request, 'zterre')
        eterre = get_int_from_post(request, 'eterre')
        peau = get_int_from_post(request, 'peau')
        zeau = get_int_from_post(request, 'zeau')
        eeau = get_int_from_post(request, 'eeau')
        pvaisselle = get_int_from_post(request, 'pvaisselle')
        zvaisselle = get_int_from_post(request, 'zvaisselle')
        evaisselle = get_int_from_post(request, 'evaisselle')
        pbouffe = get_int_from_post(request, 'pbouffe')
        zbouffe = get_int_from_post(request, 'zbouffe')
        ebouffe = get_int_from_post(request, 'ebouffe')
        pdecoupe = get_int_from_post(request, 'pdecoupe')
        zdecoupe = get_int_from_post(request, 'zdecoupe')
        edecoupe = get_int_from_post(request, 'edecoupe')
        pcuire = get_int_from_post(request, 'pcuire')
        zcuire = get_int_from_post(request, 'zcuire')
        ecuire = get_int_from_post(request, 'ecuire')
        ptable = get_int_from_post(request, 'ptable')
        ztable = get_int_from_post(request, 'ztable')
        etable = get_int_from_post(request, 'etable')
        peteindre = get_int_from_post(request, 'peteindre')
        zeteindre = get_int_from_post(request, 'zeteindre')
        eeteindre = get_int_from_post(request, 'eeteindre')

        def my_function(pbois=0, zbois=0, ebois=0, pterre=0, zterre=0, eterre=0, peau=0, zeau=0, eeau=0, pvaisselle=0, zvaisselle=0, evaisselle=0, pfeu=0, zfeu=0, efeu=0, pbouffe=0, zbouffe=0, ebouffe=0, pdecoupe=0, zdecoupe=0, edecoupe=0, pcuire=0, zcuire=0, ecuire=0, ptable=0, ztable=0, etable=0, peteindre=0, zeteindre=0, eeteindre=0):
            ecartpbois = abs(1-pbois)
            ecartpterre = abs(2-pterre)
            ecartpeau = abs(3-peau)
            ecartpvaisselle = abs(5-pvaisselle)
            ecartpfeu = abs(4-pfeu)
            ecartpbouffe = abs(6-pbouffe)
            ecartpdecoupe = abs(7-pdecoupe)
            ecartpcuire = abs(8-pcuire)
            ecartptable = abs(9-ptable)
            ecartpeteindre = abs(10-peteindre)
            nbzadeck= 6
            nbeclais = 15
            ecartzbois = abs(1-zbois)/nbzadeck
            ecartzterre = abs(0-zterre)/nbzadeck
            ecartzeau = abs(0-zeau)/nbzadeck
            ecartzvaisselle = abs(1-zvaisselle)/nbzadeck
            ecartzfeu = abs(1-zfeu)/nbzadeck
            ecartzbouffe = abs(0-zbouffe)/nbzadeck
            ecartzdecoupe = abs(1-zdecoupe)/nbzadeck
            ecartzcuire = abs(1-zcuire)/nbzadeck
            ecartztable = abs(0-ztable)/nbzadeck
            ecartzeteindre = abs(1-zeteindre)/nbzadeck
            ecartebois = abs(2-ebois)/nbeclais
            ecarteterre = abs(2-eterre)/nbeclais
            ecarteeau = abs(1-eeau)/nbeclais
            ecartevaisselle = abs(2-evaisselle)/nbeclais
            ecartefeu = abs(1-efeu)/nbeclais
            ecartebouffe = abs(2-ebouffe)/nbeclais
            ecartedecoupe = abs(2-edecoupe)/nbeclais
            ecartecuire = abs(1-ecuire)/nbeclais
            ecarteetable = abs(2-etable)/nbeclais
            ecarteeteindre = abs(0-eeteindre)/nbeclais
            somme_prio= ecartpbois + ecartpterre + ecartpeau + ecartpvaisselle + ecartpfeu + ecartpbouffe + ecartpdecoupe + ecartpcuire + ecartptable + ecartpeteindre
            somme_zadeck = ecartzbois + ecartzterre + ecartzeau + ecartzvaisselle + ecartzfeu + ecartzbouffe + ecartzdecoupe + ecartzcuire + ecartztable + ecartzeteindre
            somme_eclais = ecartebois + ecarteterre + ecarteeau + ecartevaisselle + ecartefeu + ecartebouffe + ecartedecoupe + ecartecuire + ecarteetable + ecarteeteindre
            try:
                return int(somme_prio*2+somme_zadeck*2+somme_eclais+60)
            except ValueError:
                return "Entrée invalide"

        result = my_function(pbois, zbois, ebois, pterre, zterre, eterre, peau, zeau, eeau, pvaisselle, zvaisselle, evaisselle, pfeu, zfeu, efeu, pbouffe, zbouffe, ebouffe, pdecoupe, zdecoupe, edecoupe, pcuire, zcuire, ecuire, ptable, ztable, etable, peteindre, zeteindre, eeteindre)
        return JsonResponse({'result': result})
    return render(request, 'simulation.html')