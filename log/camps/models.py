from django.db import models
from django.contrib.auth.models import AbstractUser
import os
from django.contrib.auth.models import Group

GL_CHOICES = (
    ('Aix-en-Provence', 'Aix-en-Provence'),
    ('Antony', 'Antony'),
    ('Barcokhba', 'Barcokhba'),
    ('Bordeaux', 'Bordeaux'),
    ('Buffault', 'Buffault'),
    ('Canada', 'Canada'),
    ('Cannes', 'Cannes'),
    ('Colmar-Mulhouse', 'Colmar-Mulhouse'),
    ('Copernic', 'Copernic'),
    ('Courbevoie', 'Courbevoie'),
    ('Dufrenoy', 'Dufrenoy'),
    ('Golda Meir', 'Golda Meir'),
    ('Grenoble', 'Grenoble'),
    ('Henri Schilli', 'Henri Schilli'),
    ('Israël', 'Israël'),
    ('Issy-les-Moulineaux', 'Issy-les-Moulineaux'),
    ('Koumi SLG', 'Koumi SLG'),
    ('La Victoire', 'La Victoire'),
    ('Paris 12', 'Paris 12'),
    ('Lille', 'Lille'),
    ('Londres', 'Londres'),
    ('Lyon', 'Lyon'),
    ('Marseille', 'Marseille'),
    ('Montpellier', 'Montpellier'),
    ('Nancy-Metz-Luxembourg', 'Nancy-Metz-Luxembourg'),
    ('Neuilly Vert', 'Neuilly Vert'),
    ('Neuilly Rose', 'Neuilly Rose'),
    ('Nice', 'Nice'),
    ('Noam', 'Noam'),
    ('Ori SLG', 'Ori SLG'),
    ('La Roquette', 'La Roquette'),
    ('Paris 17', 'Paris 17'),
    ('Pavillons-sous-bois', 'Pavillons-sous-bois'),
    ('Saint-Brice', 'Saint-Brice'),
    ('Ségur', 'Ségur'),
    ('Shema Israel Bleu', 'Shema Israel Bleu'),
    ('Shema Israel Noir', 'Shema Israel Noir'),
    ('Strasbourg', 'Strasbourg'),
    ('Toulon', 'Toulon'),
    ('Toulouse', 'Toulouse'),
    ('Versailles', 'Versailles'),
    ('Yona', 'Yona'),
    ('NML', 'NML'),
    ('Dor Vador', 'Dor Vador'),
    ('Edmond Fleg', 'Edmond Fleg'),
    ('Neuilly Laurent Kern', 'Neuilly Laurent Kern'),
)

NUMERO_CAMP_CHOICES = (
    ('BB 1', 'BB 1'),
    ('BB 2', 'BB 2'),
    ('BB 3', 'BB 3'),
    ('BB 4', 'BB 4'),
    ('BB 5', 'BB 5'),
    ('BC 1', 'BC 1'),
    ('BC 2', 'BC 2'),
    ('BC 3', 'BC 3'),
    ('BC 4', 'BC 4'),
    ('BC 5', 'BC 5'),
    ('BC 6', 'BC 6'),
    ('BC 7', 'BC 7'),
    ('BC 8', 'BC 8'),
    ('BC 9', 'BC 9'),
    ('BC 10', 'BC 10'),
    ('BC 11', 'BC 11'),
    ('BC 12', 'BC 12'),
    ('BC 13', 'BC 13'),
    ('BC 14', 'BC 14'),
    ('BC 15', 'BC 15'),
    ('BC 16', 'BC 16'),
    ('BC 17', 'BC 17'),
    # BM
    ('BM 1', 'BM 1'),
    ('BM 2', 'BM 2'),
    ('BM 3', 'BM 3'),
    ('BM 4', 'BM 4'),
    ('BM 5', 'BM 5'),
    ('BM 6', 'BM 6'),
    ('BM 7', 'BM 7'),
    ('BM 8', 'BM 8'),
    ('BM 9', 'BM 9'),
    ('BM 10', 'BM 10'),
    ('BM 11', 'BM 11'),
    ('BM 12', 'BM 12'),
    ('BM 13', 'BM 13'),
    ('BM 14', 'BM 14'),
    ('BM 15', 'BM 15'),
    ('BM 16', 'BM 16'),
    ('BM 17', 'BM 17'),
    ('BM 18', 'BM 18'),
    ('BM 19', 'BM 19'),
    ('BM 20', 'BM 20'),
    ('BM 21', 'BM 21'),
    ('BM 22', 'BM 22'),
    ('BM 23', 'BM 23'),
    ('BM 24', 'BM 24'),

    # BP
    ('BP 1', 'BP 1'),
    ('BP 2', 'BP 2'),
    ('BP 3', 'BP 3'),
    ('BP 4', 'BP 4'),
    ('BP 5', 'BP 5'),
    ('BP 6', 'BP 6'),
    ('BP 7', 'BP 7'),
    ('BP 8', 'BP 8'),
    ('BP 9', 'BP 9'),
    ('BP 10', 'BP 10'),
    ('BP 11', 'BP 11'),
)

ETAT_CHOICES = (
    ('Rendu', 'Rendu'),
    ('Validé', 'Validé'),
    ('Refusé', 'Refusé'),
    ('Non rendu', 'Non rendu'),
    ('Retour fait', 'Retour fait'),
    ('En cours', 'En cours'),
)

# Create your models here.
class CustomUser(AbstractUser):

    # Ajoutez vos champs personnalisés ici
    phone = models.CharField("Numéro de téléphone", max_length=15, blank=True, null=True)
    gl = models.CharField("Groupe local", max_length=30, choices=GL_CHOICES, blank=True, null=True)
    camp = models.ForeignKey('Camp', on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    
    # Nouveaux attributs de liens
    lienlog = models.URLField("Lien logistique", max_length=500, blank=True, null=True, help_text="Lien vers la page logistique")
    lienbc = models.URLField("Lien BC", max_length=500, blank=True, null=True, help_text="Lien vers la page BC")
    lienbm = models.URLField("Lien BM", max_length=500, blank=True, null=True, help_text="Lien vers la page BM")

    etatfrbm = models.CharField("État du fil rouge BM", max_length=50, choices=ETAT_CHOICES, blank=True, null=True, default='Non rendu')
    etatfbbm = models.CharField("État du fil bleu BM", max_length=50, choices=ETAT_CHOICES, blank=True, null=True, default='Non rendu')
    etatfrbc = models.CharField("État du fil rouge BC", max_length=50, choices=ETAT_CHOICES, blank=True, null=True, default='Non rendu')
    etatfbbc = models.CharField("État du fil bleu BC", max_length=50, choices=ETAT_CHOICES, blank=True, null=True, default='Non rendu')
    
    etatddcs = models.CharField("État de la grille DDCS", max_length=50, choices=ETAT_CHOICES, blank=True, null=True, default='Non rendu')
    etatgrille = models.CharField("État de la grille de l'annee", max_length=50, choices=ETAT_CHOICES, blank=True, null=True, default='Non rendu')
    
    # Nouvelles étapes BC
    etatprojetactivitebc = models.CharField("État de l'ébauche projet d'activité BC", max_length=50, choices=ETAT_CHOICES, blank=True, null=True, default='Non rendu')
    etatprojetviejuvebc = models.CharField("État de l'ébauche projet vie juive BC", max_length=50, choices=ETAT_CHOICES, blank=True, null=True, default='Non rendu')
    
    commentairefrbm = models.TextField("Commentaire du fil rouge BM", blank=True, null=True, default='')
    commentairefbbm = models.TextField("Commentaire du fil bleu BM", blank=True, null=True, default='')
    commentairefrbc = models.TextField("Commentaire du fil rouge BC", blank=True, null=True, default='')
    commentairefbbc = models.TextField("Commentaire du fil bleu BC", blank=True, null=True, default='')
    commentaireddcs = models.TextField("Commentaire de la grille DDCS", blank=True, null=True, default='')
    commentairegrille = models.TextField("Commentaire de la grille de l'annee", blank=True, null=True, default='')
    
    # Nouveaux commentaires BC
    commentaireprojetactivitebc = models.TextField("Commentaire de l'ébauche projet d'activité BC", blank=True, null=True, default='')
    commentaireprojetviejuvebc = models.TextField("Commentaire de l'ébauche projet vie juive BC", blank=True, null=True, default='')

    def __str__(self):
        return self.username
    
    def change_etat(self, etat_field, new_etat):
        """Change l'état d'un champ spécifique"""
        if hasattr(self, etat_field):
            setattr(self, etat_field, new_etat)
            self.save()
            return True
        return False
    
    def get_etat_choices(self):
        """Retourne les choix d'état simplifiés pour l'interface GL"""
        return [
            ('Non rendu', 'Non rendu'),
            ('Rendu', 'Rendu'),
            ('Validé', 'Validé'),
            ('Refusé', 'Refusé'),
            ('Retour fait', 'Retour fait'),
            ('En cours', 'En cours'),
        ]

class Camp(models.Model):

    numero = models.CharField("Numéro du camp", max_length=30, choices=NUMERO_CAMP_CHOICES, blank=True, null=True, unique=True)
    branche = models.CharField(max_length=50, blank=True, null=True)
    adresse = models.CharField(max_length=50, blank=True, null=True)
    mail = models.EmailField("Adresse e-mail", max_length=254, blank=True, null=True)
    GL1  = models.CharField("Groupe local 1", max_length=30, choices=GL_CHOICES, blank=True, null=True)
    GL2  = models.CharField("Groupe local 2", max_length=30, choices=GL_CHOICES, blank=True, null=True)
    GL3  = models.CharField("Groupe local 3", max_length=30, choices=GL_CHOICES, blank=True, null=True)
    GL4  = models.CharField("Groupe local 4", max_length=30, choices=GL_CHOICES, blank=True, null=True)
    GL5  = models.CharField("Groupe local 5", max_length=30, choices=GL_CHOICES, blank=True, null=True)
    prenomcdc1 = models.CharField("Prénom du chef de camp 1", max_length=50, blank=True, null=True)
    nomcdc1 = models.CharField("Nom du chef de camp 1", max_length=50, blank=True, null=True)
    prenomcdc2 = models.CharField("Prénom du chef de camp 2", max_length=50, blank=True, null=True)
    nomcdc2 = models.CharField("Nom du chef de camp 2", max_length=50, blank=True, null=True)
    staff1 = models.CharField("Staff 1", max_length=50, blank=True, null=True)
    staff2 = models.CharField("Staff 2", max_length=50, blank=True, null=True)
    staff3 = models.CharField("Staff 3", max_length=50, blank=True, null=True)
    enfants = models.CharField("Nombre d'enfants", max_length=50, blank=True, null=True)
    animateurs = models.CharField("Nombre d'animateurs", max_length=50, blank=True, null=True)
    date_JN = models.DateField("Date des JN", blank=True, null=True)
    drive = models.CharField("Lien du drive", max_length=100, blank=True, null=True)

    fil_rouge = models.FileField(upload_to='media/fichiers_camps/fil_rouge/depot/', blank=True, null=True)
    fil_rouge_retour = models.FileField(upload_to='media/fichiers_camps/fil_rouge/retour/', blank=True, null=True)
    fil_rouge_etat = models.CharField("État du fil rouge", max_length=50, choices=ETAT_CHOICES, blank=True, null=True, default='Non rendu')
    fil_rouge_commentaire = models.TextField("Commentaire du fil rouge", blank=True, null=True, default='')
    fil_rouge_deadline = models.CharField("Date limite du fil rouge",max_length=50, blank=True, null=True)

    fil_bleu = models.FileField(upload_to='media/fichiers_camps/fil_bleu/depot/', blank=True, null=True)
    fil_bleu_retour = models.FileField(upload_to='media/fichiers_camps/fil_bleu/retour/', blank=True, null=True)
    fil_bleu_etat = models.CharField("État du fil bleu", max_length=50, choices=ETAT_CHOICES, blank=True, null=True, default='Non rendu')
    fil_bleu_commentaire = models.TextField("Commentaire du fil bleu", blank=True, null=True, default='')
    fil_bleu_deadline = models.CharField("Date limite du fil rouge",max_length=50, blank=True, null=True)

    fil_vert = models.FileField(upload_to='media/fichiers_camps/fil_vert/depot/', blank=True, null=True)
    fil_vert_retour = models.FileField(upload_to='media/fichiers_camps/fil_vert/retour/', blank=True, null=True)
    fil_vert_etat = models.CharField("État du fil vert", max_length=50, choices=ETAT_CHOICES, blank=True, null=True, default='Non rendu')
    fil_vert_commentaire = models.TextField("Commentaire du fil vert", blank=True, null=True, default='')
    fil_vert_deadline = models.CharField("Date limite du fil rouge",max_length=50, blank=True, null=True)

    CR_prospe = models.FileField(upload_to='media/fichiers_camps/CR_prospe/', blank=True, null=True)
    CR_prospe_etat = models.CharField("État du CR prospection", max_length=50, choices=ETAT_CHOICES, blank=True, null=True, default='Non rendu')
    CR_prospe_commentaire = models.TextField("Commentaire du CR prospection", blank=True, null=True, default='')
    CR_prospe_deadline = models.DateField("Date limite du CR prospection", blank=True, null=True)

    contrat_location = models.FileField(upload_to='media/fichiers_camps/contrat_location/', blank=True, null=True)
    contrat_location_etat = models.CharField("État du contrat de location", max_length=50, choices=ETAT_CHOICES, blank=True, null=True, default='Non rendu')
    contrat_location_commentaire = models.TextField("Commentaire du contrat de location", blank=True, null=True, default='')
    contrat_location_deadline = models.CharField("Date limite du contrat de location",max_length=50,  blank=True, null=True, default='28 fevrier')

    Budget = models.FileField(upload_to='media/fichiers_camps/Budget/', blank=True, null=True)
    Budget_etat = models.CharField("État du budget", max_length=50, choices=ETAT_CHOICES, blank=True, null=True, default='Non rendu')
    Budget_commentaire = models.TextField("Commentaire du budget", blank=True, null=True, default='')
    Budget_deadline = models.CharField("Date limite du budget",max_length=50, blank=True, null=True,  default='Debut mai')

    Budgetreal = models.FileField(upload_to='media/fichiers_camps/Budgetreal/', blank=True, null=True)
    Budgetreal_etat = models.CharField("État du budget", max_length=50, choices=ETAT_CHOICES, blank=True, null=True, default='Non rendu')
    Budgetreal_commentaire = models.TextField("Commentaire du budget", blank=True, null=True, default='')
    Budgetreal_deadline = models.CharField("Date limite du budget",max_length=50, blank=True, null=True,  default='11 mai')

    voiture = models.FileField(upload_to='media/fichiers_camps/voiture/', blank=True, null=True)
    voiture_etat = models.CharField("État du budget", max_length=50, choices=ETAT_CHOICES, blank=True, null=True, default='Non rendu')
    voiture_commentaire = models.TextField("Commentaire du budget", blank=True, null=True, default='')
    voiture_deadline = models.CharField("Date limite du budget",max_length=50, blank=True, null=True,  default='Debut mai')

    grille_assurance = models.FileField(upload_to='media/fichiers_camps/grille_assurance/', blank=True, null=True)
    grille_assurance_etat = models.CharField("État de la grille d'assurance", max_length=50, choices=ETAT_CHOICES, blank=True, null=True, default='Non rendu')
    grille_assurance_commentaire = models.TextField("Commentaire de la grille d'assurance", blank=True, null=True, default='')
    grille_assurance_deadline = models.CharField("Date limite de la grille d'assurance",max_length=50, blank=True, null=True)

    grille_ddcs = models.FileField(upload_to='media/fichiers_camps/grille_ddcs/', blank=True, null=True)
    grille_ddcs_etat = models.CharField("État de la grille DDCS", max_length=50, choices=ETAT_CHOICES, blank=True, null=True, default='Non rendu')
    grille_ddcs_commentaire = models.TextField("Commentaire de la grille DDCS", blank=True, null=True, default='')
    grille_ddcs_deadline = models.CharField("Date limite de la grille DDCS",max_length=50,blank=True, null=True)

    grille_intendance = models.FileField(upload_to='media/fichiers_camps/grille_intendance/', blank=True, null=True)
    grille_intendance_etat = models.CharField("État de la grille intendance", max_length=50, choices=ETAT_CHOICES, blank=True, null=True, default='Non rendu')
    grille_intendance_commentaire = models.TextField("Commentaire de la grille intendance", blank=True, null=True, default='')
    grille_intendance_deadline = models.CharField("Date limite de la grille intendance",max_length=50, blank=True, null=True)

    intendance2 = models.FileField(upload_to='media/fichiers_camps/intendance2/', blank=True, null=True)
    intendance2_etat = models.CharField("État de la grille intendance", max_length=50, choices=ETAT_CHOICES, blank=True, null=True, default='Non rendu')
    intendance2_commentaire = models.TextField("Commentaire de la grille intendance", blank=True, null=True, default='')
    intendance2_deadline = models.CharField("Date limite de la grille intendance",max_length=50, blank=True, null=True, default='15 avril')

    JN = models.FileField(upload_to='media/fichiers_camps/JN/', blank=True, null=True)
    JN_etat = models.CharField("État de la grille intendance", max_length=50, choices=ETAT_CHOICES, blank=True, null=True, default='Non rendu')
    JN_commentaire = models.TextField("Commentaire de la grille intendance", blank=True, null=True, default='')
    JN_deadline = models.CharField("Date limite de la grille intendance",max_length=50, blank=True, null=True, default='Mi-avril')

    fiche_sncf = models.FileField(upload_to='media/fichiers_camps/fiche_sncf/', blank=True, null=True)
    fiche_sncf_etat = models.CharField("État de la fiche SNCF",max_length=50,  choices=ETAT_CHOICES, blank=True, null=True, default='Non rendu')
    fiche_sncf_commentaire = models.TextField("Commentaire de la fiche SNCF", blank=True, null=True, default='')
    fiche_sncf_deadline = models.CharField("Date limite de la fiche SNCF",max_length=50,blank=True, null=True)

    procuration_banque = models.FileField(upload_to='media/fichiers_camps/procuration_banque/', blank=True, null=True)
    procuration_banque_etat = models.CharField("État de la procuration bancaire", max_length=50, choices=ETAT_CHOICES, blank=True, null=True, default='Non rendu')
    procuration_banque_commentaire = models.TextField("Commentaire de la procuration bancaire", blank=True, null=True, default='')
    procuration_banque_deadline = models.DateField("Date limite de la procuration bancaire", blank=True, null=True)

    recepisse = models.FileField(upload_to='media/fichiers_camps/recepisse/', blank=True, null=True)
    recepisse_etat = models.CharField("État du récépissé", max_length=50, choices=ETAT_CHOICES, blank=True, null=True, default='Non rendu')
    recepisse_commentaire = models.TextField("Commentaire du récépissé", blank=True, null=True, default='')
    recepisse_deadline = models.DateField("Date limite du récépissé", blank=True, null=True)

    grille_camp = models.FileField(upload_to='media/fichiers_camps/grille_camp/', blank=True, null=True)
    grille_camp_etat = models.CharField("État de la grille camp", max_length=50, choices=ETAT_CHOICES, blank=True, null=True, default='Non rendu')
    grille_camp_commentaire = models.TextField("Commentaire de la grille camp", blank=True, null=True, default='')
    grille_camp_deadline = models.CharField("Date limite de la grille camp",max_length=50, blank=True, null=True)

    chemins_explo = models.FileField(upload_to='media/fichiers_camps/chemins_explo/', blank=True, null=True)
    chemins_explo_etat = models.CharField("État des chemins d'exploitation", max_length=50, choices=ETAT_CHOICES, blank=True, null=True, default='Non rendu')
    chemins_explo_commentaire = models.TextField("Commentaire des chemins d'exploitation", blank=True, null=True, default='')
    chemins_explo_deadline = models.DateField("Date limite des chemins d'exploitation", blank=True, null=True)

    demande_prospe = models.FileField(upload_to='media/fichiers_camps/demande_prospe/', blank=True, null=True)
    demande_prospe_etat = models.CharField("État de la demande de prospe", max_length=50, choices=ETAT_CHOICES, blank=True, null=True, default='Non rendu')
    demande_prospe_commentaire = models.TextField("Commentaire de demande de prospe", blank=True, null=True, default='')
    demande_prospe_deadline = models.CharField("Date limite demande de prospe", max_length=50, blank=True, null=True, default='30 Janvier')

    docACM = models.FileField(upload_to='media/fichiers_camps/docACM/', blank=True, null=True)
    docACM_etat = models.CharField("État de la demande de prospe", max_length=50, choices=ETAT_CHOICES, blank=True, null=True, default='Non rendu')
    docACM_commentaire = models.TextField("Commentaire de demande de prospe", blank=True, null=True, default='')
    docACM_deadline = models.CharField("Date limite demande de prospe", max_length=50, blank=True, null=True, default='Début juin')

    projetv1 = models.FileField(upload_to='media/fichiers_camps/projetv1/depot/', blank=True, null=True)
    projetv1_retour = models.FileField(upload_to='media/fichiers_camps/projetv1/retour/', blank=True, null=True)
    projetv1_etat = models.CharField("État de la demande de prospe", max_length=50, choices=ETAT_CHOICES, blank=True, null=True, default='Non rendu')
    projetv1_commentaire = models.TextField("Commentaire de demande de prospe", blank=True, null=True, default='')
    projetv1_deadline = models.CharField("Date limite demande de prospe", max_length=50, blank=True, null=True, default='18 mars')

    projetvf = models.FileField(upload_to='media/fichiers_camps/projetvf/depot/', blank=True, null=True)
    projetvf_retour = models.FileField(upload_to='media/fichiers_camps/projetvf/retour/', blank=True, null=True)
    projetvf_etat = models.CharField("État de la demande de prospe", max_length=50, choices=ETAT_CHOICES, blank=True, null=True, default='Non rendu')
    projetvf_commentaire = models.TextField("Commentaire de demande de prospe", blank=True, null=True, default='')
    projetvf_deadline = models.CharField("Date limite demande de prospe", max_length=50, blank=True, null=True, default='2 semaines après les JN')

    PAF_etat = models.CharField("État de la PAF", max_length=50, choices=ETAT_CHOICES, blank=True, null=True, default='Non rendu')
    PAF_deadline = models.CharField("Date limite de la PAF", max_length=50, blank=True, null=True, default='14 Fevrier')

    BP = models.FileField(upload_to='media/fichiers_camps/bp/', blank=True, null=True)
    BP_etat = models.CharField("État du BP", max_length=50, choices=ETAT_CHOICES, blank=True, null=True, default='Non rendu')
    BP_commentaire = models.TextField("Commentaire de demande de prospe", blank=True, null=True, default='')
    BP_deadline = models.CharField("Date limite du BP", max_length=50, blank=True, null=True, default='30 Janvier')

    V1GC = models.FileField(upload_to='media/fichiers_camps/v1gc/', blank=True, null=True)
    V1GC_etat = models.CharField("État du V1GC", max_length=50, choices=ETAT_CHOICES, blank=True, null=True, default='Non rendu')
    V1GC_commentaire = models.TextField("Commentaire de demande de prospe", blank=True, null=True, default='')
    V1GC_deadline = models.CharField("Date limite du V1GC", max_length=50, blank=True, null=True, default='30 Janvier')

    PPTPV = models.FileField(upload_to='media/fichiers_camps/pptpv/', blank=True, null=True)
    PPTPV_etat = models.CharField("État du PPTPV", max_length=50, choices=ETAT_CHOICES, blank=True, null=True, default='Non rendu')
    PPTPV_commentaire = models.TextField("Commentaire de demande de prospe", blank=True, null=True, default='')
    PPTPV_deadline = models.CharField("Date limite du PPTPV", max_length=50, blank=True, null=True, default='30 Janvier')

    casting = models.FileField(upload_to='media/fichiers_camps/casting/', blank=True, null=True)
    casting_etat = models.CharField("État du Casting", max_length=50, choices=ETAT_CHOICES, blank=True, null=True, default='Non rendu')
    casting_commentaire = models.TextField("Commentaire de demande de prospe", blank=True, null=True, default='')
    casting_deadline = models.CharField("Date limite du Casting", max_length=50, blank=True, null=True, default='30 Janvier')

    devisbillet = models.FileField(upload_to='media/fichiers_camps/devisbillet/', blank=True, null=True)
    devisbillet_etat = models.CharField("État du devisbillet", max_length=50, choices=ETAT_CHOICES, blank=True, null=True, default='Non rendu')
    devisbillet_commentaire = models.TextField("Commentaire de demande de prospe", blank=True, null=True, default='')
    devisbillet_deadline = models.CharField("Date limite du devisbillet", max_length=50, blank=True, null=True, default='30 Janvier')

    PPP = models.FileField(upload_to='media/fichiers_camps/ppp/', blank=True, null=True)
    PPP_etat = models.CharField("État du PPP", max_length=50, choices=ETAT_CHOICES, blank=True, null=True, default='Non rendu')
    PPP_commentaire = models.TextField("Commentaire de demande de prospe", blank=True, null=True, default='')
    PPP_deadline = models.CharField("Date limite du PPP", max_length=50, blank=True, null=True, default='30 Janvier')

    devislogement = models.FileField(upload_to='media/fichiers_camps/devislogement/', blank=True, null=True)
    devislogement_etat = models.CharField("État du devislogement", max_length=50, choices=ETAT_CHOICES, blank=True, null=True, default='Non rendu')
    devislogement_commentaire = models.TextField("Commentaire de demande de prospe", blank=True, null=True, default='')
    devislogement_deadline = models.CharField("Date limite du devislogement", max_length=50, blank=True, null=True, default='30 Janvier')

    PPPc = models.FileField(upload_to='media/fichiers_camps/pppc/', blank=True, null=True)
    PPPc_etat = models.CharField("État du PPPc", max_length=50, choices=ETAT_CHOICES, blank=True, null=True, default='Non rendu')
    PPPc_commentaire = models.TextField("Commentaire de demande de prospe", blank=True, null=True, default='')
    PPPc_deadline = models.CharField("Date limite du PPPc", max_length=50, blank=True, null=True, default='30 Janvier')

    V2GC = models.FileField(upload_to='media/fichiers_camps/v2gc/', blank=True, null=True)
    V2GC_etat = models.CharField("État du V2GC", max_length=50, choices=ETAT_CHOICES, blank=True, null=True, default='Non rendu')
    V2GC_commentaire = models.TextField("Commentaire de demande de prospe", blank=True, null=True, default='')
    V2GC_deadline = models.CharField("Date limite du V2GC", max_length=50, blank=True, null=True, default='30 Janvier')

    GI = models.FileField(upload_to='media/fichiers_camps/gi/', blank=True, null=True)
    GI_etat = models.CharField("État du GI", max_length=50, choices=ETAT_CHOICES, blank=True, null=True, default='Non rendu')
    GI_commentaire = models.TextField("Commentaire de demande de prospe", blank=True, null=True, default='')
    GI_deadline = models.CharField("Date limite du GI", max_length=50, blank=True, null=True, default='30 Janvier')

    VFGC = models.FileField(upload_to='media/fichiers_camps/vfgc/', blank=True, null=True)
    VFGC_etat = models.CharField("État du VFGC", max_length=50, choices=ETAT_CHOICES, blank=True, null=True, default='Non rendu')
    VFGC_commentaire = models.TextField("Commentaire de demande de prospe", blank=True, null=True, default='')
    VFGC_deadline = models.CharField("Date limite du VFGC", max_length=50, blank=True, null=True, default='30 Janvier')

    



    def count_validated_files(self):
        """Compter le nombre de fichiers validés."""
        valid_states = ['Validé']
        fields = [ self.fil_rouge_etat,
self.fil_bleu_etat,
self.fil_vert_etat,
self.CR_prospe_etat,
self.grille_assurance_etat,
self.grille_ddcs_etat,
self.grille_intendance_etat,
self.fiche_sncf_etat,
self.procuration_banque_etat,
self.recepisse_etat,
self.chemins_explo_etat,
self.contrat_location_etat,
self.Budget_etat,
self.grille_camp_etat,
self.demande_prospe_etat,
self.PAF_etat,
self.projetv1_etat,
self.intendance2_etat,
self.JN_etat,
self.voiture_etat,
self.projetvf_etat,
self.Budgetreal_etat,
self.docACM_etat
        ]
        return sum(1 for field in fields if field in valid_states) + (1 if self.PAF_etat == 'Rendu' else 0)

    def count_rendered_files(self):
        """Compter le nombre de fichiers rendus."""
        rendered_states = ['Rendu']
        fields = [self.fil_rouge_etat,
self.fil_bleu_etat,
self.fil_vert_etat,
self.CR_prospe_etat,
self.grille_assurance_etat,
self.grille_ddcs_etat,
self.grille_intendance_etat,
self.fiche_sncf_etat,
self.procuration_banque_etat,
self.recepisse_etat,
self.chemins_explo_etat,
self.contrat_location_etat,
self.Budget_etat,
self.grille_camp_etat,
self.demande_prospe_etat,
self.projetv1_etat,
self.intendance2_etat,
self.JN_etat,
self.voiture_etat,
self.projetvf_etat,
self.Budgetreal_etat,
self.docACM_etat

        ]
        return sum(1 for field in fields if field in rendered_states)


    fichiers_valides = property(count_validated_files)
    fichiers_rendus = property(count_rendered_files)

    def delete_old_file(self, field_name):
        """Supprime l'ancien fichier avant d'enregistrer un nouveau fichier."""
        field = getattr(self, field_name, None)
        if field and os.path.isfile(field.path):
            os.remove(field.path)

    def __str__(self):
        return self.numero
    
