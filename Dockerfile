# Utiliser une image Python officielle comme base
FROM python:3.13.0

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers nécessaires dans le conteneur
COPY requirements.txt requirements.txt
COPY . .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port de l'application Flask
EXPOSE 5000

# Définir la commande pour démarrer l'application
CMD ["python", "start_app.py"]
