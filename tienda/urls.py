from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('bicicletas/', views.bicicletas, name='bicicletas'),
    path('arriendoBicicletas/', views.arriendoBicicletas, name='arriendoBicicletas'),
    path('contacto/', views.contacto, name='contacto'),
    path('sobrenosotros/', views.sobrenosotros, name='sobrenosotros'),
    path('historial_arriendos/', views.historial_arriendos, name='historial_arriendos'),
    path('agregar_al_carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('limpiar_carrito/', views.limpiar_carrito, name='limpiar_carrito'),
    path('login/', LoginView.as_view(template_name='tienda/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('registro/', views.registro, name='registro'),
    path('bicicletas/<int:bicicleta_id>/', views.Bicicleta, name='bicicleta'),
    path('arriendo/', views.Arriendo, name='arriendo'),
    path('arriendoBicicletas/<int:bicicleta_id>/', views.arriendoBicicletas, name='arriendoBicicletas'),
    path('reparaciones/', views.reparaciones, name='reparaciones'),  
]
