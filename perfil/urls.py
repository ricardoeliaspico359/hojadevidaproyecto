from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('pdf/', views.generar_pdf, name='generar_pdf'),
    path('datos-personales/', views.datos_personales, name='datos_personales'),
    path('experiencia-laboral/', views.experiencia_laboral, name='experiencia_laboral'),
    path('cursos/', views.cursos, name='cursos'),
    path('reconocimientos/', views.reconocimientos, name='reconocimientos'),
    path('productos-academicos/', views.productos_academicos, name='productos_academicos'),
    path('productos-laborales/', views.productos_laborales, name='productos_laborales'),
    path('venta-garage/', views.venta_garage, name='venta_garage'),
    path("dashboard/ocultar/<str:seccion>/", views.ocultar_seccion_dashboard, name="ocultar_seccion_dashboard"),
]
