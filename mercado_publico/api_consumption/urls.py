from django.urls import path
from . import views

urlpatterns = [
    path('licitaciones/', views.list_licitaciones, name='list_licitaciones'),
    path('ordenes/', views.list_ordenes, name='list_ordenes'),
    path('licitaciones/<str:codigo>/', views.licitacion_detail, name='licitacion_detail'),
    path('ordenes/<str:codigo>/', views.orden_detail, name='orden_detail'),
    path('proveedor/<str:rut>/', views.buscar_proveedor, name='buscar_proveedor'),
]
