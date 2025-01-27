from django.core.management.base import BaseCommand
from api.models import DomaineExpertise, Qualification, Experience, Preference, Langue, Disponibilite, NiveauEducation
import random
from datetime import time

class Command(BaseCommand):
    help = 'Fill the database with example data'

    def handle(self, *args, **kwargs):
        domaines_expertise = [
            "Machine Learning", "Data Science", "Web Development", "Mobile Development",
            "Cloud Computing", "Cyber Security", "Artificial Intelligence", "Blockchain",
            "Internet of Things", "DevOps", "Network Administration", "Software Testing",
            "Game Development", "Embedded Systems", "Big Data", "IT Support",
            "Virtual Reality", "Augmented Reality", "Natural Language Processing", "Computer Vision"
        ]

        qualifications = [
            "Bachelor of Computer Science", "Master of Computer Science", "PhD in Computer Science", 
            "Bachelor of Software Engineering", "Master of Software Engineering", "Certified Ethical Hacker",
            "Cisco Certified Network Associate", "AWS Certified Solutions Architect", "Google Cloud Professional Data Engineer",
            "Microsoft Certified: Azure Administrator Associate", "Certified Information Systems Security Professional",
            "CompTIA Security+", "Oracle Certified Professional, Java SE 8 Programmer", "Project Management Professional",
            "Scrum Master Certification", "Certified Data Professional", "Certified in the Governance of Enterprise IT",
            "Certified Cloud Security Professional", "Certified Artificial Intelligence Practitioner", "Certified DevOps Engineer"
        ]

        experiences = [
            "1 year experience", "2 years experience", "3 years experience", "4 years experience",
            "5 years experience", "6 years experience", "7 years experience", "8 years experience",
            "9 years experience", "10 years experience", "11 years experience", "12 years experience",
            "13 years experience", "14 years experience", "15 years experience", "16 years experience",
            "17 years experience", "18 years experience", "19 years experience", "20 years experience"
        ]

        preferences = [
            "Morning sessions", "Afternoon sessions", "Evening sessions", "Weekend sessions",
            "Remote sessions", "In-person sessions", "Group sessions", "One-on-one sessions",
            "Project-based learning", "Theory-based learning", "Practical assignments", "Case studies",
            "Workshops", "Seminars", "Hackathons", "Code reviews", "Pair programming", "Mentorship",
            "Career guidance", "Interview preparation"
        ]

        langues = [
            "English", "French", "Spanish", "German", "Chinese", "Japanese", "Russian", "Portuguese", "Arabic", "Hindi"
        ]

        jours = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        disponibilites = []

        for day in jours:
            for i in range(3):
                start_hour = random.randint(8, 18)
                start_time = time(start_hour, 0, 0)
                end_time = time(start_hour + 1, 0, 0)
                disponibilites.append((day, start_time, end_time))

        niveaux_education = [
            "High School Diploma", "Associate Degree", "Bachelor's Degree", "Master's Degree", 
            "Doctorate Degree", "Professional Certification", "Vocational Training", 
            "Postdoctoral Fellowship", "Diploma in Computer Science", "Certificate in IT"
        ]

        # Clear existing data
        DomaineExpertise.objects.all().delete()
        Qualification.objects.all().delete()
        Experience.objects.all().delete()
        Preference.objects.all().delete()
        Langue.objects.all().delete()
        Disponibilite.objects.all().delete()
        NiveauEducation.objects.all().delete()

        # Create new data
        DomaineExpertise.objects.bulk_create([DomaineExpertise(name=name) for name in domaines_expertise])
        Qualification.objects.bulk_create([Qualification(name=name) for name in qualifications])
        Experience.objects.bulk_create([Experience(years=int(name.split()[0])) for name in experiences])
        Preference.objects.bulk_create([Preference(name=name) for name in preferences])
        Langue.objects.bulk_create([Langue(name=name) for name in langues])
        Disponibilite.objects.bulk_create([Disponibilite(day=day, start_time=start_time, end_time=end_time) for day, start_time, end_time in disponibilites])
        NiveauEducation.objects.bulk_create([NiveauEducation(level=level) for level in niveaux_education])

        self.stdout.write(self.style.SUCCESS('Successfully filled the database with example data'))
