from django.core.management.base import BaseCommand
from api.models import Utilisateur, Mentor, Mentee, DomaineExpertise, Qualification, Experience, Preference, Langue, Disponibilite, NiveauEducation
import random
from django.utils.crypto import get_random_string
from datetime import time

class Command(BaseCommand):
    help = 'Fill the database with example mentors and mentees'

    def handle(self, *args, **kwargs):
        # Assume you already have sample data generated or imported

        # Example data
        domaines_expertise = DomaineExpertise.objects.all()
        qualifications = Qualification.objects.all()
        experiences = Experience.objects.all()
        preferences = Preference.objects.all()
        langues = Langue.objects.all()
        niveaux_education = NiveauEducation.objects.all()
        disponibilites = Disponibilite.objects.all()
        
        # Create Mentors
        for _ in range(100):
            username = get_random_string(10)
            # Replace with your logic to create mentors using existing sample data
            mentor = Mentor.objects.create(
                utilisateur=Utilisateur.objects.create(
                    username=f"Mentor{username}",
                    email=f"{username}@example.com",
                    password='motdepassementor',
                    first_name=f'{username} Mentor',
                    last_name=f'{username} User',
                    is_mentor=True
                ))
            mentor.domaines_expertise.set(random.sample(list(domaines_expertise), k=3))
            mentor.qualifications.set(random.sample(list(qualifications), k=2))
            chosen_experience = random.choice(list(experiences))
            mentor.experiences.set([chosen_experience])
            mentor.preferences.set(random.sample(list(preferences), k=3))
            mentor.langues.set(random.sample(list(langues), k=2))
            mentor.disponibilite.set(random.sample(list(disponibilites), k=3))

        # Create Mentees
        # for _ in range(30):
        #     # Replace with your logic to create mentees using existing sample data
        #     username = get_random_string(10)
        #     mentee = Mentee.objects.create(
        #         utilisateur=Utilisateur.objects.create(
        #             username=f"Mentee{username}",
        #             email=f"{username}@example.com",
        #             password='motdepassementee',
        #             first_name=f'{username} Mentee',
        #             last_name=f'{username} User',
        #             is_mentee=True
        #         ))
        #     mentee.centres_interet.set(random.sample(list(domaines_expertise), k=3))
        #     mentee.objectifs.set(random.sample(list(domaines_expertise), k=2))
        #     chosen_niveau_eduction = random.choice(list(niveaux_education))
        #     mentee.niveau_education.set([chosen_niveau_eduction])
        #     mentee.competences_actuelles.set(random.sample(list(qualifications), k=3))
        #     mentee.langues.set(random.sample(list(langues), k=2))
        #     mentee.disponibilite.set(random.sample(list(disponibilites), k=3))

        self.stdout.write(self.style.SUCCESS('Successfully filled the database with example mentors and mentees'))
