from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from .models import Utilisateur, Mentor, Mentee, Session, Ressource, Evaluation
from .permissions import *
from rest_framework.permissions import IsAuthenticated
from .models import Utilisateur, Mentor, Mentee, Session, Ressource, Evaluation,DomaineExpertise, Qualification, Experience, Preference, Langue, Disponibilite, NiveauEducation,Connexion
from .serializers import (
    UtilisateurSerializer, DomaineExpertiseSerializer, QualificationSerializer, ExperienceSerializer, PreferenceSerializer, LangueSerializer, DisponibiliteSerializer, NiveauEducationSerializer,MentorSerializer, MenteeSerializer,
    SessionSerializer, RessourceSerializer, EvaluationSerializer,
    MentorRegistrationSerializer, MenteeRegistrationSerializer,ConnexionSerializer
)

from django.contrib.auth import login
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import LoginSerializer
from django.shortcuts import get_object_or_404
from api.matchin_service import Matching_service

class DomaineExpertiseViewSet(viewsets.ModelViewSet):
    queryset = DomaineExpertise.objects.all()
    serializer_class = DomaineExpertiseSerializer

class QualificationViewSet(viewsets.ModelViewSet):
    queryset = Qualification.objects.all()
    serializer_class = QualificationSerializer

class ExperienceViewSet(viewsets.ModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer

class PreferenceViewSet(viewsets.ModelViewSet):
    queryset = Preference.objects.all()
    serializer_class = PreferenceSerializer

class LangueViewSet(viewsets.ModelViewSet):
    queryset = Langue.objects.all()
    serializer_class = LangueSerializer

class DisponibiliteViewSet(viewsets.ModelViewSet):
    queryset = Disponibilite.objects.all()
    serializer_class = DisponibiliteSerializer

class NiveauEducationViewSet(viewsets.ModelViewSet):
    queryset = NiveauEducation.objects.all()
    serializer_class = NiveauEducationSerializer

class UtilisateurViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les opérations CRUD sur le modèle Utilisateur.
    """
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """
        Retourne le serializer approprié pour les actions.
        """
        if self.action in ['create', 'update', 'partial_update']:
            return UtilisateurSerializer
        return super().get_serializer_class()

class MentorViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les opérations CRUD sur le modèle Mentor.
    """
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer
    # permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """
        Retourne le serializer approprié pour les actions.
        """
        if self.action in ['create', 'update', 'partial_update']:
            return MentorRegistrationSerializer
        return super().get_serializer_class()

class MenteeViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les opérations CRUD sur le modèle Mentee.
    """
    queryset = Mentee.objects.all()
    serializer_class = MenteeSerializer
    # permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """
        Retourne le serializer approprié pour les actions.
        """
        if self.action in ['create', 'update', 'partial_update']:
            return MenteeRegistrationSerializer
        return super().get_serializer_class()


class AdminUtilisateurViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les opérations CRUD sur le modèle Utilisateur.
    """
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer
    permission_classes = [IsAdminAuthenticated]
class UtilisateurViewSet(viewsets.ModelViewSet):
    """
    #ViewSet pour gérer les opérations CRUD sur le modèle Utilisateur.
    """
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer
    # permission_classes = [IsAuthenticated]lc
@api_view(['GET'])
def match_mentor_to_mentee(request):
    mentors = Mentor.objects.all()
    mentee = Mentee.objects.get(id =2)
    matches = {}
    matching_service = Matching_service()
    best_match = None
    best_similarity = -1

    for mentor in mentors:
        
        similarity = matching_service.calculate_similarity(mentor, mentee)
        print(similarity)
        # Trouver le meilleur match pour ce mentee
        if similarity > best_similarity:
            best_similarity = similarity
            best_match = mentor
            matches={
                'mentor_id': best_match.id,
                'mentee_id': mentee.id,
                'similarity': best_similarity
            }
    
    return Response(matches)
class MatchinView(APIView):
    def get(self, request, *args, **kwargs):
        mentors= Mentor.objects.all()
        mentee = Mentee.objects.get(id =1)
        matching_service = Matching_service()
        print(matching_service.calculate_similarity(mentor,mentee))
        return Response({"data":matching_service}, status=status.HTTP_200_OK)
class ConnexionViewSet(APIView):
    def post(self, request):
        id = request.data["id"]
        type_user = request.data["type_user"]
        if type_user == "mentor":
            mentor = Mentor.objects.get(id = id)
            connexions = Connexion.objects.filter(mentor=mentor)
            data = []
            for connexion in connexions:
                data.append({"id":connexion.mentee.id, 'username': connexion.mentee.utilisateur.username,
            'email': connexion.mentor.utilisateur.email,
            'first_name': connexion.mentee.utilisateur.first_name,
            'last_name': connexion.mentee.utilisateur.last_name})
            
            return Response({"data":data}, status=status.HTTP_200_OK)
        
        if type_user == "mentee":
            mentee = Mentee .objects.get(id = id)
            connexion = Connexion.objects.get(mentee = mentee)

            data={"id":connexion.mentor.id, 
            'username': connexion.mentor.utilisateur.username,
            'email': connexion.mentor.utilisateur.email,
            'first_name': connexion.mentor.utilisateur.first_name,
            'last_name': connexion.mentor.utilisateur.last_name}
            return Response({"data":data}, status=status.HTTP_200_OK)
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            if user.is_mentor:
                mentor = Mentor.objects.get(utilisateur=user)
                data = {
                    "is_mentee":False,
                "is_mentor":True,
                    "id":mentor.id,
            'username': mentor.utilisateur.username,
            'email': mentor.utilisateur.email,
            'first_name': mentor.utilisateur.first_name,
            'last_name': mentor.utilisateur.last_name,
            'domaines_expertise': [{"id":domaines_expertise.id,"name":domaines_expertise.name}  for domaines_expertise in mentor.domaines_expertise.all()],
            'qualifications': [{"id":qualifications.id,"name":qualifications.name}  for qualifications in mentor.qualifications.all()],
            'experiences': [{"id":experiences.id,"name":experiences.years}  for experiences in mentor.experiences.all()],
            'preferences': [{"id":preferences.id,"name":preferences.name}  for preferences in mentor.preferences.all() ],
            'langues':[{"id":langues.id,"name":langues.name}  for langues in mentor.langues.all()],
            'disponibilite': {
                "id":[disponibilite.id for disponibilite in mentor.disponibilite.all()],
                "day":[disponibilite.day for disponibilite in mentor.disponibilite.all()],
                "start_time":[disponibilite.start_time for disponibilite in mentor.disponibilite.all()],
                "end_time":[disponibilite.end_time for disponibilite in mentor.disponibilite.all()],
            }}
            if user.is_mentee:
                mentee = Mentee.objects.get(utilisateur=user)
                data = {
                    "id":mentee.id,
                "is_mentee":True,
                "is_mentor":False,
                'username': mentee.utilisateur.username,
                'email': mentee.utilisateur.email,
                'first_name': mentee.utilisateur.first_name,
                'last_name': mentee.utilisateur.last_name,
                'centres_interet': [{"id":centre_interet.id,"name":centre_interet.name} for centre_interet in mentee.centres_interet.all()],
                'objectifs': [{"id":objectif.id,"name":objectif.name} for objectif in mentee.objectifs.all()],
                'niveau_education': [{"id":niveau_education.id,"name":niveau_education.level}  for niveau_education in mentee.niveau_education.all()],
                'competences_actuelles': [{"id":competence.id,"name":competence.name} for competence in mentee.competences_actuelles.all()],
                'langue': [{"id":langue.id,"name":langue.name} for langue in mentee.langues.all()],
                'disponibilite': {
                "id":[disponibilite.id for disponibilite in mentee.disponibilite.all()],
                "day":[disponibilite.day for disponibilite in mentee.disponibilite.all()],
                "start_time":[disponibilite.start_time for disponibilite in mentee.disponibilite.all()],
                "end_time":[disponibilite.end_time for disponibilite in mentee.disponibilite.all()],
            }
                }
            return Response({"message": "Login successful","is_mentor":user.is_mentor,"is_mentee":user.is_mentee,"data":data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SessionViewSet(APIView):
    """
    ViewSet pour gérer les opérations CRUD sur le modèle Session.
    """
    def post(self, request):
        data = request.data
        if data["action"]==1:
            mentor = Mentor.objects.get(id=data['mentor'])
            mentee = Mentee.objects.get(id=data['mentee'])
            disponibilite = Disponibilite.objects.get(id=data['disponibilite'])
            session = Session.objects.create(mentor=mentor, mentee=mentee, disponibilite=disponibilite,commentaire = data['commentaire'],type=data['type'])
            datas={
                "mentor":session.mentor.utilisateur.first_name+" "+session.mentor.utilisateur.last_name, 
                "mentee":session.mentee.utilisateur.first_name+" "+session.mentee.utilisateur.last_name,
                'commentaire': session.commentaire,
                'type': session.type,
                'disponibilite':  {
                    "id":disponibilite.id ,
                    "day":disponibilite.day ,
                    "start_time":disponibilite.start_time,
                    "end_time":disponibilite.end_time }
            }
            return Response({"data":datas}, status=status.HTTP_200_OK)
        if data["action"]==2:
            mentor = Mentor.objects.get(id=data['mentor'])
            sessions = Session.objects.filter(mentor=mentor)
            datas =[]
            for session in sessions:
                dat = {
                "mentor":session.mentor.utilisateur.first_name+" "+session.mentor.utilisateur.last_name, 
                "mentee":session.mentee.utilisateur.first_name+" "+session.mentee.utilisateur.last_name,
                'commentaire': session.commentaire,
                'type': session.type,
                'disponibilite':  {
                    "id":session.disponibilite.id ,
                    "day":session.disponibilite.day ,
                    "start_time":session.disponibilite.start_time,
                    "end_time":session.disponibilite.end_time }
                }
                datas.append(dat)
            return Response(datas, status=status.HTTP_200_OK)
        
        if data["action"]==5:
            mentee = Mentee.objects.get(id=data['mentee'])
            sessions = Session.objects.filter(mentee=mentee)
            datas =[]
            for session in sessions:
                dat = {
                "mentor":session.mentor.utilisateur.first_name+" "+session.mentor.utilisateur.last_name, 
                "mentee":session.mentee.utilisateur.first_name+" "+session.mentee.utilisateur.last_name,
                'commentaire': session.commentaire,
                'type': session.type,
                'disponibilite':  {
                    "id":session.disponibilite.id ,
                    "day":session.disponibilite.day ,
                    "start_time":session.disponibilite.start_time,
                    "end_time":session.disponibilite.end_time }
                }
                datas.append(dat)
            return Response(datas, status=status.HTTP_200_OK)
        
class RessourceViewSet(APIView):
    """
    ViewSet pour gérer les opérations CRUD sur le modèle Ressource.
    """
    def post(self, request):
        data = request.data
        if data["action"]==3:
            mentor = Mentor.objects.get(id=data['mentor'])
            mentee = Mentee.objects.get(id=data['mentee'])
            domaine = DomaineExpertise.objects.get(id=data['domaine'])
            ressource = Ressource.objects.create(mentor=mentor, mentee=mentee, domaine=domaine,titre = data['titre'],url = data['url'],type=data['type'])
            datas={
                "mentor":ressource.mentor.utilisateur.first_name+" "+ressource.mentor.utilisateur.last_name, 
                "mentee":ressource.mentee.utilisateur.first_name+" "+ressource.mentee.utilisateur.last_name,
                'titre': ressource.titre,
                'type': ressource.type,
                'url': ressource.url,
                'domaine': ressource.domaine.name,
            }
            return Response({"data":datas}, status=status.HTTP_200_OK)
        if data["action"]==4:
            mentor = Mentor.objects.get(id=data['mentor'])
            ressources = Ressource.objects.filter(mentor=mentor)
            datas =[]
            for ressource in ressources:
                dat = {
                "mentor":ressource.mentor.utilisateur.first_name+" "+ressource.mentor.utilisateur.last_name, 
                "mentee":ressource.mentee.utilisateur.first_name+" "+ressource.mentee.utilisateur.last_name,
                'titre': ressource.titre,
                'type': ressource.type,
                'url': ressource.url,
                'domaine': ressource.domaine.name,
                }
                datas.append(dat)
            return Response(datas, status=status.HTTP_200_OK)

        if data["action"]==6:
            mentee = Mentee.objects.get(id=data['mentee'])
            ressources = Ressource.objects.filter(mentee=mentee)
            datas =[]
            for ressource in ressources:
                dat = {
                "mentor":ressource.mentor.utilisateur.first_name+" "+ressource.mentor.utilisateur.last_name, 
                "mentee":ressource.mentee.utilisateur.first_name+" "+ressource.mentee.utilisateur.last_name,
                'titre': ressource.titre,
                'type': ressource.type,
                'url': ressource.url,
                'domaine': ressource.domaine.name,
                }
                datas.append(dat)
            return Response(datas, status=status.HTTP_200_OK)

class EvaluationViewSet(APIView):
    """
    ViewSet pour gérer les opérations CRUD sur le modèle Evaluation.
    """
    def post(self, request):
        data = request.data
        if data["action"]==7:
            
            mentee = Mentee.objects.get(id=data['mentee'])
            mentor = Connexion.objects.get(mentee=mentee).mentor

            evaluation = Evaluation.objects.create(mentor=mentor, mentee=mentee, note= data['note'],commentaire = data['commentaire'],date=data['date'])
            datas={
                "mentor":evaluation.mentor.utilisateur.first_name+" "+evaluation.mentor.utilisateur.last_name, 
                "mentee":evaluation.mentee.utilisateur.first_name+" "+evaluation.mentee.utilisateur.last_name,
                'commentaire': evaluation.commentaire,
                'note': evaluation.note,
                'date': evaluation.date,
            }
            return Response({"data":datas}, status=status.HTTP_200_OK)
        if data["action"]==8:
            mentor = Mentor.objects.get(id=data['mentor'])
            evaluations = Evaluation.objects.filter(mentor=mentor)
            datas =[]
            for evaluation in evaluations:
                dat = {
                "mentor":evaluation.mentor.utilisateur.first_name+" "+evaluation.mentor.utilisateur.last_name, 
                "mentee":evaluation.mentee.utilisateur.first_name+" "+evaluation.mentee.utilisateur.last_name,
                'commentaire': evaluation.commentaire,
                'note': evaluation.note,
                'date': evaluation.date,
                }
                datas.append(dat)
            return Response(datas, status=status.HTTP_200_OK)
        
        if data["action"]==9:
            mentee = Mentee.objects.get(id=data['mentee'])
            evaluations = Evaluation.objects.filter(mentee=mentee)
            datas =[]
            for evaluation in evaluations:
                dat = {
                "mentor":evaluation.mentor.utilisateur.first_name+" "+evaluation.mentor.utilisateur.last_name, 
                "mentee":evaluation.mentee.utilisateur.first_name+" "+evaluation.mentee.utilisateur.last_name,
                'commentaire': evaluation.commentaire,
                'note': evaluation.note,
                'date': evaluation.date,
                }
                datas.append(dat)
            return Response(datas, status=status.HTTP_200_OK)
