
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
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings


def send_notification_email(user, field_name, old_value, new_value, modified_by):
    """Envoie un email de notification à l'utilisateur quand ses informations sont modifiées"""
    # Vérifier si l'utilisateur qui a fait la modification appartient aux groupes autorisés
    authorized_groups = ['cga', 'log', 'anbc', 'anbm', 'anrgl', 'masai', 'gl']
    user_groups = [group.name for group in modified_by.groups.all()]
    
    if not any(group in user_groups for group in authorized_groups):
        return
    
    # Noms d'affichage des champs
    field_names = {
        'etatfrbc': 'État du fil rouge BC',
        'etatfrbm': 'État du fil rouge BM',
        'etatfbbm': 'État du fil bleu BM',
        'etatfbbc': 'État du fil bleu BC',
        'etatddcs': 'État de la grille DDCS',
        'etatgrille': 'État de la grille de l\'année',
        'etatprojetactivitebc': 'État de l\'ébauche projet d\'activité BC',
        'etatprojetviejuvebc': 'État de l\'ébauche projet vie juive BC',
        'commentairefrbm': 'Commentaire du fil rouge BM',
        'commentairefbbm': 'Commentaire du fil bleu BM',
        'commentairefrbc': 'Commentaire du fil rouge BC',
        'commentairefbbc': 'Commentaire du fil bleu BC',
        'commentaireddcs': 'Commentaire de la grille DDCS',
        'commentairegrille': 'Commentaire de la grille de l\'année',
        'commentaireprojetactivitebc': 'Commentaire de l\'ébauche projet d\'activité BC',
        'commentaireprojetviejuvebc': 'Commentaire de l\'ébauche projet vie juive BC',
    }
    
    field_display = field_names.get(field_name, field_name)
    
    # Déterminer le type de modification
    if field_name.startswith('etat'):
        change_type = 'état'
        message_content = f"L'{field_display} a été modifié de '{old_value}' vers '{new_value}'"
    else:
        change_type = 'commentaire'
        message_content = f"Le {field_display} a été modifié"
    
    # Créer le message
    subject = f'Modification de vos informations - {user.first_name} {user.last_name}'
    message = f"""
Bonjour {user.first_name} {user.last_name},

Vos informations ont été modifiées par {modified_by.first_name} {modified_by.last_name}.

{message_content}

Connectez-vous sur https://eeif.rezel.net/home/ pour voir les détails.

Cordialement,
L'équipe EEIF
"""
    
    # Envoyer l'email
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True,  # Ne pas faire planter l'application si l'email échoue
        )
        print(f"Email de notification envoyé à {user.email} pour la modification de {field_name} par {modified_by.username}")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email à {user.email}: {str(e)}")
        # Optionnel : log l'erreur dans un fichier ou base de données


def send_group_notification_email(field_name, old_value, new_value, modified_by, target_user):
    """Envoie un email de notification aux groupes spécifiques quand un utilisateur GL modifie certains états"""
    # Vérifier si l'utilisateur qui a fait la modification appartient au groupe GL
    if not modified_by.groups.filter(name='gl').exists():
        return
    
    # Définir les mappings des champs vers les emails des groupes
    field_to_group_email = {
        'etatfrbm': 'anbm@eeif.org',
        'etatfbbm': 'anbm@eeif.org',
        'etatfrbc': 'anbc@eeif.org',
        'etatfbbc': 'anbc@eeif.org',
        'etatprojetactivitebc': 'anbc@eeif.org',
        'etatprojetviejuvebc': 'anbc@eeif.org',
        'etatddcs': 'anrgl@eeif.org',
        'etatgrille': 'anrgl@eeif.org',
    }
    
    # Vérifier si le champ nécessite une notification de groupe
    if field_name not in field_to_group_email:
        return
    
    group_email = field_to_group_email[field_name]
    
    # Noms d'affichage des champs
    field_names = {
        'etatfrbc': 'État du fil rouge BC',
        'etatfrbm': 'État du fil rouge BM',
        'etatfbbm': 'État du fil bleu BM',
        'etatfbbc': 'État du fil bleu BC',
        'etatprojetactivitebc': 'État de l\'ébauche projet d\'activité BC',
        'etatprojetviejuvebc': 'État de l\'ébauche projet vie juive BC',
        'etatddcs': 'État de la grille DDCS',
        'etatgrille': 'État de la grille de l\'année',
    }
    
    field_display = field_names.get(field_name, field_name)
    
    # Déterminer le groupe destinataire
    group_names = {
        'anbm@eeif.org': 'ANBM',
        'anbc@eeif.org': 'ANBC',
        'anrgl@eeif.org': 'ANRGL',
    }
    group_name = group_names.get(group_email, 'Groupe')
    
    # Créer le message
    subject = f'Modification d\'état par un utilisateur GL - {target_user.first_name} {target_user.last_name}'
    message = f"""
Bonjour {group_name},

Un utilisateur du groupe GL a modifié un état.

Détails de la modification :
- Utilisateur modifié : {target_user.first_name} {target_user.last_name} ({target_user.username})
- Groupe local : {target_user.gl}
- Champ modifié : {field_display}
- Ancienne valeur : {old_value}
- Nouvelle valeur : {new_value}
- Modifié par : {modified_by.first_name} {modified_by.last_name} ({modified_by.username})

Connectez-vous sur https://eeif.rezel.net/home/ pour voir les détails.

Cordialement,
L'équipe EEIF
"""
    
    # Envoyer l'email
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[group_email],
            fail_silently=True,
        )
        print(f"Email de notification de groupe envoyé à {group_email} pour la modification de {field_name} par {modified_by.username}")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email de groupe à {group_email}: {str(e)}")


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
    
    if camp.branche == 'BC' or camp.branche == 'BM':
        documents = [
            {'name': 'Demande de prospection', 'slug': 'demande_prospe', 'deadline': camp.demande_prospe_deadline, 'file': camp.demande_prospe, 'state': camp.demande_prospe_etat, 'comment': camp.demande_prospe_commentaire},
            {'name': 'Compte-Rendu Prospection', 'slug': 'CR_prospe', 'deadline': camp.CR_prospe_deadline, 'file': camp.CR_prospe, 'state': camp.CR_prospe_etat, 'comment': camp.CR_prospe_commentaire},
            {'name': 'Contrat de location', 'slug': 'contrat_location', 'deadline': camp.contrat_location_deadline, 'file': camp.contrat_location, 'state': camp.contrat_location_etat, 'comment': camp.contrat_location_commentaire},
            # 2026
            {'name': 'Inscriptions prioritaires', 'slug': 'inscriptions_prio', 'deadline': camp.inscriptions_prio_deadline, 'state': camp.inscriptions_prio_etat, 'comment': camp.inscriptions_prio_commentaire},
            {'name': 'Budget prévisionnel', 'slug': 'budget_2026', 'deadline': camp.budget_2026_deadline, 'file': camp.budget_2026, 'state': camp.budget_2026_etat, 'comment': camp.budget_2026_commentaire},
            {'name': 'RDV Budget', 'slug': 'Budget_RDV', 'deadline': camp.Budget_RDV_deadline, 'state': camp.Budget_RDV_etat, 'comment': camp.Budget_RDV_commentaire},
            {'name': 'Date JN', 'slug': 'JN_2026', 'deadline': camp.JN_2026_deadline, 'date_jn': camp.JN_2026_date, 'state': camp.JN_2026_etat},
            {'name': 'PPP V1', 'slug': 'pppv1', 'deadline': camp.pppv1_deadline, 'file': camp.pppv1, 'state': camp.pppv1_etat, 'comment': camp.pppv1_commentaire},
            {'name': 'Projet d\'activité V2', 'slug': 'pav2', 'deadline': camp.pav2_deadline, 'file': camp.pav2, 'state': camp.pav2_etat, 'comment': camp.pav2_commentaire},
            {'name': 'Projet vie juive V2', 'slug': 'pvjv2', 'deadline': camp.pvjv2_deadline, 'file': camp.pvjv2, 'state': camp.pvjv2_etat, 'comment': camp.pvjv2_commentaire},
            {'name': 'Projet vie de camp V2', 'slug': 'pvcv2', 'deadline': camp.pvcv2_deadline, 'file': camp.pvcv2, 'state': camp.pvcv2_etat, 'comment': camp.pvcv2_commentaire},
            {'name': 'Projet d\'activité VF', 'slug': 'pavf', 'deadline': camp.pavf_deadline, 'file': camp.pavf, 'state': camp.pavf_etat, 'comment': camp.pavf_commentaire},
            {'name': 'Projet vie juive VF', 'slug': 'pvjvf', 'deadline': camp.pvjvf_deadline, 'file': camp.pvjvf, 'state': camp.pvjvf_etat, 'comment': camp.pvjvf_commentaire},
            {'name': 'Projet vie de camp VF', 'slug': 'pvcvf', 'deadline': camp.pvcvf_deadline, 'file': camp.pvcvf, 'state': camp.pvcvf_etat, 'comment': camp.pvcvf_commentaire},
            {'name': 'Grille de camp', 'slug': 'grille_camp_2026', 'deadline': camp.grille_camp_2026_deadline, 'file': camp.grille_camp_2026, 'state': camp.grille_camp_2026_etat, 'comment': camp.grille_camp_2026_commentaire},
            {'name': 'Maitrise', 'slug': 'maitrise_2026', 'deadline': camp.maitrise_2026_deadline, 'file': camp.maitrise_2026, 'state': camp.maitrise_2026_etat, 'comment': camp.maitrise_2026_commentaire},
            {'name': 'Fiche SNCF / Cars', 'slug': 'sncf_2026', 'deadline': camp.sncf_2026_deadline, 'file': camp.sncf_2026, 'state': camp.sncf_2026_etat, 'comment': camp.sncf_2026_commentaire},
            {'name': 'Grille intendance', 'slug': 'grille_intendance_2026', 'deadline': camp.grille_intendance_2026_deadline, 'file': camp.grille_intendance_2026, 'state': camp.grille_intendance_2026_etat, 'comment': camp.grille_intendance_2026_commentaire},
            {'name': 'Commandes intendance', 'slug': 'commandes_intendance_2026', 'deadline': camp.commandes_intendance_2026_deadline, 'file': camp.commandes_intendance_2026, 'state': camp.commandes_intendance_2026_etat, 'comment': camp.commandes_intendance_2026_commentaire},
            {'name': 'Voiture', 'slug': 'voiture_2026', 'deadline': camp.voiture_2026_deadline, 'file': camp.voiture_2026, 'state': camp.voiture_2026_etat, 'comment': camp.voiture_2026_commentaire},
            {'name': 'Assurance', 'slug': 'assurance_2026', 'deadline': camp.assurance_2026_deadline, 'file': camp.assurance_2026, 'state': camp.assurance_2026_etat, 'comment': camp.assurance_2026_commentaire},
            {'name': 'Billets', 'slug': 'billets_2026', 'deadline': camp.billets_2026_deadline, 'file': camp.billets_2026, 'state': camp.billets_2026_etat, 'comment': camp.billets_2026_commentaire},
        ]
    elif camp.branche == 'BP':
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
    else:
        # Cas par défaut pour les autres branches
        documents = []
    
    # Filtrer les documents pour s'assurer qu'ils ont tous un slug valide
    documents = [doc for doc in documents if doc.get('slug')]
    
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

@group_required(['logistique','masai' ,'superuser','anbb','anbc','anbm','anbp', 'gl'])
def gl(request):
    return render(request, 'gl.html')


@group_required(['logistique','masai' ,'superuser','anbb'])
def statbb(request):
    documents = [
        {'name': 'Demande de prospection', 'slug': 'demande_prospe'},
        {'name': 'Compte-Rendu Prospection', 'slug': 'CR_prospe'},
        {'name': 'Contrat de location', 'slug': 'contrat_location'},
        # 2026
        {'name': 'Inscriptions prioritaires', 'slug': 'inscriptions_prio'},
        {'name': 'Budget prévisionnel', 'slug': 'budget_2026'},
        {'name': 'RDV Budget', 'slug': 'Budget_RDV'},
        {'name': 'Date JN', 'slug': 'JN_2026'},
        {'name': 'PPP V1', 'slug': 'pppv1'},
        {'name': 'Projet d\'activité V2', 'slug': 'pav2'},
        {'name': 'Projet vie juive V2', 'slug': 'pvjv2'},
        {'name': 'Projet vie de camp V2', 'slug': 'pvcv2'},
        {'name': 'Projet d\'activité VF', 'slug': 'pavf'},
        {'name': 'Projet vie juive VF', 'slug': 'pvjvf'},
        {'name': 'Projet vie de camp VF', 'slug': 'pvcvf'},
        {'name': 'Grille de camp', 'slug': 'grille_camp_2026'},
        {'name': 'Maitrise', 'slug': 'maitrise_2026'},
        {'name': 'Fiche SNCF / Cars', 'slug': 'sncf_2026'},
        {'name': 'Grille intendance', 'slug': 'grille_intendance_2026'},
        {'name': 'Commandes intendance', 'slug': 'commandes_intendance_2026'},
        {'name': 'Voiture', 'slug': 'voiture_2026'},
        {'name': 'Assurance', 'slug': 'assurance_2026'},
        {'name': 'Billets', 'slug': 'billets_2026'},
        # {'name': 'Upload des prio', 'slug': 'PAF'},
        # {'name': 'Maitrise', 'slug': 'grille_ddcs'},
        # {'name': 'Grille de Camp', 'slug': 'grille_camp'},
        # {'name': 'Projet pédagogique V1', 'slug': 'projetv1'},
        # {'name': 'Grille Intendance', 'slug': 'grille_intendance'},
        # {'name': 'Fiche SNCF / Cars', 'slug': 'fiche_sncf'},
        # {'name': 'Commandes Intendance', 'slug': 'intendance2'},
        # {'name': 'Grille Assurance', 'slug': 'grille_assurance'},
        # {'name': 'Infos JN', 'slug': 'JN'},
        # {'name': 'Projet d activité', 'slug': 'fil_rouge'},
        # {'name': 'Projet vie juive', 'slug': 'fil_bleu'},
        # {'name': 'Projet vie de camp', 'slug': 'fil_vert'},
        # {'name': 'Budget prévisionnel', 'slug': 'Budget'},
        # {'name': 'Voiture', 'slug': 'voiture'},
        # {'name': 'Projet pédagogique VF', 'slug': 'projetvf'},
        # {'name': 'Budget réel', 'slug': 'Budgetreal'},
        # {'name': 'Documents obligatoires en ACM', 'slug': 'docACM'},
        # {'name': 'Récepissé', 'slug': 'recepisse'},
        # {'name': 'Chemins Explo', 'slug': 'chemins_explo'},
        # {'name': 'Procuration Banque', 'slug': 'procuration_banque'},
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
        # 2026
        {'name': 'Inscriptions prioritaires', 'slug': 'inscriptions_prio'},
        {'name': 'Budget prévisionnel', 'slug': 'budget_2026'},
        {'name': 'RDV Budget', 'slug': 'Budget_RDV'},
        {'name': 'Date JN', 'slug': 'JN_2026'},
        {'name': 'PPP V1', 'slug': 'pppv1'},
        {'name': 'Projet d\'activité V2', 'slug': 'pav2'},
        {'name': 'Projet vie juive V2', 'slug': 'pvjv2'},
        {'name': 'Projet vie de camp V2', 'slug': 'pvcv2'},
        {'name': 'Projet d\'activité VF', 'slug': 'pavf'},
        {'name': 'Projet vie juive VF', 'slug': 'pvjvf'},
        {'name': 'Projet vie de camp VF', 'slug': 'pvcvf'},
        {'name': 'Grille de camp', 'slug': 'grille_camp_2026'},
        {'name': 'Maitrise', 'slug': 'maitrise_2026'},
        {'name': 'Fiche SNCF / Cars', 'slug': 'sncf_2026'},
        {'name': 'Grille intendance', 'slug': 'grille_intendance_2026'},
        {'name': 'Commandes intendance', 'slug': 'commandes_intendance_2026'},
        {'name': 'Voiture', 'slug': 'voiture_2026'},
        {'name': 'Assurance', 'slug': 'assurance_2026'},
        {'name': 'Billets', 'slug': 'billets_2026'},
        # {'name': 'Maitrise', 'slug': 'grille_ddcs'},
        # {'name': 'Grille de Camp', 'slug': 'grille_camp'},
        # {'name': 'Projet pédagogique V1', 'slug': 'projetv1'},
        # {'name': 'Grille Intendance', 'slug': 'grille_intendance'},
        # {'name': 'Fiche SNCF / Cars', 'slug': 'fiche_sncf'},
        # {'name': 'Commandes Intendance', 'slug': 'intendance2'},
        # {'name': 'Grille Assurance', 'slug': 'grille_assurance'},
        # {'name': 'Infos JN', 'slug': 'JN'},
        # {'name': 'Projet d activité', 'slug': 'fil_rouge'},
        # {'name': 'Projet vie juive', 'slug': 'fil_bleu'},
        # {'name': 'Projet vie de camp', 'slug': 'fil_vert'},
        # {'name': 'Budget prévisionnel', 'slug': 'Budget'},
        # {'name': 'Voiture', 'slug': 'voiture'},
        # {'name': 'Projet pédagogique VF', 'slug': 'projetvf'},
        # {'name': 'Budget réel', 'slug': 'Budgetreal'},
        # {'name': 'Documents obligatoires en ACM', 'slug': 'docACM'},
        # {'name': 'Récepissé', 'slug': 'recepisse'},
        # {'name': 'Procuration Banque', 'slug': 'procuration_banque'},
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

@group_required(['logistique','masai' ,'superuser','anbc'])
def bcstats(request):
    """Vue pour les statistiques des étapes BC par groupe local"""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    # Récupération des utilisateurs du groupe GL
    users = User.objects.filter(groups__name='gl')
    
    # Définition des étapes BC
    etapes_bc = [
        {'name': 'Ébauche Projet d\'Activité BC', 'slug': 'etatprojetactivitebc'},
        {'name': 'Ébauche Projet Vie Juive BC', 'slug': 'etatprojetviejuvebc'},
        {'name': 'Projet d\'Activité BC', 'slug': 'etatfrbc'},
        {'name': 'Projet Vie Juive BC', 'slug': 'etatfbbc'},
    ]
    
    # Définition des états possibles
    etats = ["Non rendu", "Rendu", "Validé", "Refusé", "Retour fait", "En cours"]
    
    # Initialisation des compteurs
    compteurs = {
        etape['slug']: {"data": [0] * len(etats), "groupes": {etat: [] for etat in etats}}
        for etape in etapes_bc
    }
    
    # Remplissage des compteurs
    for user in users:
        for etape in etapes_bc:
            etat = getattr(user, etape['slug'], None)
            if etat in etats:
                index = etats.index(etat)
                compteurs[etape['slug']]['data'][index] += 1
                if user.gl:  # Ajouter le groupe local seulement s'il est défini
                    compteurs[etape['slug']]['groupes'][etat].append(user.gl)
    
    # Création du dictionnaire lisible pour le template
    compteurs_readable = {
        etape['name']: {
            "data": compteurs[etape['slug']]['data'],
            "groupes": compteurs[etape['slug']]['groupes'],
            "id": etape['slug']
        }
        for etape in etapes_bc
    }
    
    return render(request, 'bcstats.html', {'users': users, 'compteurs': compteurs_readable})

@group_required(['logistique','masai' ,'superuser','anbm'])
def bmstats(request):
    """Vue pour les statistiques des étapes BM par groupe local"""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    # Récupération des utilisateurs du groupe GL
    users = User.objects.filter(groups__name='gl')
    
    # Définition des étapes BM
    etapes_bm = [
        {'name': 'Projet d\'Activité BM', 'slug': 'etatfrbm'},
        {'name': 'Projet Vie Juive BM', 'slug': 'etatfbbm'},
    ]
    
    # Définition des états possibles
    etats = ["Non rendu", "Rendu", "Validé", "Refusé", "Retour fait", "En cours"]
    
    # Initialisation des compteurs
    compteurs = {
        etape['slug']: {"data": [0] * len(etats), "groupes": {etat: [] for etat in etats}}
        for etape in etapes_bm
    }
    
    # Remplissage des compteurs
    for user in users:
        for etape in etapes_bm:
            etat = getattr(user, etape['slug'], None)
            if etat in etats:
                index = etats.index(etat)
                compteurs[etape['slug']]['data'][index] += 1
                if user.gl:  # Ajouter le groupe local seulement s'il est défini
                    compteurs[etape['slug']]['groupes'][etat].append(user.gl)
    
    # Création du dictionnaire lisible pour le template
    compteurs_readable = {
        etape['name']: {
            "data": compteurs[etape['slug']]['data'],
            "groupes": compteurs[etape['slug']]['groupes'],
            "id": etape['slug']
        }
        for etape in etapes_bm
    }
    
    return render(request, 'bmstats.html', {'users': users, 'compteurs': compteurs_readable})

@group_required(['logistique','masai' ,'superuser','anrgl'])
def glstats(request):
    """Vue pour les statistiques des étapes GL par groupe local"""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    # Récupération des utilisateurs du groupe GL
    users = User.objects.filter(groups__name='gl')
    
    # Définition des étapes GL
    etapes_gl = [
        {'name': 'Grille DDCS', 'slug': 'etatddcs'},
        {'name': 'Grille de l\'Année', 'slug': 'etatgrille'},
    ]
    
    # Définition des états possibles
    etats = ["Non rendu", "Rendu", "Validé", "Refusé", "Retour fait", "En cours"]
    
    # Initialisation des compteurs
    compteurs = {
        etape['slug']: {"data": [0] * len(etats), "groupes": {etat: [] for etat in etats}}
        for etape in etapes_gl
    }
    
    # Remplissage des compteurs
    for user in users:
        for etape in etapes_gl:
            etat = getattr(user, etape['slug'], None)
            if etat in etats:
                index = etats.index(etat)
                compteurs[etape['slug']]['data'][index] += 1
                if user.gl:  # Ajouter le groupe local seulement s'il est défini
                    compteurs[etape['slug']]['groupes'][etat].append(user.gl)
    
    # Création du dictionnaire lisible pour le template
    compteurs_readable = {
        etape['name']: {
            "data": compteurs[etape['slug']]['data'],
            "groupes": compteurs[etape['slug']]['groupes'],
            "id": etape['slug']
        }
        for etape in etapes_gl
    }
    
    return render(request, 'glstats.html', {'users': users, 'compteurs': compteurs_readable})

@group_required(['logistique','masai' ,'superuser','anbm'])
def statbm(request):
    documents = [
        {'name': 'Demande de prospection', 'slug': 'demande_prospe'},
        {'name': 'Compte-Rendu Prospection', 'slug': 'CR_prospe'},
        {'name': 'Contrat de location', 'slug': 'contrat_location'},
        # 2026
        {'name': 'Inscriptions prioritaires', 'slug': 'inscriptions_prio'},
        {'name': 'Budget prévisionnel', 'slug': 'budget_2026'},
        {'name': 'RDV Budget', 'slug': 'Budget_RDV'},
        {'name': 'Date JN', 'slug': 'JN_2026'},
        {'name': 'PPP V1', 'slug': 'pppv1'},
        {'name': 'Projet d\'activité V2', 'slug': 'pav2'},
        {'name': 'Projet vie juive V2', 'slug': 'pvjv2'},
        {'name': 'Projet vie de camp V2', 'slug': 'pvcv2'},
        {'name': 'Projet d\'activité VF', 'slug': 'pavf'},
        {'name': 'Projet vie juive VF', 'slug': 'pvjvf'},
        {'name': 'Projet vie de camp VF', 'slug': 'pvcvf'},
        {'name': 'Grille de camp', 'slug': 'grille_camp_2026'},
        {'name': 'Maitrise', 'slug': 'maitrise_2026'},
        {'name': 'Fiche SNCF / Cars', 'slug': 'sncf_2026'},
        {'name': 'Grille intendance', 'slug': 'grille_intendance_2026'},
        {'name': 'Commandes intendance', 'slug': 'commandes_intendance_2026'},
        {'name': 'Voiture', 'slug': 'voiture_2026'},
        {'name': 'Assurance', 'slug': 'assurance_2026'},
        {'name': 'Billets', 'slug': 'billets_2026'},
        # {'name': 'Maitrise', 'slug': 'grille_ddcs'},
        # {'name': 'Grille de Camp', 'slug': 'grille_camp'},
        # {'name': 'Projet pédagogique V1', 'slug': 'projetv1'},
        # {'name': 'Grille Intendance', 'slug': 'grille_intendance'},
        # {'name': 'Fiche SNCF / Cars', 'slug': 'fiche_sncf'},
        # {'name': 'Commandes Intendance', 'slug': 'intendance2'},
        # {'name': 'Grille Assurance', 'slug': 'grille_assurance'},
        # {'name': 'Infos JN', 'slug': 'JN'},
        # {'name': 'Projet d activité', 'slug': 'fil_rouge'},
        # {'name': 'Projet vie juive', 'slug': 'fil_bleu'},
        # {'name': 'Projet vie de camp', 'slug': 'fil_vert'},
        # {'name': 'Budget prévisionnel', 'slug': 'Budget'},
        # {'name': 'Voiture', 'slug': 'voiture'},
        # {'name': 'Projet pédagogique VF', 'slug': 'projetvf'},
        # {'name': 'Budget réel', 'slug': 'Budgetreal'},
        # {'name': 'Documents obligatoires en ACM', 'slug': 'docACM'},
        # {'name': 'Récepissé', 'slug': 'recepisse'},
        # {'name': 'Procuration Banque', 'slug': 'procuration_banque'},
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

    if camp.branche == 'BC' or camp.branche == 'BM':
        # Liste de tous les documents
        documents = [
            {'name': 'Demande de prospection', 'slug': 'demande_prospe', 'deadline': camp.demande_prospe_deadline, 'file': camp.demande_prospe, 'state': camp.demande_prospe_etat, 'comment': camp.demande_prospe_commentaire},
            {'name': 'Compte-Rendu Prospection', 'slug': 'CR_prospe', 'deadline': camp.CR_prospe_deadline, 'file': camp.CR_prospe, 'state': camp.CR_prospe_etat, 'comment': camp.CR_prospe_commentaire},
            {'name': 'Contrat de location', 'slug': 'contrat_location', 'deadline': camp.contrat_location_deadline, 'file': camp.contrat_location, 'state': camp.contrat_location_etat, 'comment': camp.contrat_location_commentaire},
            # 2026
            {'name': 'Inscriptions prioritaires', 'slug': 'inscriptions_prio', 'deadline': camp.inscriptions_prio_deadline, 'state': camp.inscriptions_prio_etat, 'comment': camp.inscriptions_prio_commentaire},
            {'name': 'Budget prévisionnel', 'slug': 'budget_2026', 'deadline': camp.budget_2026_deadline, 'file': camp.budget_2026, 'state': camp.budget_2026_etat, 'comment': camp.budget_2026_commentaire},
            {'name': 'RDV Budget', 'slug': 'Budget_RDV', 'deadline': camp.Budget_RDV_deadline, 'state': camp.Budget_RDV_etat, 'comment': camp.Budget_RDV_commentaire},
            {'name': 'Date JN', 'slug': 'JN_2026', 'deadline': camp.JN_2026_deadline, 'date_jn': camp.JN_2026_date, 'state': camp.JN_2026_etat},
            {'name': 'PPP V1', 'slug': 'pppv1', 'deadline': camp.pppv1_deadline, 'file': camp.pppv1, 'state': camp.pppv1_etat, 'comment': camp.pppv1_commentaire},
            {'name': 'Projet d\'activité V2', 'slug': 'pav2', 'deadline': camp.pav2_deadline, 'file': camp.pav2, 'state': camp.pav2_etat, 'comment': camp.pav2_commentaire},
            {'name': 'Projet vie juive V2', 'slug': 'pvjv2', 'deadline': camp.pvjv2_deadline, 'file': camp.pvjv2, 'state': camp.pvjv2_etat, 'comment': camp.pvjv2_commentaire},
            {'name': 'Projet vie de camp V2', 'slug': 'pvcv2', 'deadline': camp.pvcv2_deadline, 'file': camp.pvcv2, 'state': camp.pvcv2_etat, 'comment': camp.pvcv2_commentaire},
            {'name': 'Projet d\'activité VF', 'slug': 'pavf', 'deadline': camp.pavf_deadline, 'file': camp.pavf, 'state': camp.pavf_etat, 'comment': camp.pavf_commentaire},
            {'name': 'Projet vie juive VF', 'slug': 'pvjvf', 'deadline': camp.pvjvf_deadline, 'file': camp.pvjvf, 'state': camp.pvjvf_etat, 'comment': camp.pvjvf_commentaire},
            {'name': 'Projet vie de camp VF', 'slug': 'pvcvf', 'deadline': camp.pvcvf_deadline, 'file': camp.pvcvf, 'state': camp.pvcvf_etat, 'comment': camp.pvcvf_commentaire},
            {'name': 'Grille de camp', 'slug': 'grille_camp_2026', 'deadline': camp.grille_camp_2026_deadline, 'file': camp.grille_camp_2026, 'state': camp.grille_camp_2026_etat, 'comment': camp.grille_camp_2026_commentaire},
            {'name': 'Maitrise', 'slug': 'maitrise_2026', 'deadline': camp.maitrise_2026_deadline, 'file': camp.maitrise_2026, 'state': camp.maitrise_2026_etat, 'comment': camp.maitrise_2026_commentaire},
            {'name': 'Fiche SNCF / Cars', 'slug': 'sncf_2026', 'deadline': camp.sncf_2026_deadline, 'file': camp.sncf_2026, 'state': camp.sncf_2026_etat, 'comment': camp.sncf_2026_commentaire},
            {'name': 'Grille intendance', 'slug': 'grille_intendance_2026', 'deadline': camp.grille_intendance_2026_deadline, 'file': camp.grille_intendance_2026, 'state': camp.grille_intendance_2026_etat, 'comment': camp.grille_intendance_2026_commentaire},
            {'name': 'Commandes intendance', 'slug': 'commandes_intendance_2026', 'deadline': camp.commandes_intendance_2026_deadline, 'file': camp.commandes_intendance_2026, 'state': camp.commandes_intendance_2026_etat, 'comment': camp.commandes_intendance_2026_commentaire},
            {'name': 'Voiture', 'slug': 'voiture_2026', 'deadline': camp.voiture_2026_deadline, 'file': camp.voiture_2026, 'state': camp.voiture_2026_etat, 'comment': camp.voiture_2026_commentaire},
            {'name': 'Assurance', 'slug': 'assurance_2026', 'deadline': camp.assurance_2026_deadline, 'file': camp.assurance_2026, 'state': camp.assurance_2026_etat, 'comment': camp.assurance_2026_commentaire},
            {'name': 'Billets', 'slug': 'billets_2026', 'deadline': camp.billets_2026_deadline, 'file': camp.billets_2026, 'state': camp.billets_2026_etat, 'comment': camp.billets_2026_commentaire},
        ]
    elif camp.branche == 'BP':
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
    else:
        # Cas par défaut pour les autres branches (BB, etc.)
        documents = []
    
    # Filtrer les documents pour s'assurer qu'ils ont tous un slug valide
    documents = [doc for doc in documents if doc.get('slug')]
    
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
            {'name': 'Procuration Banque', 'slug': 'procuration_banque'},
            # 2026
            {'name': 'Inscriptions prioritaires', 'slug': 'inscriptions_prio'},
            {'name': 'Budget 2026', 'slug': 'budget_2026'},
            {'name': 'RDV Budget', 'slug': 'Budget_RDV'},
            {'name': 'Date JN', 'slug': 'JN_2026'},
            {'name': 'PPP V1', 'slug': 'pppv1'},
            {'name': 'Projet d\'activité V2', 'slug': 'pav2'},
            {'name': 'Projet vie juive V2', 'slug': 'pvjv2'},
            {'name': 'Projet vie de camp V2', 'slug': 'pvcv2'},
            {'name': 'Projet d\'activité VF', 'slug': 'pavf'},
            {'name': 'Projet vie juive VF', 'slug': 'pvjvf'},
            {'name': 'Projet vie de camp VF', 'slug': 'pvcvf'},
            {'name': 'Grille de camp 2026', 'slug': 'grille_camp_2026'},
            {'name': 'Maitrise 2026', 'slug': 'maitrise_2026'},
            {'name': 'Fiche SNCF 2026', 'slug': 'sncf_2026'},
            {'name': 'Grille intendance 2026', 'slug': 'grille_intendance_2026'},
            {'name': 'Commandes intendance 2026', 'slug': 'commandes_intendance_2026'},
            {'name': 'Voiture 2026', 'slug': 'voiture_2026'},
            {'name': 'Assurance 2026', 'slug': 'assurance_2026'},
            {'name': 'Billets 2026', 'slug': 'billets_2026'},
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
            from_email=settings.DEFAULT_FROM_EMAIL,
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
            {'name': 'Procuration Banque', 'slug': 'procuration_banque'},
            # 2026
            {'name': 'Inscriptions prioritaires', 'slug': 'inscriptions_prio'},
            {'name': 'Budget 2026', 'slug': 'budget_2026'},
            {'name': 'RDV Budget', 'slug': 'Budget_RDV'},
            {'name': 'Date JN', 'slug': 'JN_2026'},
            {'name': 'PPP V1', 'slug': 'pppv1'},
            {'name': 'Projet d\'activité V2', 'slug': 'pav2'},
            {'name': 'Projet vie juive V2', 'slug': 'pvjv2'},
            {'name': 'Projet vie de camp V2', 'slug': 'pvcv2'},
            {'name': 'Projet d\'activité VF', 'slug': 'pavf'},
            {'name': 'Projet vie juive VF', 'slug': 'pvjvf'},
            {'name': 'Projet vie de camp VF', 'slug': 'pvcvf'},
            {'name': 'Grille de camp 2026', 'slug': 'grille_camp_2026'},
            {'name': 'Maitrise 2026', 'slug': 'maitrise_2026'},
            {'name': 'Fiche SNCF 2026', 'slug': 'sncf_2026'},
            {'name': 'Grille intendance 2026', 'slug': 'grille_intendance_2026'},
            {'name': 'Commandes intendance 2026', 'slug': 'commandes_intendance_2026'},
            {'name': 'Voiture 2026', 'slug': 'voiture_2026'},
            {'name': 'Assurance 2026', 'slug': 'assurance_2026'},
            {'name': 'Billets 2026', 'slug': 'billets_2026'},
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
            from_email=settings.DEFAULT_FROM_EMAIL,
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
        {'name': 'Procuration Banque', 'slug': 'procuration_banque'},
        # 2026
        {'name': 'Inscriptions prioritaires', 'slug': 'inscriptions_prio'},
        {'name': 'Budget 2026', 'slug': 'budget_2026'},
        {'name': 'RDV Budget', 'slug': 'Budget_RDV'},
        {'name': 'Date JN', 'slug': 'JN_2026'},
        {'name': 'PPP V1', 'slug': 'pppv1'},
        {'name': 'Projet d\'activité V2', 'slug': 'pav2'},
        {'name': 'Projet vie juive V2', 'slug': 'pvjv2'},
        {'name': 'Projet vie de camp V2', 'slug': 'pvcv2'},
        {'name': 'Projet d\'activité VF', 'slug': 'pavf'},
        {'name': 'Projet vie juive VF', 'slug': 'pvjvf'},
        {'name': 'Projet vie de camp VF', 'slug': 'pvcvf'},
        {'name': 'Grille de camp 2026', 'slug': 'grille_camp_2026'},
        {'name': 'Maitrise 2026', 'slug': 'maitrise_2026'},
        {'name': 'Fiche SNCF 2026', 'slug': 'sncf_2026'},
        {'name': 'Grille intendance 2026', 'slug': 'grille_intendance_2026'},
        {'name': 'Commandes intendance 2026', 'slug': 'commandes_intendance_2026'},
        {'name': 'Voiture 2026', 'slug': 'voiture_2026'},
        {'name': 'Assurance 2026', 'slug': 'assurance_2026'},
        {'name': 'Billets 2026', 'slug': 'billets_2026'},
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
        {'name': 'Procuration Banque', 'slug': 'procuration_banque'},
        # 2026
        {'name': 'Inscriptions prioritaires', 'slug': 'inscriptions_prio'},
        {'name': 'Budget 2026', 'slug': 'budget_2026'},
        {'name': 'RDV Budget', 'slug': 'Budget_RDV'},
        {'name': 'Date JN', 'slug': 'JN_2026'},
        {'name': 'PPP V1', 'slug': 'pppv1'},
        {'name': 'Projet d\'activité V2', 'slug': 'pav2'},
        {'name': 'Projet vie juive V2', 'slug': 'pvjv2'},
        {'name': 'Projet vie de camp V2', 'slug': 'pvcv2'},
        {'name': 'Projet d\'activité VF', 'slug': 'pavf'},
        {'name': 'Projet vie juive VF', 'slug': 'pvjvf'},
        {'name': 'Projet vie de camp VF', 'slug': 'pvcvf'},
        {'name': 'Grille de camp 2026', 'slug': 'grille_camp_2026'},
        {'name': 'Maitrise 2026', 'slug': 'maitrise_2026'},
        {'name': 'Fiche SNCF 2026', 'slug': 'sncf_2026'},
        {'name': 'Grille intendance 2026', 'slug': 'grille_intendance_2026'},
        {'name': 'Commandes intendance 2026', 'slug': 'commandes_intendance_2026'},
        {'name': 'Voiture 2026', 'slug': 'voiture_2026'},
        {'name': 'Assurance 2026', 'slug': 'assurance_2026'},
        {'name': 'Billets 2026', 'slug': 'billets_2026'},
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
            {'name': 'Procuration Banque', 'slug': 'procuration_banque'},
            # 2026
            {'name': 'Inscriptions prioritaires', 'slug': 'inscriptions_prio'},
            {'name': 'Budget 2026', 'slug': 'budget_2026'},
            {'name': 'RDV Budget', 'slug': 'Budget_RDV'},
            {'name': 'Date JN', 'slug': 'JN_2026'},
            {'name': 'PPP V1', 'slug': 'pppv1'},
            {'name': 'Projet d\'activité V2', 'slug': 'pav2'},
            {'name': 'Projet vie juive V2', 'slug': 'pvjv2'},
            {'name': 'Projet vie de camp V2', 'slug': 'pvcv2'},
            {'name': 'Projet d\'activité VF', 'slug': 'pavf'},
            {'name': 'Projet vie juive VF', 'slug': 'pvjvf'},
            {'name': 'Projet vie de camp VF', 'slug': 'pvcvf'},
            {'name': 'Grille de camp 2026', 'slug': 'grille_camp_2026'},
            {'name': 'Maitrise 2026', 'slug': 'maitrise_2026'},
            {'name': 'Fiche SNCF 2026', 'slug': 'sncf_2026'},
            {'name': 'Grille intendance 2026', 'slug': 'grille_intendance_2026'},
            {'name': 'Commandes intendance 2026', 'slug': 'commandes_intendance_2026'},
            {'name': 'Voiture 2026', 'slug': 'voiture_2026'},
            {'name': 'Assurance 2026', 'slug': 'assurance_2026'},
            {'name': 'Billets 2026', 'slug': 'billets_2026'},
        ]

        # Vérifier si le type de fichier est valide
        slugs = {doc['slug'] for doc in documents}
        if file_type not in slugs:
            return HttpResponse("Type de fichier invalide.", status=400)

        # Récupérer l'ancien état
        old_state = getattr(camp, f"{file_type}_etat", '')

        # Mettre à jour l'état du fichier dynamiquement
        setattr(camp, f"{file_type}_etat", new_state)

        # Sauvegarder les modifications
        camp.save()

        # Envoi d'un email de notification
        file_label = next((doc['name'] for doc in documents if doc['slug'] == file_type), file_type)
        from django.contrib.auth import get_user_model
        User = get_user_model()

        # Destinataires : tous les utilisateurs du groupe 'cga'
        recipients = list(User.objects.filter(groups__name='cga', email__isnull=False).exclude(email='').values_list('email', flat=True))

        # Ajouter les utilisateurs du groupe anbc ou anbm selon la branche
        if camp.branche == 'BC':
            recipients += list(User.objects.filter(groups__name='anbc', email__isnull=False).exclude(email='').values_list('email', flat=True))
        elif camp.branche == 'BM':
            recipients += list(User.objects.filter(groups__name='anbm', email__isnull=False).exclude(email='').values_list('email', flat=True))

        # Supprimer les doublons
        recipients = list(set(recipients))

        if recipients:
            try:
                send_mail(
                    subject=f'Modification d\'état - Camp {camp.numero}',
                    message=f'L\'état de l\'étape "{file_label}" du camp {camp.numero} a été modifié de "{old_state}" vers "{new_state}" par {request.user.first_name} {request.user.last_name}.\n\nConnectez-vous sur https://eeif.rezel.net/home/ pour voir les détails.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=recipients,
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Erreur envoi mail update_file_state_cdc: {e}")

        return redirect('cdc')

    return redirect('cdc')

@login_required
def update_date_jn(request, camp_id):
    if request.method == "POST":
        camp = get_object_or_404(Camp, numero=camp_id)
        date_jn = request.POST.get("date_jn")
        if date_jn:
            camp.JN_2026_date = date_jn
            camp.save()
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
            {'name': 'Procuration Banque', 'slug': 'procuration_banque'},
            # 2026
            {'name': 'Inscriptions prioritaires', 'slug': 'inscriptions_prio'},
            {'name': 'Budget 2026', 'slug': 'budget_2026'},
            {'name': 'RDV Budget', 'slug': 'Budget_RDV'},
            {'name': 'Date JN', 'slug': 'JN_2026'},
            {'name': 'PPP V1', 'slug': 'pppv1'},
            {'name': 'Projet d\'activité V2', 'slug': 'pav2'},
            {'name': 'Projet vie juive V2', 'slug': 'pvjv2'},
            {'name': 'Projet vie de camp V2', 'slug': 'pvcv2'},
            {'name': 'Projet d\'activité VF', 'slug': 'pavf'},
            {'name': 'Projet vie juive VF', 'slug': 'pvjvf'},
            {'name': 'Projet vie de camp VF', 'slug': 'pvcvf'},
            {'name': 'Grille de camp 2026', 'slug': 'grille_camp_2026'},
            {'name': 'Maitrise 2026', 'slug': 'maitrise_2026'},
            {'name': 'Fiche SNCF 2026', 'slug': 'sncf_2026'},
            {'name': 'Grille intendance 2026', 'slug': 'grille_intendance_2026'},
            {'name': 'Commandes intendance 2026', 'slug': 'commandes_intendance_2026'},
            {'name': 'Voiture 2026', 'slug': 'voiture_2026'},
            {'name': 'Assurance 2026', 'slug': 'assurance_2026'},
            {'name': 'Billets 2026', 'slug': 'billets_2026'},
        ]

        # Vérifier si le type de fichier est valide
        slugs = {doc['slug'] for doc in documents}
        if file_type not in slugs:
            return HttpResponse("Type de fichier invalide.", status=400)

        # Récupérer l'ancien état
        old_state = getattr(camp, f"{file_type}_etat", '')

        # Mettre à jour l'état du fichier dynamiquement
        setattr(camp, f"{file_type}_etat", new_state)

        # Sauvegarder les modifications
        camp.save()

        # Envoi d'un email de notification
        file_label = next((doc['name'] for doc in documents if doc['slug'] == file_type), file_type)
        recipients = []

        # Email du camp
        if camp.mail:
            recipients.append(camp.mail)

        # Emails des utilisateurs assignés au camp
        assigned_emails = list(camp.users.filter(email__isnull=False).exclude(email='').values_list('email', flat=True))
        recipients += assigned_emails

        # Supprimer les doublons
        recipients = list(set(recipients))

        if recipients:
            try:
                send_mail(
                    subject=f'Retour du QG - Camp {camp.numero}',
                    message=f'L\'état de l\'étape "{file_label}" du camp {camp.numero} a été modifié de "{old_state}" vers "{new_state}" par {request.user.first_name} {request.user.last_name}.\n\nConnectez-vous sur https://eeif.rezel.net/home/ pour voir les détails.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=recipients,
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Erreur envoi mail update_file_state: {e}")

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
            {'name': 'Procuration Banque', 'slug': 'procuration_banque'},
            # 2026
            {'name': 'Inscriptions prioritaires', 'slug': 'inscriptions_prio'},
            {'name': 'Budget 2026', 'slug': 'budget_2026'},
            {'name': 'RDV Budget', 'slug': 'Budget_RDV'},
            {'name': 'Date JN', 'slug': 'JN_2026'},
            {'name': 'PPP V1', 'slug': 'pppv1'},
            {'name': 'Projet d\'activité V2', 'slug': 'pav2'},
            {'name': 'Projet vie juive V2', 'slug': 'pvjv2'},
            {'name': 'Projet vie de camp V2', 'slug': 'pvcv2'},
            {'name': 'Projet d\'activité VF', 'slug': 'pavf'},
            {'name': 'Projet vie juive VF', 'slug': 'pvjvf'},
            {'name': 'Projet vie de camp VF', 'slug': 'pvcvf'},
            {'name': 'Grille de camp 2026', 'slug': 'grille_camp_2026'},
            {'name': 'Maitrise 2026', 'slug': 'maitrise_2026'},
            {'name': 'Fiche SNCF 2026', 'slug': 'sncf_2026'},
            {'name': 'Grille intendance 2026', 'slug': 'grille_intendance_2026'},
            {'name': 'Commandes intendance 2026', 'slug': 'commandes_intendance_2026'},
            {'name': 'Voiture 2026', 'slug': 'voiture_2026'},
            {'name': 'Assurance 2026', 'slug': 'assurance_2026'},
            {'name': 'Billets 2026', 'slug': 'billets_2026'},
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
        file_label = next((doc['name'] for doc in documents if doc['slug'] == file_type), file_type)
        recipients = []

        # Email du camp
        if camp.mail:
            recipients.append(camp.mail)

        # Emails des utilisateurs assignés au camp
        assigned_emails = list(camp.users.filter(email__isnull=False).exclude(email='').values_list('email', flat=True))
        recipients += assigned_emails

        # Supprimer les doublons
        recipients = list(set(recipients))

        if recipients:
            try:
                send_mail(
                    subject=f'Retour du QG - Camp {camp.numero}',
                    message=f'Le commentaire de l\'étape "{file_label}" du camp {camp.numero} a été modifié par {request.user.first_name} {request.user.last_name}.\n\nNouveau commentaire : {nouveau_commentaire}\n\nConnectez-vous sur https://eeif.rezel.net/home/ pour voir les détails.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=recipients,
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Erreur envoi mail modifier_commentaire: {e}")

    # Rediriger vers la page principale après la mise à jour
    return redirect('camp_detail', numero=camp_id)

from django.http import JsonResponse

def get_int_from_post(request, key):
    value = request.POST.get(key, '0')
    return int(value) if value.isdigit() else 0

def simulation(request):
    if request.method == "POST":
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

        # Appeler la fonction et passer le résultat au template
        result = my_function(pbois, zbois, ebois, pterre, zterre, eterre, peau, zeau, eeau, pvaisselle, zvaisselle, evaisselle, pfeu, zfeu, efeu, pbouffe, zbouffe, ebouffe, pdecoupe, zdecoupe, edecoupe, pcuire, zcuire, ecuire, ptable, ztable, etable, peteindre, zeteindre, eeteindre)
        
        # Vérifier si c'est une requête AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            from django.http import JsonResponse
            return JsonResponse({'result': result})
        
        return render(request, 'simulation.html', {'result': result})
    
    # Si ce n'est pas une requête POST, afficher le formulaire
    return render(request, 'simulation.html')


@login_required
def bc(request):
    """Vue pour afficher la page BC"""
    from django.contrib.auth.models import Group
    try:
        gl_group = Group.objects.get(name='gl')
        users = gl_group.user_set.all()
    except Group.DoesNotExist:
        users = []
    context = {
        'users': users,
    }
    return render(request, 'bc.html', context)


@login_required
def bm(request):
    """Vue pour afficher la page BM"""
    from django.contrib.auth.models import Group
    try:
        gl_group = Group.objects.get(name='gl')
        users = gl_group.user_set.all()
    except Group.DoesNotExist:
        users = []
    context = {
        'users': users,
    }
    return render(request, 'bm.html', context)


@login_required
def log(request):
    """Vue pour afficher la page logistique"""
    from django.contrib.auth.models import Group
    try:
        gl_group = Group.objects.get(name='gl')
        users = gl_group.user_set.all()
    except Group.DoesNotExist:
        users = []
    context = {
        'users': users,
    }
    return render(request, 'log.html', context)


@login_required
def cga(request):
    """Vue pour afficher la page CGA"""
    return render(request, 'cga.html')


@login_required
def anrgl(request):
    """Vue pour afficher la page ANRGL"""
    from django.contrib.auth.models import Group
    try:
        gl_group = Group.objects.get(name='gl')
        users = gl_group.user_set.all()
    except Group.DoesNotExist:
        users = []
    context = {
        'users': users,
    }
    return render(request, 'log.html', context)


@login_required
def gl2(request, username):
    """Vue pour afficher les informations d'un utilisateur spécifique"""
    from django.contrib.auth import get_user_model
    from .models import ETAT_CHOICES
    
    User = get_user_model()
    try:
        target_user = User.objects.get(username=username)
    except User.DoesNotExist:
        target_user = None
    
    context = {
        'target_user': target_user,
        'etat_choices': ETAT_CHOICES,
    }
    return render(request, 'gl2.html', context)


@login_required
def change_etat(request):
    """Vue pour changer l'état d'une étape"""
    if request.method == 'POST':
        etat_field = request.POST.get('etat_field')
        new_etat = request.POST.get('new_etat')
        username = request.POST.get('username')  # Récupérer l'username si présent
        
        if etat_field and new_etat:
            # Si on a un username, on change l'état de cet utilisateur
            if username:
                from django.contrib.auth import get_user_model
                User = get_user_model()
                try:
                    target_user = User.objects.get(username=username)
                    old_value = getattr(target_user, etat_field)
                    
                    if hasattr(target_user, etat_field):
                        setattr(target_user, etat_field, new_etat)
                        target_user.save()
                        
                        # Envoyer l'email de notification à l'utilisateur
                        send_notification_email(target_user, etat_field, old_value, new_etat, request.user)
                        
                        # Envoyer l'email de notification aux groupes spécifiques
                        send_group_notification_email(etat_field, old_value, new_etat, request.user, target_user)
                        
                        messages.success(request, f'État de {etat_field} mis à jour avec succès!')
                    else:
                        messages.error(request, 'Champ d\'état invalide.')
                except User.DoesNotExist:
                    messages.error(request, 'Utilisateur non trouvé.')
            else:
                # Sinon, on change l'état de l'utilisateur connecté
                old_value = getattr(request.user, etat_field)
                success = request.user.change_etat(etat_field, new_etat)
                if success:
                    # Envoyer l'email de notification à l'utilisateur
                    send_notification_email(request.user, etat_field, old_value, new_etat, request.user)
                    
                    # Envoyer l'email de notification aux groupes spécifiques
                    send_group_notification_email(etat_field, old_value, new_etat, request.user, request.user)
                    
                    messages.success(request, f'État de {etat_field} mis à jour avec succès!')
                else:
                    messages.error(request, 'Erreur lors de la mise à jour de l\'état.')
        else:
            messages.error(request, 'Données manquantes.')
    
    # Déterminer la page de redirection
    if username:
        return redirect('gl2', username=username)
    else:
        return redirect('gl')


@login_required
def update_comment(request):
    """Vue pour mettre à jour un commentaire"""
    if request.method == 'POST':
        comment_field = request.POST.get('comment_field')
        new_comment = request.POST.get('new_comment')
        username = request.POST.get('username')
        
        if comment_field and username:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            try:
                target_user = User.objects.get(username=username)
                old_value = getattr(target_user, comment_field)
                
                if hasattr(target_user, comment_field):
                    setattr(target_user, comment_field, new_comment)
                    target_user.save()
                    
                    # Envoyer l'email de notification
                    send_notification_email(target_user, comment_field, old_value, new_comment, request.user)
                    
                    messages.success(request, f'Commentaire de {comment_field} mis à jour avec succès!')
                else:
                    messages.error(request, 'Champ de commentaire invalide.')
            except User.DoesNotExist:
                messages.error(request, 'Utilisateur non trouvé.')
        else:
            messages.error(request, 'Données manquantes.')
    
    if username:
        return redirect('gl2', username=username)
    else:
        return redirect('gl')