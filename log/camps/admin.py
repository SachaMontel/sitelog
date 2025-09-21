from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Camp

    # Ajoutez vos champs personnalisés à l'interface admin
class CustomUserAdmin(UserAdmin):
    # Champs à afficher dans la liste des utilisateurs
    list_display = ('username', 'email', 'first_name', 'last_name', 'gl', 'camp', 'lienlog', 'lienbc', 'lienbm')
    list_filter = ('gl', 'camp', 'group', 'is_staff', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'gl')
    
    # Ajouter la nouvelle section "Attributs"
    fieldsets = UserAdmin.fieldsets + (
        ('Attributs', {
            'fields': ('phone', 'gl', 'camp', 'group')  # Champs personnalisés existants
        }),
        ('Liens', {
            'fields': ('lienlog', 'lienbc', 'lienbm')  # Nouveaux champs de liens
        }),
    )

    # Ajouter ces champs dans la création si nécessaire
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Attributs', {
            'fields': ('phone', 'gl', 'camp', 'group')  # Champs personnalisés pour la création
        }),
        ('Liens', {
            'fields': ('lienlog', 'lienbc', 'lienbm')  # Nouveaux champs de liens
        }),
    )


# Enregistrer le modèle personnalisé dans l'admin
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Camp)