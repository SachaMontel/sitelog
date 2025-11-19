from django import forms

class PhotoUploadForm(forms.Form):
    photo = forms.ImageField(label="Ajouter une photo")

class MessageForm(forms.Form):
    texte = forms.CharField(
        label="Message",
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 40, 'placeholder': 'Entrez votre message...'})
    )
    auteur = forms.CharField(
        label="Auteur",
        max_length=200,
        widget=forms.TextInput(attrs={'placeholder': 'Votre nom'})
    )

