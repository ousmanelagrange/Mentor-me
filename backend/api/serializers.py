from rest_framework import serializers
from .models import Utilisateur, Mentor, Mentee, Session, Ressource, Evaluation,DomaineExpertise, Qualification, Experience, Preference, Langue, Disponibilite, NiveauEducation,Connexion
from django.contrib.auth import authenticate
from api.matchin_service import Matching_service


class ConnexionSerializer(serializers.ModelSerializer):
    class Meta:
        model= Connexion
        fields = ["mentor","mentee","score"]
class DomaineExpertiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DomaineExpertise
        fields = ['id', 'name']

class QualificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qualification
        fields = ['id', 'name']

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ['id', 'years']

class PreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preference
        fields = ['id', 'name']

class LangueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Langue
        fields = ['id', 'name']

class DisponibiliteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disponibilite
        fields = ['id', 'day', 'start_time', 'end_time']

class NiveauEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = NiveauEducation
        fields = ['id', 'level']

class UtilisateurSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Utilisateur, qui étend AbstractUser.
    """
    
    class Meta:
        model = Utilisateur
        fields = ['id', 'username', 'email', 'first_name', 'last_name','is_mentor','is_mentee','date_joined']

class MentorSerializer(serializers.ModelSerializer):
    """
    Serializer pour l'inscription d'un Mentor.
    """
    # Champs spécifiques au Mentor
    domaines_expertise = DomaineExpertiseSerializer(many=True)
    qualifications = QualificationSerializer(many=True)
    experiences = ExperienceSerializer(many=True)
    preferences = PreferenceSerializer(many=True)
    langues = LangueSerializer(many=True)
    disponibilite = DisponibiliteSerializer(many=True)

    utilisateur = UtilisateurSerializer()
    class Meta:
        model = Mentor
        fields = ['id','utilisateur',  'domaines_expertise', 'qualifications', 'experiences', 'preferences', 'langues', 'disponibilite']

 
    

class MenteeSerializer(serializers.ModelSerializer):
    """
    Serializer pour l'inscription d'un Mentee.
    """
    # Champs spécifiques au Mentee
    centres_interet = DomaineExpertiseSerializer(many=True)
    competences_actuelles = QualificationSerializer(many=True)
    langues = LangueSerializer(many=True)
    disponibilite = DisponibiliteSerializer(many=True)
    niveau_education = NiveauEducationSerializer(many=True)
    objectifs = DomaineExpertiseSerializer(many=True)
    utilisateur = UtilisateurSerializer()
    class Meta:
        model = Mentee
        fields = ['id','utilisateur', 'centres_interet', 'objectifs', 'niveau_education', 'competences_actuelles', 'langues', 'disponibilite']

    
class SessionSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Session.
    Inclut les informations sur le mentor et le mentee associés à la session.
    """
    mentor = MentorSerializer()
    mentee = MenteeSerializer()
    disponibilite = DisponibiliteSerializer()

    class Meta:
        model = Session
        fields = ['id', 'mentor', 'mentee', 'disponibilite', 'type', 'commentaire']

    def create(self, validated_data):
        """
        Méthode pour créer une session de mentorat.
        """
        mentor = Mentor.objects.get(id=validated_data['mentor'])
        mentee = Mentee.objects.get(id=validated_data['mentee'])
        disponibilite = Disponibilite.objects.get(id=validated_data['disponibilite'])
        session = Session.objects.create(mentor=mentor, mentee=mentee, disponibilite=disponibilite, **validated_data)
        return session

    def update(self, instance, validated_data):
        """
        Méthode pour mettre à jour une session de mentorat.
        """
        mentor_data = validated_data.pop('mentor')
        mentee_data = validated_data.pop('mentee')
        instance.mentor = Mentor.objects.get(id=mentor_data['id'])
        instance.mentee = Mentee.objects.get(id=mentee_data['id'])
        instance.date = validated_data.get('date', instance.date)
        instance.heureDebut = validated_data.get('heureDebut', instance.heureDebut)
        instance.heureFin = validated_data.get('heureFin', instance.heureFin)
        instance.type = validated_data.get('type', instance.type)
        instance.save()
        return instance

class RessourceSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Ressource.
    Inclut les informations sur le mentor associé à la ressource.
    """
    mentor = MentorSerializer()
    mentee = MenteeSerializer()
    domaine = DomaineExpertiseSerializer()

    class Meta:
        model = Ressource
        fields = ['id', 'titre', 'type', 'url', 'domaine', 'mentor','mentee']

    def create(self, validated_data):
        """
        Méthode pour créer une ressource.
        """
        mentor_data = validated_data.pop('mentor')
        mentor = Mentor.objects.get(id=mentor_data['id'])
        ressource = Ressource.objects.create(mentor=mentor, **validated_data)
        return ressource

    def update(self, instance, validated_data):
        """
        Méthode pour mettre à jour une ressource.
        """
        mentor_data = validated_data.pop('mentor')
        instance.mentor = Mentor.objects.get(id=mentor_data['id'])
        instance.titre = validated_data.get('titre', instance.titre)
        instance.type = validated_data.get('type', instance.type)
        instance.url = validated_data.get('url', instance.url)
        instance.domaine = validated_data.get('domaine', instance.domaine)
        instance.save()
        return instance

class EvaluationSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle Evaluation.
    Inclut les informations sur le mentor et le mentee associés à l'évaluation.
    """
    mentor = MentorSerializer()
    mentee = MenteeSerializer()

    class Meta:
        model = Evaluation
        fields = ['id', 'mentor', 'mentee', 'note', 'commentaire', 'date']

    def create(self, validated_data):
        """
        Méthode pour créer une évaluation.
        """
        mentor_data = validated_data.pop('mentor')
        mentee_data = validated_data.pop('mentee')
        mentor = Mentor.objects.get(id=mentor_data['id'])
        mentee = Mentee.objects.get(id=mentee_data['id'])
        evaluation = Evaluation.objects.create(mentor=mentor, mentee=mentee, **validated_data)
        return evaluation

    def update(self, instance, validated_data):
        """
        Méthode pour mettre à jour une évaluation.
        """
        mentor_data = validated_data.pop('mentor')
        mentee_data = validated_data.pop('mentee')
        instance.mentor = Mentor.objects.get(id=mentor_data['id'])
        instance.mentee = Mentee.objects.get(id=mentee_data['id'])
        instance.note = validated_data.get('note', instance.note)
        instance.commentaire = validated_data.get('commentaire', instance.commentaire)
        instance.date = validated_data.get('date', instance.date)
        instance.save()
        return instance

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise serializers.ValidationError("Incorrect username or password")
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'")
        
        data['user'] = user
        return data

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer de base pour l'inscription et la mise à jour d'un utilisateur.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Utilisateur
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        user = Utilisateur(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_mentor=validated_data['is_mentor'],
            is_mentee=validated_data['is_mentee']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        """
        Méthode pour mettre à jour un utilisateur existant.
        """
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class MentorRegistrationSerializer(serializers.Serializer):
    """
    Serializer pour l'inscription et la mise à jour d'un Mentor.
    """
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()


    domaines_expertise = serializers.PrimaryKeyRelatedField(many=True, queryset=DomaineExpertise.objects.all())
    qualifications = serializers.PrimaryKeyRelatedField(many=True, queryset=Qualification.objects.all())
    experiences = serializers.PrimaryKeyRelatedField(many=True, queryset=Experience.objects.all())
    preferences = serializers.PrimaryKeyRelatedField(many=True, queryset=Preference.objects.all())
    langues = serializers.PrimaryKeyRelatedField(many=True, queryset=Langue.objects.all())
    disponibilite = serializers.PrimaryKeyRelatedField(many=True, queryset=Disponibilite.objects.all())
    class Meta(UserRegistrationSerializer.Meta):
        fields = ['username','email','password','first_name','last_name','domaines_expertise', 'qualifications', 'experiences', 'preferences', 'langues', 'disponibilite']

    def create(self, validated_data):
        """
        Méthode pour créer un nouvel utilisateur Mentor.
        """
        user_data = {key: validated_data[key] for key in UserRegistrationSerializer.Meta.fields if key in validated_data}
        user_data['is_mentor']=True
        user_data['is_mentee']=False
        user_data['password'] = validated_data['password']
        user = UserRegistrationSerializer().create(user_data)
        mentor= Mentor.objects.create(utilisateur=user)
        mentor.domaines_expertise.set(validated_data['domaines_expertise'])
        mentor.qualifications.set(validated_data['qualifications'])
        mentor.experiences.set(validated_data['experiences'])
        mentor.preferences.set(validated_data['preferences'])
        mentor.langues.set(validated_data['langues'])
        mentor.disponibilite.set(validated_data['disponibilite'])
        
        return {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'domaines_expertise': validated_data['domaines_expertise'],
            'qualifications': validated_data['qualifications'],
            'experiences': validated_data['experiences'],
            'preferences': validated_data['preferences'],
            'langues': validated_data['langues'],
            'disponibilite': validated_data['disponibilite']
        }

    def update(self, instance, validated_data):
        """
        Méthode pour mettre à jour un Mentor existant.
        """
        user_data = {key: validated_data.get(key, getattr(instance.utilisateur, key)) for key in UserRegistrationSerializer.Meta.fields}
        user = UserRegistrationSerializer().update(instance.utilisateur, user_data)
        instance.domaines_expertise = validated_data.get('domaines_expertise', instance._expertise)
        instance.qualifications = validated_data.get('qualifications', instance.qualifications)
        instance.experience = validated_data.get('experience', instance.experience)
        instance.preferences = validated_data.get('preferences', instance.preferences)
        instance.langue = validated_data.get('langue', instance.langue)
        instance.disponibilite = validated_data.get('disponibilite', instance.disponibilite)
        instance.save()

        data = {}
        for key, value in user.__dict__.items():
            data[key] = value
        for key, value in instance.__dict__.items():
            data[key] = value
        return data


class MenteeRegistrationSerializer(serializers.Serializer):
    """
    Serializer pour l'inscription et la mise à jour d'un Mentee.
    """
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    centres_interet = serializers.PrimaryKeyRelatedField(many=True, queryset=DomaineExpertise.objects.all())
    objectifs = serializers.PrimaryKeyRelatedField(many=True, queryset=DomaineExpertise.objects.all())
    niveau_education = serializers.PrimaryKeyRelatedField(many=True, queryset=NiveauEducation.objects.all())
    competences_actuelles = serializers.PrimaryKeyRelatedField(many=True, queryset=Qualification.objects.all())
    langues = serializers.PrimaryKeyRelatedField(many=True, queryset=Langue.objects.all())
    disponibilite = serializers.PrimaryKeyRelatedField(many=True, queryset=Disponibilite.objects.all())

    class Meta:
        fields = ['username','email','password','first_name','last_name','centres_interet', 'objectifs', 'niveau_education', 'competences_actuelles', 'langues', 'disponibilite']

    def create(self, validated_data):
        """
        Méthode pour créer un nouvel utilisateur Mentee.
        """
        user_data = {key: validated_data[key] for key in UserRegistrationSerializer.Meta.fields if key in validated_data}
        user_data['is_mentee']=True
        user_data['is_mentor']=False
        user_data['password'] = validated_data['password']
        user = UserRegistrationSerializer().create(user_data)
        mentee=Mentee.objects.create(utilisateur=user)
        mentee.centres_interet.set(validated_data['centres_interet']),
        mentee.objectifs.set(validated_data['objectifs']),
        mentee.niveau_education.set(validated_data['niveau_education']),
        mentee.competences_actuelles.set(validated_data['competences_actuelles']),
        mentee.langues.set(validated_data['langues']),
        mentee.disponibilite.set(validated_data['disponibilite'])

        matching_service = Matching_service()
        matches = matching_service.match_mentor_to_mentee(mentee)
        mentor = matches["mentor"]
        connexion =Connexion.objects.create(mentor=mentor,mentee=mentee,score=matches["similarity"])
        connexion

        return {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'centres_interet': validated_data['centres_interet'],
                'objectifs': validated_data['objectifs'],
                'niveau_education': validated_data['niveau_education'],
                'competences_actuelles': validated_data['competences_actuelles'],
                'langues': validated_data['langues'],
                'disponibilite': validated_data['disponibilite']
                }

    def update(self, instance, validated_data):
        """
        Méthode pour mettre à jour un Mentee existant.
        """
        user_data = {key: validated_data.get(key, getattr(instance.utilisateur, key)) for key in UserRegistrationSerializer.Meta.fields}
        user = super().update(instance.utilisateur, user_data)
        instance.centresInteret = validated_data.get('centresInteret', instance.centresInteret)
        instance.objectifs = validated_data.get('objectifs', instance.objectifs)
        instance.niveau_education = validated_data.get('niveau_education', instance.niveau_education)
        instance.competences_actuelles = validated_data.get('competences_actuelles', instance.competences_actuelles)
        instance.langue = validated_data.get('langue', instance.langue)
        instance.disponibilite = validated_data.get('disponibilite', instance.disponibilite)
        instance.save()
        return instance
