from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdminUtilisateurViewSet, DisponibiliteViewSet, DomaineExpertiseViewSet, ExperienceViewSet, LangueViewSet, NiveauEducationViewSet, PreferenceViewSet, QualificationViewSet,UtilisateurViewSet, MentorViewSet, MenteeViewSet, SessionViewSet, RessourceViewSet, EvaluationViewSet,ConnexionViewSet
from .views import LoginView
router = DefaultRouter()
router.register(r'utilisateurs', UtilisateurViewSet)
# router.register(r'admin/auth', AdminUtilisateurViewSet)
router.register(r'mentors', MentorViewSet)
router.register(r'mentees', MenteeViewSet)
router.register(r'domaines_expertise', DomaineExpertiseViewSet)
router.register(r'qualifications', QualificationViewSet)
router.register(r'experiences', ExperienceViewSet)
router.register(r'preferences', PreferenceViewSet)
router.register(r'langues', LangueViewSet)
router.register(r'disponibilites', DisponibiliteViewSet)
router.register(r'niveau_education', NiveauEducationViewSet)



urlpatterns = [
    path('', include(router.urls)),
    path('utilisateurs/login/', LoginView.as_view(), name='login'),
]
