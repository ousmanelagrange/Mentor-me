# Étape 1 : Build de l'application Angular
FROM node:18-alpine AS build

# Définir le répertoire de travail
WORKDIR /app

# Configurer npm pour optimiser les installations
RUN npm config set fetch-retries 5
RUN npm config set fetch-retry-mintimeout 20000
RUN npm config set fetch-retry-maxtimeout 120000
RUN npm config set registry https://registry.npmjs.org

# Copier les fichiers package.json et package-lock.json
COPY package.json package-lock.json ./

# Installer les dépendances Angular avec un nettoyage du cache npm
RUN npm install --force --legacy-peer-deps && npm cache clean --force

# Copier tout le projet dans l'image
COPY . .

# Construire les fichiers statiques de l'application Angular
RUN npm run build


# Étape 2 : Configuration de Nginx pour servir l'application Angular
FROM nginx:stable-alpine

# Copier les fichiers construits dans le répertoire par défaut de Nginx
COPY --from=build /app/dist/mentor_me /usr/share/nginx/html

# Ajouter une configuration personnalisée pour gérer les routes Angular
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Exposer le port 80 pour le service web
EXPOSE 80

# Démarrer Nginx
CMD ["nginx", "-g", "daemon off;"]
