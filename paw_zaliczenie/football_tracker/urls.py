from django.urls import path
from . import views

urlpatterns = [
    # URL dla strony głównej aplikacji
    path('home/', views.home_page_html, name='home-page'),

    # URLs dla logowania i wylogowywania
    path('login/', views.user_login, name='user-login'),
    path('logout/', views.user_logout, name='user-logout'),

    # URLs dla modelu Player
    path('players/', views.player_list_html, name='players-list'),
    path('players/<int:id>/', views.player_details_html, name='player-details'),
    path('players/create/', views.player_create_html, name='player-create'),

    # URLs dla modelu Club
    path('clubs/', views.club_list_html, name='club-list'),
    path('clubs/<int:id>/', views.club_details_html, name='club-details'),

    # URLs dla modelu Manager
    path('managers/', views.manager_list_html, name='manager-list'),
    path('managers/<int:id>/', views.manager_details_html, name='manager-details'),

    # URLs dla modelu League
    path('leagues/', views.league_list_html, name='league-list'),
    path('leagues/<int:id>/', views.league_details_html, name='league-details'),

    # URLs dla modelu Tournament
    path('tournaments/', views.tournament_list_html, name='tournament-list'),
    path('tournaments/<int:id>/', views.tournament_details_html, name='tournament-details'),
]