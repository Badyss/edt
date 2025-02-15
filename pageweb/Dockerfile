# Utiliser une image Nginx légère
FROM nginx:alpine

# Supprimer le fichier par défaut Nginx
RUN rm -rf /usr/share/nginx/html/*

# Copier le fichier index.html dans le conteneur
COPY index.html /usr/share/nginx/html/
EXPOSE 8080
CMD ["nginx","-g","daemon off;"]
