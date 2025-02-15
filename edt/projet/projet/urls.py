from django.contrib import admin
from django.urls import path, include  # Inclure les URLs de l'application

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app/', include('app.urls'))
]

