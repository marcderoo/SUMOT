# Utiliser une image Python officielle comme base
FROM python:3.13.0

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier tous les fichiers du projet
COPY . .

# Installer les dépendances
RUN pip install --no-cache-dir -r /app/requirements.txt

# Exposer le port de l'application Flask
EXPOSE 5000

# Démarrer l'application (chemin correct)
CMD ["python", "/tests/start_app.py"]
