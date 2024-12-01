from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('automobiliai/', views.automobiliai, name='automobiliai'),
    path('automobiliai/<int:automobilis_id>', views.automobilis, name='automobilis'),
    path('uzsakymai/', views.UzsakymasView.as_view(), name='uzsakymai'),
    path('uzsakymai/<uuid:pk>', views.UzsakymasDetails.as_view(), name='uzsakymas_detail')
]
