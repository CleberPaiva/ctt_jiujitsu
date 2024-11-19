from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # Inclui as URLs do app core
    path('accounts/login/', RedirectView.as_view(url='/login/')),  # Redireciona /accounts/login/ para /login/
]
