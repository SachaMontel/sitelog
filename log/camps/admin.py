from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Camp

    # Ajoutez vos champs personnalisés à l'interface admin
class CustomUserAdmin(UserAdmin):
    # Ajouter la nouvelle section "Attributs"
    fieldsets = UserAdmin.fieldsets + (
        ('Attributs', {
            'fields': ('phone', 'gl', 'camp' )  # Remplacez par les champs que vous voulez dans cette section
        }),
    )

    # Ajouter ces champs dans la création si nécessaire
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Attributs', {
            'fields': ('phone', 'gl', 'camp', 'password1', 'password2')  # Remplacez par les champs que vous voulez dans cette,
        }),
    )


# Enregistrer le modèle personnalisé dans l'admin
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Camp)