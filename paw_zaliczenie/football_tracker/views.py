from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .models import Player, Club, League, Manager, Tournament
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Widok do wyświetlania panelu logowania
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home-page')
        else:
            return render(request, 'football_tracker/login.html', {'error': 'Nieprawidłowe dane'})
    return render(request, 'football_tracker/login.html')


# Widok do wylogowywania
def user_logout(request):
    logout(request)
    return redirect('user-login')


# Widok do wyświetlania strony głównej aplikacji
@login_required(login_url='user-login')
def home_page_html(request):
    return render(request, 'football_tracker/home_page.html')




"""WIDOKI DLA MODELU PLAYER"""

# Widok do wyświetlania całej listy piłkarzy
@login_required(login_url='user-login')
def player_list_html(request):
    players = Player.objects.all()
    return render(request, 'football_tracker/player/list.html', {'players': players})


# Widok do wyświetlania konkretnego piłkarza
@login_required(login_url='user-login')
def player_details_html(request, id):
    try:
        player = Player.objects.get(id=id)
    except:
        raise Http404("Player doesn't exist in the database")
    return render(request, "football_tracker/player/details.html", {'player': player})


# Widok do tworzenia nowego piłkarza
def player_create_html(request):
    clubs = Club.objects.all()

    if request.method == "GET":
        return render(request, "football_tracker/player/create.html", {'clubs': clubs})
    
    elif request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        birth_date = request.POST.get('birth_date')
        nationality = request.POST.get('nationality')
        preffered_foot = request.POST.get('preffered_foot')
        height = request.POST.get('height')
        position = request.POST.get('position')
        club_id = request.POST.get('club')

        if first_name and last_name and birth_date and nationality and preffered_foot and height and position and club_id:
            try:
                club_obj = Club.objects.get(id=club_id)
            except Club.DoesNotExist:
                error = "The Club doesn't exist"
                return render(request, "football_tracker/player/create.html", {'error': error})
            
            Player.objects.create(
                first_name = first_name,
                last_name = last_name,
                birth_date = birth_date,
                nationality = nationality, 
                preffered_foot = preffered_foot,
                height = height,
                position = position,
                club = club_obj
            )
            return redirect('players-list')
        else:
            error = "All fields are required to create a new player."
            return render(request, "football_tracker/player/create.html", {'error': error, 'clubs': clubs})


"""WIDOKI DLA MODELU CLUB"""

# Widok do wyświetlania całej listy klubów
@login_required(login_url='user-login')
def club_list_html(request):
    clubs = Club.objects.all()
    return render(request, 'football_tracker/club/list.html', {'clubs': clubs})


# Widok do wyświetlania konkretnego klubu
@login_required(login_url='user-login')
def club_details_html(request, id):
    try:
        club = Club.objects.get(id=id)
    except:
        raise Http404("Club doesn't exist in the database")
    
    club_players = club.players.all()
    return render(request, 'football_tracker/club/details.html', {'club': club, 'club_players': club_players})




"""WIDOKI DLA MODELU MANAGER"""

# Widok do wyświetlania całej listy menadzerów
@login_required(login_url='user-login')
def manager_list_html(request):
    managers = Manager.objects.all()
    return render(request, 'football_tracker/manager/list.html', {'managers': managers})


# Widok do wyświetlania konkretnego managera
@login_required(login_url='user-login')
def manager_details_html(request, id):
    try:
        manager = Manager.objects.get(id=id)
    except:
        raise Http404("Manager doesn't exist in the database")
    return render(request, 'football_tracker/manager/details.html', {'manager': manager})




"""WIDOKI DLA MODELU LEAGUE"""

# Widok do wyświetlania całej listy lig
@login_required(login_url='user-login')
def league_list_html(request):
    leagues = League.objects.all()
    return render(request, 'football_tracker/league/list.html', {'leagues': leagues})


# Widok do wyświetlania konkretnej ligi
@login_required(login_url='user-login')
def league_details_html(request, id):
    try:
        league = League.objects.get(id=id)
    except:
        raise Http404("League doesn't exist in the database")
    
    clubs = league.clubs.all()
    return render(request, 'football_tracker/league/details.html', {'league': league, 'clubs': clubs})




"""WIDOKI DLA MODELU TOURNAMENT"""

# Widok do wyświetlania całej listy turniejów
@login_required(login_url='user-login')
def tournament_list_html(request):
    tournamnets = Tournament.objects.all()
    return render(request, 'football_tracker/tournament/list.html', {'tournaments': tournamnets})


# Widok do wyświetlania konkretnego turnieju
@login_required(login_url='user-login')
def tournament_details_html(request, id):
    try:
        tournament = Tournament.objects.get(id=id)
    except:
        raise Http404("Tournament doesn't exist in the database.")
    return render(request, 'football_tracker/tournament/details.html', {'tournament': tournament})
