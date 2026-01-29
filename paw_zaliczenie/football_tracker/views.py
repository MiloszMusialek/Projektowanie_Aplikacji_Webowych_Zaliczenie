from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Player, Club, League, Manager, Tournament

# Widok do wyświetlania strony głównej aplikacji
def home_page_html(request):
    return render(request, 'football_tracker/home_page.html')

# Widok do wyświetlania całej listy piłkarzy
def player_list_html(request):
    players = Player.objects.all()
    return render(request, 'football_tracker/player/list.html', {'players': players})


# Widok do wyświetlania konkretnego piłkarza
def player_details_html(request, id):
    try:
        player = Player.objects.get(id=id)
    except:
        raise Http404("Player doesn't exist in the database")
    return render(request, "football_tracker/player/details.html", {'player': player})


# Widok do wyświetlania całej listy klubów
def club_list_html(request):
    clubs = Club.objects.all()
    return render(request, 'football_tracker/club/list.html', {'clubs': clubs})


# Widok do wyświetlania konkretnego klubu
def club_details_html(request, id):
    try:
        club = Club.objects.get(id=id)
    except:
        raise Http404("Club doesn't exist in the database")
    return render(request, 'football_tracker/club/details.html', {'club': club})


# Widok do wyświetlania całej listy menadzerów
def manager_list_html(request):
    managers = Manager.objects.all()
    return render(request, 'football_tracker/manager/list.html', {'managers': managers})


# Widok do wyświetlania konkretnego managera
def manager_details_html(request, id):
    try:
        manager = Manager.objects.get(id=id)
    except:
        raise Http404("Manager doesn't exist in the database")
    return render(request, 'football_tracker/manager/details.html', {'manager': manager})


# Widok do wyświetlania całej listy lig
def league_list_html(request):
    leagues = League.objects.all()
    return render(request, 'football_tracker/league/list.html', {'leagues': leagues})


# Widok do wyświetlania konkretnej ligi
def league_details_html(request, id):
    try:
        league = League.objects.get(id=id)
    except:
        raise Http404("League doesn't exist in the database")
    return render(request, 'football_tracker/league/details.html', {'league': league})


# Widok do wyświetlania całej listy turniejów
def tournament_list_html(request):
    tournamnets = Tournament.objects.all()
    return render(request, 'football_tracker/tournament/list.html', {'tournaments': tournamnets})


# Widok do wyświetlania konkretnego turnieju
def tournament_details_html(request, id):
    try:
        tournament = Tournament.objects.get(id=id)
    except:
        raise Http404("Tournament doesn't exist in the database.")
    return render(request, 'football_tracker/tournament/details.html', {'tournament': tournament})
