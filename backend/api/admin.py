from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateur, Mentor, Mentee, Session, Ressource, Evaluation,DomaineExpertise, Qualification, Experience, Preference, Langue, Disponibilite, NiveauEducation, Connexion

class UtilisateurAdmin(UserAdmin):
    """
    Configuration de l'interface d'administration pour le modèle Utilisateur.
    """
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff','is_mentor','is_mentee')
    search_fields = ('username', 'email', 'first_name', 'last_name','is_mentor','is_mentee')
    ordering = ('username',)

class MentorAdmin(admin.ModelAdmin):
    """
    Configuration de l'interface d'administration pour le modèle Mentor.
    """
    """
    Admin view for the Mentor model.
    """
    list_display = ('utilisateur',)
    search_fields = ('utilisateur__username', 'utilisateur__email', 'utilisateur__first_name', 'utilisateur__last_name')
    filter_horizontal = ('domaines_expertise', 'qualifications', 'experiences', 'preferences', 'langues', 'disponibilite')

class MenteeAdmin(admin.ModelAdmin):
    """
    Configuration de l'interface d'administration pour le modèle Mentee.
    Admin view for the Mentee model.
    """
    list_display = ('utilisateur',)
    search_fields = ('utilisateur__username', 'utilisateur__email', 'utilisateur__first_name', 'utilisateur__last_name')
    filter_horizontal = ('centres_interet', 'competences_actuelles', 'langues', 'disponibilite')
    list_filter = ('niveau_education',)

class SessionAdmin(admin.ModelAdmin):
    """
    Configuration de l'interface d'administration pour le modèle Session.
    """
    list_display = ('mentor', 'mentee', 'disponibilite', 'type', 'commentaire')
    search_fields = ('mentor__utilisateur__username', 'mentee__utilisateur__username', 'type','commentaire')
    list_filter = ('commentaire', 'type')

class ConnexionAdmin(admin.ModelAdmin):

    list_display = ('mentor', 'mentee', 'score')
    search_fields = ('mentor__utilisateur__username', 'mentee__utilisateur__username', 'score')
    
class RessourceAdmin(admin.ModelAdmin):
    """
    Configuration de l'interface d'administration pour le modèle Ressource.
    """
    list_display = ('titre', 'type', 'domaine', 'mentor')
    search_fields = ('titre', 'type', 'domaine', 'mentor__utilisateur__username')
    list_filter = ('type', 'domaine')

class EvaluationAdmin(admin.ModelAdmin):
    """
    Configuration de l'interface d'administration pour le modèle Evaluation.
    """
    list_display = ('mentor', 'mentee', 'note', 'date')
    search_fields = ('mentor__utilisateur__username', 'mentee__utilisateur__username', 'commentaire')
    list_filter = ('note', 'date')


class DomaineExpertiseAdmin(admin.ModelAdmin):
    """
    Admin view for the DomaineExpertise model.
    """
    list_display = ('name',)
    search_fields = ('name',)

class QualificationAdmin(admin.ModelAdmin):
    """
    Admin view for the Qualification model.
    """
    list_display = ('name',)
    search_fields = ('name',)

class ExperienceAdmin(admin.ModelAdmin):
    """
    Admin view for the Experience model.
    """
    list_display = ('years',)
    search_fields = ('years',)

class PreferenceAdmin(admin.ModelAdmin):
    """
    Admin view for the Preference model.
    """
    list_display = ('name',)
    search_fields = ('name',)


class LangueAdmin(admin.ModelAdmin):
    """
    Admin view for the Langue model.
    """
    list_display = ('name',)
    search_fields = ('name',)


class DisponibiliteAdmin(admin.ModelAdmin):
    """
    Admin view for the Disponibilite model.
    """
    list_display = ('day', 'start_time', 'end_time')
    search_fields = ('day', 'start_time', 'end_time')


class NiveauEducationAdmin(admin.ModelAdmin):
    """
    Admin view for the NiveauEducation model.
    """
    list_display = ('level',)
    search_fields = ('level',)

admin.site.register(Utilisateur, UtilisateurAdmin)
admin.site.register(Mentor, MentorAdmin)
admin.site.register(Mentee, MenteeAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Ressource, RessourceAdmin)
admin.site.register(Evaluation, EvaluationAdmin)
admin.site.register(NiveauEducation, NiveauEducationAdmin)
admin.site.register(Disponibilite,DisponibiliteAdmin)
admin.site.register(Langue,LangueAdmin)
admin.site.register(DomaineExpertise,DomaineExpertiseAdmin)
admin.site.register(Qualification,QualificationAdmin)
admin.site.register(Experience,ExperienceAdmin)
admin.site.register(Preference,PreferenceAdmin)
admin.site.register(Connexion,ConnexionAdmin)