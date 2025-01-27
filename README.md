# Mentor-me
# Plateforme de Mentorat

## Description

La **Plateforme de Mentorat** est une application web qui connecte les mentors et les mentees dans le but de favoriser l'apprentissage et le développement personnel. Elle offre une série de fonctionnalités permettant aux utilisateurs de se connecter, de planifier des sessions de mentorat, d'évaluer leurs progrès, et d'accéder à des ressources d'apprentissage.

### Fonctionnalités

1. **Inscription et Profil :**
   - Les utilisateurs (mentors et mentees) peuvent s'inscrire sur la plateforme et créer un profil détaillé.
   - Les **mentors** peuvent lister leurs domaines d'expertise, leurs qualifications, et leur expérience.
   - Les **mentees** peuvent lister leurs centres d'intérêt, leurs objectifs d'apprentissage, et leurs besoins.

2. **Matching :**
   - Un algorithme de matching connecte les mentors et les mentees en fonction de leurs intérêts et objectifs.
   - Les utilisateurs peuvent également rechercher et choisir des mentors manuellement en fonction de leurs préférences.

3. **Sessions de Mentorat :**
   - Planification des sessions de mentorat en ligne via la plateforme.
   - Types de sessions : discussions individuelles, ateliers de groupe, webinaires, etc.

4. **Ressources d'Apprentissage :**
   - La plateforme propose des ressources d'apprentissage telles que des articles, des vidéos, des cours en ligne, etc.

5. **Suivi et Évaluation :**
   - Les mentees peuvent suivre leurs progrès et évaluer leurs mentors.
   - Les mentors peuvent également donner des feedbacks à leurs mentees pour améliorer la qualité des sessions.

6. **Communauté :**
   - Un espace communautaire permettant aux utilisateurs de partager leurs expériences, poser des questions, et participer à des discussions en ligne.

---

## Technologies Utilisées

- **Backend** : Django (avec djangorestframework et dj-rest-auth pour l'authentification)
- **Frontend** : Angular
- **Base de données** : SQLite
- **Authentification** : JWT pour sécuriser les API
- **Déploiement** : Docker pour conteneuriser l'application

---

## Installation

### Prérequis

Avant de commencer, assurez-vous d'avoir installé Docker et Docker Compose sur votre machine.

- [Docker Installation Guide](https://docs.docker.com/get-docker/)
- [Docker Compose Installation Guide](https://docs.docker.com/compose/install/)

### Étapes pour exécuter l'application

1. Clonez le repository du projet :

   ```bash
   git clone https://votre-repository.git
   cd Mentor-me
   
2. Construisez les conteneurs avec Docker Compose :
	docker-compose up --build
	
3. Exécutez les migrations de la base de données :

	docker-compose run backend python manage.py migrate
	
4. Lancez le projet 
	docker-compose up

5. Accédez à l'application :

    Frontend (Angular) : http://localhost:3000
    Backend (Django API) : http://localhost:8000


Auteurs

    Njikoufon Mfochivé Ousmanou - Développeur principal
    
Licence

Ce projet est sous licence MIT - voir le fichier LICENSE pour plus de détails.


