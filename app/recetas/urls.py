# recetas/urls.py
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('detalles/<str:nombre_id>', views.detalles, name='detalles'),
    path('update/<str:nombre_id>', views.updateView, name='update'),
    path('delete/<str:nombre_id>', views.deleteView, name='delete'),
    path('add/', views.add, name='add'),
    path('addIng/', views.addIng, name='addIng'),
    path('searchbar/', views.searchbar, name='searchbar'),
    path('toggleMode/', views.toggleMode, name='mode'),  
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
