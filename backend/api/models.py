from django.db import models
from django.contrib.auth.models import AbstractUser

class DomaineExpertise(models.Model):
    name = models.CharField(max_length=100)

class Qualification(models.Model):
    name = models.CharField(max_length=100)

class Experience(models.Model):
    years = models.IntegerField()

class Preference(models.Model):
    name = models.CharField(max_length=100)

class Langue(models.Model):
    name = models.CharField(max_length=100)

class Disponibilite(models.Model):
    day = models.CharField(max_length=10)  # e.g., 'Monday'
    start_time = models.TimeField()        # e.g., '09:00'
    end_time = models.TimeField()          # e.g., '17:00'

class NiveauEducation(models.Model):
    level = models.CharField(max_length=100)  # e.g., 'Bachelor', 'Master', etc.
class Utilisateur(AbstractUser):
    """
    Ce modèle étend AbstractUser pour inclure des fonctionnalités utilisateur de base.
    Les utilisateurs peuvent s'inscrire et se connecter via des méthodes dédiées.
    """
    is_mentor = models.BooleanField(default=False)
    is_mentee = models.BooleanField(default=False)

class Mentor(models.Model):
    """
    Ce modèle représente un mentor et étend les informations de base de l'utilisateur.
    Il inclut des domaines d'expertise, des qualifications, de l'expérience, des préférences,
    des langues parlées et des disponibilités.
    """
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)  # Référence au modèle Utilisateur
    domaines_expertise = models.ManyToManyField(DomaineExpertise)
    qualifications = models.ManyToManyField(Qualification)
    experiences = models.ManyToManyField(Experience)
    preferences = models.ManyToManyField(Preference)
    langues = models.ManyToManyField(Langue)
    disponibilite = models.ManyToManyField(Disponibilite)

    def proposerSession(self):
        """
        Méthode pour que le mentor propose une session de mentorat.
        """
        pass  # Logique pour proposer une session

    def partagerRessource(self):
        """
        Méthode pour que le mentor partage une ressource.
        """
        pass  # Logique pour partager une ressource

class Mentee(models.Model):
    """
    Ce modèle représente un mentee et étend les informations de base de l'utilisateur.
    Il inclut des centres d'intérêt, des objectifs, le niveau d'éducation, les compétences actuelles,
    les langues parlées et les disponibilités.
    """
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)  # Référence au modèle Utilisateur
    centres_interet = models.ManyToManyField(DomaineExpertise, related_name='centres_interet_mentees')
    objectifs = models.ManyToManyField(DomaineExpertise,related_name='objectifs_mentees')
    niveau_education = models.ManyToManyField(NiveauEducation)
    competences_actuelles = models.ManyToManyField(Qualification)
    langues = models.ManyToManyField(Langue)
    disponibilite = models.ManyToManyField(Disponibilite)

    def rechercherMentor(self):
        """
        Méthode pour que le mentee recherche un mentor.
        """
        pass  # Logique pour rechercher un mentor

    def evaluerMentor(self):
        """
        Méthode pour que le mentee évalue un mentor.
        """
        pass  # Logique pour évaluer un mentor

class Connexion(models.Model):
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)  # Référence au mentor de la session
    mentee = models.ForeignKey(Mentee, on_delete=models.CASCADE)  # Référence au mentee de la session
    score = models.FloatField()
class Session(models.Model):
    """
    Ce modèle représente une session de mentorat entre un mentor et un mentee.
    Il inclut la date, l'heure de début, l'heure de fin et le type de session.
    """
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)  # Référence au mentor de la session
    mentee = models.ForeignKey(Mentee, on_delete=models.CASCADE)  # Référence au mentee de la session
    disponibilite = models.ForeignKey(Disponibilite, on_delete=models.CASCADE)  # Référence au mentee de la session
    type = models.CharField(max_length=255)  # Type de session
    commentaire = models.CharField(max_length=255)

    def planifier(self):
        """
        Méthode pour planifier une session de mentorat.
        """
        pass  # Logique pour planifier une session

    def annuler(self):
        """
        Méthode pour annuler une session de mentorat.
        """
        pass  # Logique pour annuler une session

class Ressource(models.Model):
    """
    Ce modèle représente une ressource partagée par un mentor.
    Il inclut le titre, le type, l'URL et le domaine de la ressource.
    """
    titre = models.CharField(max_length=255)  # Titre de la ressource
    type = models.CharField(max_length=255)  # Type de ressource (article, vidéo, etc.)
    url = models.URLField()  # URL de la ressource
    domaine = models.ForeignKey(DomaineExpertise, on_delete=models.CASCADE, related_name='ressources')  # Domaine de la ressource
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name='ressources')  # Référence au mentor qui partage la ressource
    mentee = models.ForeignKey(Mentee, on_delete=models.CASCADE, related_name='ressources')  # Référence au mentor qui partage la ressource

    def ajouterRessource(self):
        """
        Méthode pour ajouter une ressource.
        """
        pass  # Logique pour ajouter une ressource

    def consulterRessource(self):
        """
        Méthode pour consulter une ressource.
        """
        pass  # Logique pour consulter une ressource

class Evaluation(models.Model):
    """
    Ce modèle représente une évaluation donnée par un mentee à un mentor.
    Il inclut la note, le commentaire et la date de l'évaluation.
    """
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)  # Référence au mentor évalué
    mentee = models.ForeignKey(Mentee, on_delete=models.CASCADE)  # Référence au mentee qui donne l'évaluation
    note = models.IntegerField()  # Note de l'évaluation
    commentaire = models.TextField()  # Commentaire de l'évaluation
    date = models.DateField()  # Date de l'évaluation

    def donnerFeedback(self):
        """
        Méthode pour donner un feedback au mentor.
        """
        pass  # Logique pour donner un feedback

    def consulterFeedback(self):
        """
        Méthode pour consulter un feedback donné.
        """
        pass  # Logique pour consulter un feedback


