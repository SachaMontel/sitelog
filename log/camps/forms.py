from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth.models import Group

class CustomUserCreationForm(UserCreationForm):
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=False,
        label="Groupe",
        help_text="Choisissez le groupe auquel vous appartenez."
    )
    
    class Meta:
        model = CustomUser  # Utilisez votre modèle personnalisé
        fields = ['first_name', 'last_name', 'username','password1', 'password2', 'phone', 'gl',  'camp', 'email']  # Ajoutez vos champs ici

    def save(self, commit=True):
        user = super().save(commit=False)
        group = self.cleaned_data.get('group')
        if commit:
            user.save()
            if group:
                user.groups.add(group)  
                
            if user.camp:
                camp = user.camp
                if not camp.prenomcdc1:
                    camp.prenomcdc1 = user.first_name
                    camp.nomcdc1 = user.last_name
                elif not camp.prenomcdc2:
                    camp.prenomcdc2 = user.first_name
                    camp.nomcdc2 = user.last_name
                camp.save()  # Enregistrer les modifications du modèle Camp# Ajoute l'utilisateur au groupe sélectionné
        return user    