FROM postgres:15

# Définir les variables d'environnement pour la configuration initiale
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_DB=stripe-example

# Définir le point de montage pour les données persistantes
VOLUME ["/var/lib/postgresql/data"]

# Exposer le port PostgreSQL
EXPOSE 5432

# Commande de démarrage du conteneur
CMD ["postgres"]
