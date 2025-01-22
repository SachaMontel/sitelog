
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
    return render(request, 'cdc.html', {'camp': camp})

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

def camp_detail(request, numero):
    camp = get_object_or_404(Camp, numero=numero)
    return render(request, 'camp_detail.html', {'camp': camp})

@login_required
def upload_file(request, file_type, camp_id):
    MAX_FILE_SIZE_MB = 5  # Taille maximale en Mo
    MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024  # Convertir en octets
    
    if request.method == "POST" and request.FILES['file']:
        camp = get_object_or_404(Camp, numero=camp_id)
        uploaded_file = request.FILES['file']

        # Vérification de la taille du fichier
        if uploaded_file.size > MAX_FILE_SIZE_BYTES:
            return HttpResponse(
                f"Erreur : Le fichier est trop volumineux. Taille maximale autorisée : {MAX_FILE_SIZE_MB} Mo.",
                status=400
            )
            
        if file_type == 'fil_rouge':
            camp.delete_old_file('fil_rouge')
            camp.fil_rouge = uploaded_file
            file_label = "Fil rouge"
            camp.fil_rouge_etat = 'Rendu'
        elif file_type == 'fil_bleu':
            camp.delete_old_file('fil_bleu')
            camp.fil_bleu = uploaded_file   
            file_label= "Fil bleu"
            camp.fil_bleu_etat = 'Rendu'
        elif file_type == 'Budget':
            camp.delete_old_file('Budget')
            camp.Budget = uploaded_file
            file_label = "Budget"
            camp.Budget_etat = 'Rendu'
        elif file_type == 'contrat_location':
            camp.delete_old_file('contrat_location')
            camp.contrat_location = uploaded_file
            file_label = "Contrat de location"
            camp.contrat_location_etat = 'Rendu'
        elif file_type == 'CR_prospe':
            camp.delete_old_file('CR_prospe')
            camp.CR_prospe = uploaded_file
            file_label = "Compte-rendu de prospection"
            camp.CR_prospe_etat = 'Rendu'
        elif file_type == 'fiche_sncf':
            camp.delete_old_file('fiche_sncf')
            camp.fiche_sncf = uploaded_file
            file_label = "Fiche SNCF"
            camp.fiche_sncf_etat = 'Rendu'
        elif file_type == 'grille_assurance':
            camp.delete_old_file('grille_assurance')
            camp.grille_assurance = uploaded_file
            file_label = "Grille d'assurance"
            camp.grille_assurance_etat = 'Rendu'
        elif file_type == 'grille_ddcs':
            camp.delete_old_file('grille_ddcs')
            camp.grille_ddcs = uploaded_file
            file_label = "Grille DDCS"
            camp.grille_ddcs_etat = 'Rendu'
        elif file_type == 'grille_intendance':
            camp.delete_old_file('grille_intendance')
            camp.grille_intendance = uploaded_file
            file_label = "Grille intendance"
            camp.grille_intendance_etat = 'Rendu'
        elif file_type == 'procuration_banque':
            camp.delete_old_file('procuration_banque')
            camp.procuration_banque = uploaded_file
            file_label = "Procuration bancaire"
            camp.procuration_banque_etat = 'Rendu'
        elif file_type == 'recepisse':
            camp.delete_old_file('recepisse')
            camp.recepisse = uploaded_file
            file_label = "Récépissé"
            camp.recepisse_etat = 'Rendu'
        elif file_type == 'chemins_explo':
            camp.delete_old_file('chemins_explo')
            camp.chemins_explo = uploaded_file
            file_label = "Chemins d'explo"
            camp.chemins_explo_etat = 'Rendu'
        elif file_type == 'fil_vert':
            camp.delete_old_file('fil_vert')
            camp.fil_vert = uploaded_file
            file_label = "Fil vert"
            camp.fil_vert_etat = 'Rendu'
        elif file_type == 'grille_camp':
            camp.delete_old_file('grille_camp')
            camp.grille_camp = uploaded_file
            file_label = "Grille camp"
            camp.grille_camp_etat = 'Rendu'
        else:
            return HttpResponse("Type de fichier invalide.", status=400)
        camp.save()
        if camp.branche == 'BB':
            receveur = ['elie.nebot@eeif.org', 'ben.tubiana@eeif.org', 'chloe.studnia@eeif.org', 'elsa.seksik@eeif.org', 'annaelle.seksik@eeif.org', 'responsablesnational@eeif.org']
        elif camp.branche == 'BC':
            receveur = ['raphael.jaoui@eeif.org', 'ronel.atlan@eeif.org', 'ben.tubiana@eeif.org', 'chloe.studnia@eeif.org', 'elsa.seksik@eeif.org', 'annaelle.seksik@eeif.org', 'responsablesnational@eeif.org']
        elif camp.branche == 'BM':
            #receveur = ['sacha.montel@eeif.org']
            receveur = ['david.allali@eeif.org', 'noam.tordjman@eeif.org', 'ben.tubiana@eeif.org', 'chloe.studnia@eeif.org', 'elsa.seksik@eeif.org', 'annaelle.seksik@eeif.org', 'responsablesnational@eeif.org']
        elif camp.branche == 'BP':
            receveur = ['emma.elkaim-weil@eeif.org', 'ben.tubiana@eeif.org', 'chloe.studnia@eeif.org', 'elsa.seksik@eeif.org', 'annaelle.seksik@eeif.org', 'responsablesnational@eeif.org']
        send_mail(
            subject='Un fichier a été téléversé',
            message=f'Un fichier de type "{file_label}" a été téléversé pour le camp {camp.numero}. Connectez-vous sur https://eeif.rezel.net/home/',
            from_email='eeif@rezel.net',  # Remplacez par votre adresse e-mail
            recipient_list=receveur,
        )
        return redirect('cdc')
    return HttpResponse("Invalid request", status=400)

@login_required
def delete_file(request, file_type, camp_id):
    camp = get_object_or_404(Camp, numero=camp_id)

    # Supprime le fichier spécifié
    if file_type == 'fil_rouge' and camp.fil_rouge:
        camp.delete_old_file('fil_rouge')
        camp.fil_rouge = None
        camp.fil_rouge_etat = 'Non rendu'
    elif file_type == 'fil_bleu' and camp.fil_bleu:
        camp.delete_old_file('fil_bleu')
        camp.fil_bleu = None
        camp.fil_bleu_etat = 'Non rendu'
    elif file_type == 'Budget' and camp.Budget:
        camp.delete_old_file('Budget')
        camp.Budget = None
        camp.Budget_etat = 'Non rendu'
    elif file_type == 'contrat_location' and camp.contrat_location:
        camp.delete_old_file('contrat_location')
        camp.contrat_location = None
        camp.contrat_location_etat = 'Non rendu'
    elif file_type == 'CR_prospe' and camp.CR_prospe:
        camp.delete_old_file('CR_prospe')
        camp.CR_prospe = None
        camp.CR_prospe_etat = 'Non rendu'
    elif file_type == 'fiche_sncf' and camp.fiche_sncf:
        camp.delete_old_file('fiche_sncf')
        camp.fiche_sncf = None
        camp.fiche_sncf_etat = 'Non rendu'
    elif file_type == 'grille_assurance':
        camp.delete_old_file('grille_assurance')
        camp.grille_assurance = None
        camp.grille_assurance_etat = 'Non rendu'
    elif file_type == 'grille_ddcs':
        camp.delete_old_file('grille_ddcs')
        camp.grille_ddcs = None
        camp.grille_ddcs_etat = 'Non rendu'
    elif file_type == 'grille_intendance':
        camp.delete_old_file('grille_intendance')
        camp.grille_intendance = None
        camp.grille_intendance_etat = 'Non rendu'
    elif file_type == 'procuration_banque':
        camp.delete_old_file('procuration_banque')
        camp.procuration_banque = None
        camp.procuration_banque_etat = 'Non rendu'
    elif file_type == 'recepisse':
        camp.delete_old_file('recepisse')
        camp.recepisse = None
        camp.recepisse_etat = 'Non rendu'
    elif file_type == 'chemins_explo':
        camp.delete_old_file('chemins_explo')
        camp.chemins_explo = None
        camp.chemins_explo_etat = 'Non rendu'
    elif file_type == 'fil_vert':
        camp.delete_old_file('fil_vert')
        camp.fil_vert = None
        camp.fil_vert_etat = 'Non rendu'
    elif file_type == 'grille_camp':
        camp.delete_old_file('grille_camp')
        camp.grille_camp = None
        camp.grille_camp_etat = 'Non rendu'
    else:
        return HttpResponse("Type de fichier invalide.", status=400)
    camp.save()
    return redirect('cdc')


@login_required
def update_file_state(request, file_type, camp_id):
    if request.method == "POST":
        new_state = request.POST.get("new_state")
        camp = get_object_or_404(Camp, numero=camp_id)

        # Mettre à jour l'état du fichier correspondant
        if file_type == "fil_rouge":
            camp.fil_rouge_etat = new_state
        elif file_type == "fil_bleu":
            camp.fil_bleu_etat = new_state
        elif file_type == "fil_vert":
            camp.fil_vert_etat = new_state
        elif file_type == "CR_prospe":
            camp.CR_prospe_etat = new_state
        elif file_type == "grille_assurance":
            camp.grille_assurance_etat = new_state
        elif file_type == "grille_ddcs":
            camp.grille_ddcs_etat = new_state
        elif file_type == "grille_intendance":
            camp.grille_intendance_etat = new_state
        elif file_type == "fiche_sncf":
            camp.fiche_sncf_etat = new_state
        elif file_type == "procuration_banque":
            camp.procuration_banque_etat = new_state
        elif file_type == "recepisse":
            camp.recepisse_etat = new_state
        elif file_type == "chemins_explo":
            camp.chemins_explo_etat = new_state
        elif file_type == "contrat_location":
            camp.contrat_location_etat = new_state
        elif file_type == "Budget":
            camp.Budget_etat = new_state
        elif file_type == "grille_camp":
            camp.grille_camp_etat = new_state
        else:
            return HttpResponse("Type de fichier invalide.", status=400)
        # Sauvegarder les changements
        camp.save()
        send_mail(
            subject='Retour du QG',
            message=f'L état du fichier {file_type} a été modifié pour le camp {camp.numero}. Connectez-vous sur https://eeif.rezel.net/home',
            from_email='eeif@rezel.net',  # Remplacez par votre adresse e-mail
            recipient_list=[camp.mail],
        )

        # Rediriger vers la page de détails du camp
        return redirect('camp_detail', numero=camp_id)
    return redirect('camp_detail', numero=camp_id)

def modifier_commentaire(request, file_type, camp_id):
    if request.method == 'POST':
        # Récupérer l'objet commission à partir de l'ID
        camp = get_object_or_404(Camp, numero=camp_id)
        
        # Récupérer le commentaire envoyé via le formulaire
        nouveau_commentaire = request.POST.get('commentaire')
        
        if file_type == 'fil_rouge':
            camp.fil_rouge_commentaire = nouveau_commentaire
        elif file_type == 'fil_bleu':
            camp.fil_bleu_commentaire = nouveau_commentaire
        elif file_type == 'fil_vert':
            camp.fil_vert_commentaire = nouveau_commentaire
        elif file_type == 'CR_prospe':
            camp.CR_prospe_commentaire = nouveau_commentaire
        elif file_type == 'grille_assurance':
            camp.grille_assurance_commentaire = nouveau_commentaire
        elif file_type == 'grille_ddcs':
            camp.grille_ddcs_commentaire = nouveau_commentaire
        elif file_type == 'grille_intendance':
            camp.grille_intendance_commentaire = nouveau_commentaire
        elif file_type == 'fiche_sncf':
            camp.fiche_sncf_commentaire = nouveau_commentaire
        elif file_type == 'procuration_banque':
            camp.procuration_banque_commentaire = nouveau_commentaire
        elif file_type == 'recepisse':
            camp.recepisse_commentaire = nouveau_commentaire
        elif file_type == 'chemins_explo':
            camp.chemins_explo_commentaire = nouveau_commentaire
        elif file_type == 'contrat_location':
            camp.contrat_location_commentaire = nouveau_commentaire
        elif file_type == 'Budget':
            camp.Budget_commentaire = nouveau_commentaire
        elif file_type == 'grille_camp':
            camp.grille_camp_commentaire = nouveau_commentaire
        else:
            return HttpResponse("Type de fichier invalide.", status=400)
        # Sauvegarder les changements
        camp.save()
        send_mail(
            subject='Retour du QG',
            message=f'Le commentaire concernant le fichier {file_type} a été modifié pour le camp {camp.numero}. Connectez-vous sur https://eeif.rezel.net/home',
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