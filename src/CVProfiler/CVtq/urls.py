from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'CVtq'

urlpatterns = [
    path('', views.index, name='index'),

    path('profiles/', views.ProfilesListView.as_view(), name='profiles'),
    path('firms/', views.FirmsView.as_view(), name='firms'),
    path('account_edit/', views.ProfileDetailEditView.as_view(), name='account_edit'),
    path('account/<pk>/', views.ProfileDetailView.as_view(), name='account'),
    path('account/<pk>/cv/<profile_id>/', views.cvView, name='cv' ),

    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('activate/<uidb64>/<token>/', views.activate_user, name='activate'),
]