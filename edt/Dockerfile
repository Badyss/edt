# Utiliser l'image Python officielle
FROM python:3.10

# Définir le répertoire de travail
WORKDIR /app

# Copier tous les fichiers du projet dans le conteneur
COPY . .

# Installer les dépendances du projet
RUN apt-get update && apt-get install -y \
    unzip \
    curl \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Installer les packages Python requis
RUN pip install --no-cache-dir -r requirements.txt

# Définir les variables d'environnement pour Chrome et Selenium
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_BIN=/usr/bin/chromedriver

# Exposer le port 8084
EXPOSE 8084

# Lancer l'application Django sur le port 8084
CMD ["python", "projet/manage.py", "runserver", "0.0.0.0:8084", "--noreload"]
