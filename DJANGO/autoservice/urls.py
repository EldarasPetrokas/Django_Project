from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
    path('automobiliai/', views.automobiliu_sarasas, name='automobiliai'),
    path('automobiliai/<int:automobilis_id>', views.automobilis, name='automobilis'),
    path('uzsakymai/', views.UzsakymasListView.as_view(), name='uzsakymai'),
    path('uzsakymai/<uuid:pk>', views.UzsakymasDetails.as_view(), name='uzsakymas_detail'),
    path('search/', views.search, name='search'),
    path('my-orders/', views.UserUzsakymaiView.as_view(), name='my-orders'),
    path('register/', views.register, name='register'),
    path('profilis/', views.profilis, name='profilis'),

]
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]



