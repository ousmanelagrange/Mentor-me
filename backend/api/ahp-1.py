import numpy as np


class Utilisateur:
    def __init__(self, id, nom, email, langues, disponibilite):
        self.id = id
        self.nom = nom
        self.email = email
        self.langues = langues
        self.disponibilite = disponibilite

class Mentor(Utilisateur):
    def __init__(self, id, nom, email, langues, disponibilite, domaines_expertise, qualifications, experience, preferences):
        super().__init__(id, nom, email, langues, disponibilite)
        self.domaines_expertise = domaines_expertise
        self.qualifications = qualifications
        self.experience = experience
        self.preferences = preferences

class Mentee(Utilisateur):
    def __init__(self, id, nom, email, langues, disponibilite, centres_interet, objectifs, niveau_education, competences_actuelles):
        super().__init__(id, nom, email, langues, disponibilite)
        self.centres_interet = centres_interet
        self.objectifs = objectifs
        self.niveau_education = niveau_education
        self.competences_actuelles = competences_actuelles

class AHP:
    def __init__(self, criteria):
        self.criteria = criteria
        self.num_criteria = len(criteria)
        self.pairwise_matrix = np.ones((self.num_criteria, self.num_criteria))
        self.normalized_matrix = None
        self.weights = None

    def set_comparison(self, i, j, value):
        self.pairwise_matrix[i, j] = value
        self.pairwise_matrix[j, i] = 1 / value

    def normalize(self):
        column_sums = np.sum(self.pairwise_matrix, axis=0)
        self.normalized_matrix = self.pairwise_matrix / column_sums

    def calculate_weights(self):
        self.normalize()
        self.weights = np.mean(self.normalized_matrix, axis=1)
        return self.weights

    def check_consistency(self):
        if self.weights is None:
            self.calculate_weights()
        weighted_sum = np.dot(self.pairwise_matrix, self.weights)
        consistency_vector = weighted_sum / self.weights
        lambda_max = np.mean(consistency_vector)
        ci = (lambda_max - self.num_criteria) / (self.num_criteria - 1)
        ri_dict = {1: 0, 2: 0, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}
        ri = ri_dict.get(self.num_criteria, 1.49)
        cr = ci / ri
        return cr < 0.1

    def calculate_scores(self, alternatives):
        scores = []
        for alternative in alternatives:
            scores.append(np.dot(self.weights, alternative))
        return scores

class MentorshipPlatform:
    def __init__(self, mentors, mentees, criteria):
        self.mentors = mentors
        self.mentees = mentees
        self.ahp = AHP(criteria)

    def calculate_similarity_matrix(self):
        # Suppose we manually set pairwise comparison values
        self.ahp.set_comparison(0, 1, 3)  # Expertise is moderately more important than Languages
        self.ahp.set_comparison(0, 2, 5)  # Expertise is strongly more important than Objectives
        self.ahp.set_comparison(0, 3, 7)  # Expertise is very strongly more important than Availability
        self.ahp.set_comparison(1, 2, 3)  # Languages is moderately more important than Objectives
        self.ahp.set_comparison(1, 3, 5)  # Languages is strongly more important than Availability
        self.ahp.set_comparison(2, 3, 3)  # Objectives is moderately more important than Availability

    def match(self):
        matches = []
        self.calculate_similarity_matrix()
        if not self.ahp.check_consistency():
            raise ValueError("The pairwise comparison matrix is inconsistent")

        weights = self.ahp.calculate_weights()
        for mentee in self.mentees:
            best_score = -1
            best_mentor = None
            for mentor in self.mentors:
                # Create the alternative vector based on criteria
                alternative = [
                    self.calculate_criteria_score(mentor.domaines_expertise, mentee.centres_interet),
                    self.calculate_criteria_score(mentor.langues, mentee.langues),
                    self.calculate_criteria_score(mentor.domaines_expertise, mentee.objectifs),
                    self.calculate_criteria_score(mentor.disponibilite, mentee.disponibilite)
                ]
                score = np.dot(weights, alternative)
                if score > best_score:
                    best_score = score
                    best_mentor = mentor
            if best_mentor:
                matches.append((mentee, best_mentor))
                self.mentors.remove(best_mentor)
                if best_mentor not in [m for n, m in matches if m == best_mentor]:
                    self.mentors.append(best_mentor)
                elif len([m for n, m in matches if m == best_mentor]) >= 2:
                    self.mentors.remove(best_mentor)
        
        return matches

    def calculate_criteria_score(self, mentor_attr, mentee_attr):
        # Simple matching score, could be more sophisticated
        return len(set(mentor_attr) & set(mentee_attr)) / max(len(set(mentor_attr) | set(mentee_attr)), 1)


# Créer des exemples de mentors et de mentees
mentors = [
    Mentor(1, "John Doe", "john@example.com", ["English", "French"], {}, ["IT", "Management"], ["PhD"], 10, ["Online"]),
    Mentor(2, "Jane Smith", "jane@example.com", ["English"], {}, ["Marketing", "Sales"], ["MBA"], 8, ["In-person"]),
]

mentees = [
    Mentee(1, "Alice Johnson", "alice@example.com", ["English"], {}, ["IT"], ["Learn Python"], "Bachelor", ["Basic IT skills"]),
    Mentee(2, "Bob Brown", "bob@example.com", ["French"], {}, ["Sales"], ["Improve Sales Skills"], "High School", ["Intermediate sales experience"]),
]

# Définir les critères pour l'AHP
criteria = ["Expertise", "Languages", "Objectives", "Availability"]

# Créer une plateforme de mentorat et trouver des appariements
platform = MentorshipPlatform(mentors, mentees, criteria)
matches = platform.match()

# Afficher les appariements
for mentee, mentor in matches:
    print(f"Mentee {mentee.nom} is matched with Mentor {mentor.nom}")
