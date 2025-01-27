from api.models import Mentor, Mentee
from api.AHP import AHP
import numpy as np

class Matching_service:
    def __init__(self):
        criteria_matrix = np.array([
        [1, 3, 5, 7, 9, 9],
        [1/3, 1, 3, 5, 7, 9],
        [1/5, 1/3, 1, 3, 5, 7],
        [1/7, 1/5, 1/3, 1, 3, 5],
        [1/9, 1/7, 1/5, 1/3, 1, 3],
        [1/9, 1/9, 1/7, 1/5, 1/3, 1]
    ])

        ahp = AHP(criteria_matrix)
        self.weights = ahp.get_weights()


    def calculate_similarity(self, mentor:Mentor, mentee:Mentee):
        weights = self.weights
        
        similarity = 0.0

        # Exemple de calcul pour chaque critère
        expertise_similarity = len(set(mentor.domaines_expertise.all()).intersection(mentee.centres_interet.all())) / max(len(mentor.domaines_expertise.all()), 1)
        qualification_compatibility = len(set(mentor.qualifications.all()).intersection(mentee.competences_actuelles.all())) / max(len(mentor.qualifications.all()), 1)
        experience_relevance = len(set(mentor.experiences.all()).intersection(mentee.niveau_education.all())) / max(len(mentor.experiences.all()), 1)
        common_language = len(set(mentor.langues.all()).intersection(mentee.langues.all())) / max(len(mentor.langues.all()), 1)
        availability = len(set(mentor.disponibilite.all()).intersection(mentee.disponibilite.all())) / max(len(mentor.disponibilite.all()), 1)
        mentorship_preferences = 1  # Exemple de similitude des préférences (à définir)

        # Calcul de la similarité pondérée
        similarity = (
            weights['expertise_similarity'] * expertise_similarity +
            weights['qualification_compatibility'] * qualification_compatibility +
            weights['experience_relevance'] * experience_relevance +
            weights['common_language'] * common_language +
            weights['availability'] * availability +
            weights['mentorship_preferences'] * mentorship_preferences
        )
        
        return similarity

    def match_mentor_to_mentee(self,mentee:Mentee):
        mentors = Mentor.objects.all()
        matches = {}
        best_match = None
        best_similarity = -1

        for mentor in mentors:
            
            similarity = self.calculate_similarity(mentor, mentee)
            # print(similarity)
            # Trouver le meilleur match pour ce mentee
            if similarity > best_similarity:
                best_similarity = similarity
                best_match = mentor
                matches={
                    'mentor': best_match,
                    'mentee': mentee,
                    'similarity': best_similarity
                }
        return matches