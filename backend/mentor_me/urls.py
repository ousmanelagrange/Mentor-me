
from django.contrib import admin
from django.urls import path, include

from api.views import LoginView,ConnexionViewSet,SessionViewSet,RessourceViewSet,EvaluationViewSet,match_mentor_to_mentee

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/connexion/', ConnexionViewSet.as_view(), name='connexion'),
    path('api/sessions/', SessionViewSet.as_view(), name='sessions'),
    path('api/ressources/', RessourceViewSet.as_view(), name='ressources'),
    path('api/evaluation/', EvaluationViewSet.as_view(), name='evaluation'),
    path('api/matching/', match_mentor_to_mentee, name='matchin'),
]
