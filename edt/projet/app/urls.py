from django.contrib import admin
from django.urls import path
from app.views import login_and_fetch_schedule, execute_main_script, logout_view  # Importer les vues depuis votre application

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', login_and_fetch_schedule, name='fetch_schedule'),  # URL pour le formulaire de connexion
    path('execute-script/', execute_main_script, name='execute_script'),  # URL pour exécuter un script spécifique
    path('logout/', logout_view, name='logout'),
]
