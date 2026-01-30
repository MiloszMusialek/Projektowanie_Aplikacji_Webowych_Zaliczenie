from django.shortcuts import render, redirect
from django.http import Http404
from .models import Player, Club, League, Manager, Tournament
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
# region WIDOKI DLA LOGOWANIA WYLOGOWYWANIA I STRONY GŁÓWNEJ

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

# endregion






# region WIDOKI DLA MODELU PLAYER

# Widok do wyświetlania całej listy piłkarzy
@login_required(login_url='user-login')
def player_list_html(request):
    players = Player.objects.all()

    search_query = request.GET.get('search')
    filter_position = request.GET.get('position')
    filter_foot = request.GET.get('foot')

    if search_query:
        players = players.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )

    if filter_foot:
        players = players.filter(preffered_foot=filter_foot)

    if filter_position:
        players = players.filter(position=filter_position)

    filters = {
        'search_query': search_query,
        'filter_position': filter_position,
        'filter_foot': filter_foot,
    }

    return render(request, 'football_tracker/player/list.html', {'players': players, 'filters': filters})


# Widok do wyświetlania konkretnego piłkarza
@login_required(login_url='user-login')
def player_details_html(request, id):
    try:
        player = Player.objects.get(id=id)
    except:
        raise Http404("Player doesn't exist in the database")
    
    if request.method == "GET":
        return render(request, "football_tracker/player/details.html", {'player': player})
    if request.method == "POST":
        player.delete()
        return redirect('players-list')


# Widok do tworzenia nowego piłkarza
@login_required(login_url='user-login')
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
            if not first_name[0].isupper() or not first_name.isalpha():
                error = "Wrong first name format"
                return render(request, "football_tracker/player/create.html", {'error': error, 'clubs': clubs})
            
            if not last_name[0].isupper() or not last_name.isalpha():
                error = "Wrong last name format"
                return render(request, "football_tracker/player/create.html", {'error': error, 'clubs': clubs})
            
            if len(nationality) != 3 or not nationality.isupper() or not nationality.isalpha():
                error = "Wrong nationality format"
                return render(request, "football_tracker/player/create.html", {'error': error, 'clubs': clubs})

            if int(height) > 210 or int(height) < 150:
                error = "Wrong height value"
                return render(request, "football_tracker/player/create.html", {'error': error, 'clubs': clubs})            

            try:
                club_obj = Club.objects.get(id=club_id)
            except Club.DoesNotExist:
                error = "The Club doesn't exist"
                return render(request, "football_tracker/player/create.html", {'error': error, 'clubs': clubs})
            
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
        

# Widok do aktualizowania piłkarza
@login_required(login_url='user-login')
def player_update_html(request, id):
    clubs = Club.objects.all()

    try:
        player = Player.objects.get(id=id)
    except:
        raise Http404("Player doesn't exist in the database")
    
    if request.method == "GET":
        return render(request, "football_tracker/player/update.html", {'player': player, 'clubs': clubs})
    
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
            if not first_name[0].isupper() or not first_name.isalpha():
                error = "Wrong first name format"
                return render(request, "football_tracker/player/update.html", {'error': error, 'player': player, 'clubs': clubs})
            
            if not last_name[0].isupper() or not last_name.isalpha():
                error = "Wrong last name format"
                return render(request, "football_tracker/player/update.html", {'error': error, 'player': player, 'clubs': clubs})
            
            if len(nationality) != 3 or not nationality.isupper() or not nationality.isalpha():
                error = "Wrong nationality format"
                return render(request, "football_tracker/player/update.html", {'error': error, 'player': player, 'clubs': clubs})

            if int(height) > 210 or int(height) < 150:
                error = "Wrong height value"
                return render(request, "football_tracker/player/update.html", {'error': error, 'player': player, 'clubs': clubs})
            
            try:
                club_obj = Club.objects.get(id=club_id)
            except Club.DoesNotExist:
                error = "The Club doesn't exist"
                return render(request, "football_tracker/player/update.html", {'error': error, 'player': player, 'clubs': clubs})            

            player.first_name = first_name
            player.last_name = last_name
            player.birth_date = birth_date
            player.nationality = nationality
            player.preffered_foot = preffered_foot
            player.height = height
            player.position = position
            player.club = club_obj

            player.save()
            return redirect('player-details', id=player.id)
        
        else:
            error = "All fields are required to update a player"
            return render(request, "football_tracker/player/update.html", {'error': error, 'player': player, 'clubs': clubs})
        
# endregion






# region WIDOKI DLA MODELU CLUB

# Widok do wyświetlania całej listy klubów
@login_required(login_url='user-login')
def club_list_html(request):
    clubs = Club.objects.all()
    leagues = League.objects.all()

    search_query = request.GET.get('search')
    filter_league = request.GET.get('league')

    if search_query:
        clubs = clubs.filter(club_name__icontains=search_query)
    if filter_league:
        clubs = clubs.filter(league_id = filter_league)

    filters={
        'search_query': search_query,
        'filter_league': filter_league,
    }

    return render(request, 'football_tracker/club/list.html', {'clubs': clubs, 'leagues': leagues, 'filters': filters})


# Widok do wyświetlania konkretnego klubu
@login_required(login_url='user-login')
def club_details_html(request, id):
    try:
        club = Club.objects.get(id=id)
    except:
        raise Http404("Club doesn't exist in the database")
    
    if request.method == "GET":
        club_players = club.players.all()
        return render(request, 'football_tracker/club/details.html', {'club': club, 'club_players': club_players})
    if request.method == "POST":
        club.delete()
        return redirect('club-list')


# Widok do tworzenia nowego klubu
@login_required(login_url='user-login')
def club_create_html(request):
    leagues = League.objects.all()
    managers = Manager.objects.all()

    if request.method == "GET":
        return render(request, "football_tracker/club/create.html", {'leagues': leagues, 'managers': managers})
    
    elif request.method == "POST":
        club_name = request.POST.get('club_name')
        foundation_year = request.POST.get('foundation_year')
        stadium = request.POST.get('stadium')
        manager_id = request.POST.get('manager')
        league_id = request.POST.get('league')

        if club_name and foundation_year and stadium and manager_id and league_id:
            if not club_name[0].isupper():
                error = "Incorrect name format"
                return render(request, "football_tracker/club/create.html", {'error': error, 'leagues': leagues, 'managers': managers})

            if int(foundation_year) < 1857 or int(foundation_year) > timezone.now().year:
                error = "Incorrect foundation year"
                return render(request, "football_tracker/club/create.html", {'error': error, 'leagues': leagues, 'managers': managers})
            
            if not stadium[0].isupper() or len(stadium) < 3:
                error = "Incorrect stadium name"
                return render(request, "football_tracker/club/create.html", {'error': error, 'leagues': leagues, 'managers': managers})


            try:
                manager_obj = Manager.objects.get(id=manager_id)
            except Manager.DoesNotExist:
                error = "Manager doesn't exist"
                return render(request, "football_tracker/club/create.html", {'error': error, 'leagues': leagues, 'managers': managers})
            try:
                league_obj = League.objects.get(id=league_id)
            except League.DoesNotExist:
                error = "League doesn't exist"
                return render(request, "football_tracker/club/create.html", {'error': error, 'leagues': leagues, 'managers': managers})
            
            Club.objects.create(
                club_name = club_name,
                foundation_year = foundation_year,
                stadium = stadium,
                manager = manager_obj,
                league = league_obj
            )
            return redirect('club-list')
        else:
            error = "All fields are required to create a new club"
            return render(request, "football_tracker/club/create.html", {'error': error, 'leagues': leagues, 'managers': managers})
        

@login_required(login_url='user-login')
def club_update_html(request, id):
    managers = Manager.objects.all()
    leagues = League.objects.all()

    try:
        club = Club.objects.get(id=id)
    except:
        raise Http404("Club doesn't exist in the database")
    
    if request.method == "GET":
        return render(request, "football_tracker/club/update.html", {'club': club, 'managers': managers, 'leagues': leagues})
    
    elif request.method == "POST":
        club_name = request.POST.get('club_name')
        foundation_year = request.POST.get('foundation_year')
        stadium = request.POST.get('stadium')
        manager_id = request.POST.get('manager')
        league_id = request.POST.get('league')

        if club_name and foundation_year and stadium and manager_id and league_id:
            if not club_name[0].isupper():
                error = "Incorrect name format"
                return render(request, "football_tracker/club/update.html", {'error': error, 'club': club, 'leagues': leagues, 'managers': managers})

            if int(foundation_year) < 1857 or int(foundation_year) > timezone.now().year:
                error = "Incorrect foundation year"
                return render(request, "football_tracker/club/update.html", {'error': error, 'club': club, 'leagues': leagues, 'managers': managers})
            
            if not stadium[0].isupper() or len(stadium) < 3:
                error = "Incorrect stadium name"
                return render(request, "football_tracker/club/update.html", {'error': error, 'club': club, 'leagues': leagues, 'managers': managers})
            

            try:
                manager_obj = Manager.objects.get(id=manager_id)
            except Manager.DoesNotExist:
                error = "Manager doesn't exist"
                return render(request, "football_tracker/club/update.html", {'error': error, 'club': club, 'leagues': leagues, 'managers': managers})
            try:
                league_obj = League.objects.get(id=league_id)
            except League.DoesNotExist:
                error = "League doesn't exist"
                return render(request, "football_tracker/club/update.html", {'error': error, 'club': club, 'leagues': leagues, 'managers': managers})
            
            club.club_name = club_name
            club.foundation_year = foundation_year
            club.stadium = stadium
            club.manager = manager_obj
            club.league = league_obj

            club.save()
            return redirect('club-details', id=club.id)
        else:
            error = "All fields are required to update the club"
            return render(request, "football_tracker/club/update.html", {'error': error, 'club': club, 'leagues': leagues, 'managers': managers})
        
# endregion






# region WIDOKI DLA MODELU MANAGER

# Widok do wyświetlania całej listy menadzerów
@login_required(login_url='user-login')
def manager_list_html(request):
    managers = Manager.objects.all()

    search_query = request.GET.get('search')
    if search_query:
        managers = managers.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )
    
    return render(request, 'football_tracker/manager/list.html', {'managers': managers, 'search_query': search_query})


# Widok do wyświetlania konkretnego managera
@login_required(login_url='user-login')
def manager_details_html(request, id):
    try:
        manager = Manager.objects.get(id=id)
    except:
        raise Http404("Manager doesn't exist in the database")
    
    if request.method == "GET":
        return render(request, 'football_tracker/manager/details.html', {'manager': manager})
    if request.method == "POST":
        manager.delete()
        return redirect('manager-list')


# Widok do tworzenia nowego menadzera
@login_required(login_url='user-login')
def manager_create_html(request):
    if request.method == "GET":
        return render(request, "football_tracker/manager/create.html")
    elif request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        birth_date = request.POST.get('birth_date')
        nationality = request.POST.get('nationality')

        if first_name and last_name and birth_date and nationality:
            if not first_name[0].isupper() or not first_name.isalpha():
                error = "Wrong first name format"
                return render(request, "football_tracker/manager/create.html", {'error': error})
            
            if not last_name[0].isupper() or not last_name.isalpha():
                error = "Wrong last name format"
                return render(request, "football_tracker/manager/create.html", {'error': error})
            
            if len(nationality) != 3 or not nationality.isupper() or not nationality.isalpha():
                error = "Wrong nationality format"
                return render(request, "football_tracker/manager/create.html", {'error': error})

            Manager.objects.create(
                first_name = first_name,
                last_name = last_name,
                birth_date = birth_date,
                nationality = nationality,
            )
            return redirect('manager-list')
        else:
            error = "All fields are required to create a new manager"
            return render(request, "football_tracker/manager/create.html", {'error': error})
        

# Widok do aktualizowania menadzera
@login_required(login_url='user-login')
def manager_update_html(request, id):
    try:
        manager = Manager.objects.get(id=id)
    except:
        raise Http404("Manager doesn't exist in the database")

    if request.method == "GET":
        return render(request, "football_tracker/manager/update.html", {'manager': manager})
    elif request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        birth_date = request.POST.get('birth_date')
        nationality = request.POST.get('nationality')

        if first_name and last_name and birth_date and nationality:
            if not first_name[0].isupper() or not first_name.isalpha():
                error = "Wrong first name format"
                return render(request, "football_tracker/manager/update.html", {'error': error, 'manager': manager})
            
            if not last_name[0].isupper() or not last_name.isalpha():
                error = "Wrong last name format"
                return render(request, "football_tracker/manager/update.html", {'error': error, 'manager': manager})
            
            if len(nationality) != 3 or not nationality.isupper() or not nationality.isalpha():
                error = "Wrong nationality format"
                return render(request, "football_tracker/manager/update.html", {'error': error, 'manager': manager})
            
            manager.first_name = first_name
            manager.last_name = last_name
            manager.birth_date = birth_date
            manager.nationality = nationality

            manager.save()
            return redirect('manager-details', id=manager.id)
        
        else:
            error = "All fields are required to update the manager"
            return render(request, "football_tracker/manager/update.html", {'error': error, 'manager': manager})

# endregion






# region WIDOKI DLA MODELU LEAGUE

# Widok do wyświetlania całej listy lig
@login_required(login_url='user-login')
def league_list_html(request):
    leagues = League.objects.all()

    search_query = request.GET.get('search')
    if search_query:
        leagues = leagues.filter(league_name__icontains=search_query)

    return render(request, 'football_tracker/league/list.html', {'leagues': leagues, 'search_query': search_query})


# Widok do wyświetlania konkretnej ligi
@login_required(login_url='user-login')
def league_details_html(request, id):
    try:
        league = League.objects.get(id=id)
    except:
        raise Http404("League doesn't exist in the database")
    
    if request.method == "GET":
        clubs = league.clubs.all()
        return render(request, 'football_tracker/league/details.html', {'league': league, 'clubs': clubs})
    if request.method == "POST":
        league.delete()
        return redirect('league-list')


# Widok do dodawania nowej ligi
@login_required(login_url='user-login')
def league_create_html(request):
    players = Player.objects.all()

    if request.method == "GET":
        return render(request, "football_tracker/league/create.html", {'players': players})
    
    elif request.method == "POST":
        league_name = request.POST.get('league_name')
        country = request.POST.get('country')
        founding_year = request.POST.get('founding_year')
        top_scorer_id = request.POST.get('top_scorer')

        if league_name and country and founding_year and top_scorer_id:
            if not league_name[0].is_upper() or len(league_name) < 3:
                error = "Incorrect name format"
                return render(request, "football_tracker/league/create.html", {'error': error, 'players': players})
            
            if not country.isupper() or len(country) != 3:
                error = "Incorrect country format"
                return render(request, "football_tracker/league/create.html", {'error': error, 'players': players})
            
            if int(founding_year) < 1850 or int(founding_year) > timezone.now().year:
                error = "Incorrect founding year"
                return render(request, "football_tracker/league/create.html", {'error': error, 'players': players})
            

            try:
                top_scorer_obj = Player.objects.get(id=top_scorer_id)
            except Player.DoesNotExist:
                error = "Player doesn't exist"
                return render(request, "football_tracker/league/create.html", {'error': error, 'players': players})
            
            League.objects.create(
                league_name = league_name,
                country = country,
                founding_year = founding_year,
                top_scorer = top_scorer_obj
            )
            return redirect('league-list')

        else:
            error="All fields are needed to create a new league"
            return render(request, "football_tracker/league/create.html", {'error': error, 'players': players})


# Widok do aktualizowania wybranej ligi
@login_required(login_url='user-login')
def league_update_html(request, id):
    players = Player.objects.all()

    try:
        league = League.objects.get(id=id)
    except League.DoesNotExist:
        raise Http404("League doesn't exist in the database")
    
    if request.method == "GET":
        return render(request, "football_tracker/league/update.html", {'players': players, 'league': league})
    
    elif request.method == "POST":
        league_name = request.POST.get('league_name')
        country = request.POST.get('country')
        founding_year = request.POST.get('founding_year')
        top_scorer_id = request.POST.get('top_scorer')

        if league_name and country and founding_year and top_scorer_id:
            if not league_name[0].is_upper() or len(league_name) < 3:
                error = "Incorrect name format"
                return render(request, "football_tracker/league/update.html", {'error': error, 'players': players, 'league': league})
            
            if not country.isupper() or len(country) != 3:
                error = "Incorrect country format"
                return render(request, "football_tracker/league/update.html", {'error': error, 'players': players, 'league': league})
            
            if int(founding_year) < 1850 or int(founding_year) > timezone.now().year:
                error = "Incorrect founding year"
                return render(request, "football_tracker/league/update.html", {'error': error, 'players': players, 'league': league})
            

            try:
                top_scorer_obj = Player.objects.get(id=top_scorer_id)
            except Player.DoesNotExist:
                error = "Player doesn't exist"
                return render(request, "football_tracker/league/update.html", {'error': error, 'players': players, 'league': league})
            
            league.league_name = league_name
            league.country = country
            league.founding_year = founding_year
            league.top_scorer = top_scorer_obj

            league.save()
            return redirect('league-details', id = league.id)
        else:
            error = "All values are needed to update the league"
            return render(request, "football_tracker/league/update.html", {'error': error, 'players': players, 'league': league})

# endregion






# region WIDOKI DLA MODELU TOURNAMENT

# Widok do wyświetlania całej listy turniejów
@login_required(login_url='user-login')
def tournament_list_html(request):
    tournamnets = Tournament.objects.all()

    search_query = request.GET.get('search')
    if search_query:
        tournaments = tournaments.filter(name__icontains=search_query)

    return render(request, 'football_tracker/tournament/list.html', {'tournaments': tournamnets, 'search_query': search_query})


# Widok do wyświetlania konkretnego turnieju
@login_required(login_url='user-login')
def tournament_details_html(request, id):
    try:
        tournament = Tournament.objects.get(id=id)
    except:
        raise Http404("Tournament doesn't exist in the database.")
    
    if request.method == "GET":
        return render(request, 'football_tracker/tournament/details.html', {'tournament': tournament})
    if request.method == "POST":
        tournament.delete()
        return redirect('tournament-list')


# Widok do tworzenia nowego obiektu Tournament
@login_required(login_url='user-login')
def tournament_create_html(request):
    players = Player.objects.all()
    clubs = Club.objects.all()

    if request.method == "GET":
        return render(request, "football_tracker/tournament/create.html", {'players': players, 'clubs': clubs})
    elif request.method == "POST":
        name = request.POST.get('name')
        year = request.POST.get('year')
        final_winner_id = request.POST.get('final_winner')
        final_second_place_id = request.POST.get('final_second_place')
        man_of_the_match_id = request.POST.get('man_of_the_match')
        winner_score = request.POST.get('winner_score')
        second_place_score = request.POST.get('second_place_score')
        city = request.POST.get('city')
        venue = request.POST.get('venue')

        if name and year and final_winner_id and final_second_place_id and man_of_the_match_id and winner_score and second_place_score and city and venue:
            if not name[0].isupper() or len(name) < 5:
                error = "Incorrect name format"
                return render(request, "football_tracker/tournament/create.html", {'error': error, 'players': players, 'clubs': clubs})
            if int(year) < 1850 or int(year) > timezone.now().year:
                error = "Incorrect year format"
                return render(request, "football_tracker/tournament/create.html", {'error': error, 'players': players, 'clubs': clubs})
            if int(winner_score) < 0 or int(winner_score) > 10:
                error = "Incorrect winner score"
                return render(request, "football_tracker/tournament/create.html", {'error': error, 'players': players, 'clubs': clubs})
            if int(winner_score) < int(second_place_score):
                error = "Winner score must be equal or higher than the second place score"
                return render(request, "football_tracker/tournament/create.html", {'error': error, 'players': players, 'clubs': clubs})
            if int(second_place_score) < 0 or int(second_place_score) > 10:
                error = "Incorrect second place score"
                return render(request, "football_tracker/tournament/create.html", {'error': error, 'players': players, 'clubs': clubs})
            if not city[0].isupper() or not city.isalpha():
                error = "Incorrect city format"
                return render(request, "football_tracker/tournament/create.html", {'error': error, 'players': players, 'clubs': clubs})
            if not venue[0].isupper() or len(venue) < 2:
                error = "Incorrect venue format"
                return render(request, "football_tracker/tournament/create.html", {'error': error, 'players': players, 'clubs': clubs})


            try:
                final_winner_obj = Club.objects.get(id=final_winner_id)
            except:
                error = "The club that won the tournament doesn't exist in the database"
                return render(request, "football_tracker/tournament/create.html", {'error': error, 'players': players, 'clubs': clubs})
            try:
                final_second_place_obj = Club.objects.get(id=final_second_place_id)
            except:
                error = "The club that lost the finale of the tournament doesn't exist in the database"
                return render(request, "football_tracker/tournament/create.html", {'error': error, 'players': players, 'clubs': clubs})
            try:
                man_of_the_match_obj = Player.objects.get(id=man_of_the_match_id)
            except:
                error = "The given man of the match doesn't exist in the database"
                return render(request, "football_tracker/tournament/create.html", {'error': error, 'players': players, 'clubs': clubs}) 
            
            Tournament.objects.create(
                name = name,
                year = year,
                final_winner = final_winner_obj,
                final_second_place = final_second_place_obj,
                man_of_the_match = man_of_the_match_obj,
                winner_score = winner_score,
                second_place_score = second_place_score,
                city = city, 
                venue = venue,
            )
            return redirect('tournament-list')
        else:
            error = "All fields are required to create a new tournament"
            return render(request, "football_tracker/tournament/create.html", {'error': error, 'players': players, 'clubs': clubs})

# Widok do aktualizowania danego obiektu Tournament
@login_required(login_url='user-login')
def tournament_update_html(request, id):
    players = Player.objects.all()
    clubs = Club.objects.all()

    try:
        tournament = Tournament.objects.get(id=id)
    except Tournament.DoesNotExist:
        raise Http404("Tournament doesn't exist in the database")
    
    if request.method == "GET":
        return render(request, "football_tracker/tournament/update.html", {'players': players, 'clubs': clubs, 'tournament': tournament})
    
    elif request.method == "POST":
        name = request.POST.get('name')
        year = request.POST.get('year')
        final_winner_id = request.POST.get('final_winner')
        final_second_place_id = request.POST.get('final_second_place')
        man_of_the_match_id = request.POST.get('man_of_the_match')
        winner_score = request.POST.get('winner_score')
        second_place_score = request.POST.get('second_place_score')
        city = request.POST.get('city')
        venue = request.POST.get('venue')

        if name and year and final_winner_id and final_second_place_id and man_of_the_match_id and winner_score and second_place_score and city and venue:
            if not name[0].isupper() or len(name) < 5:
                error = "Incorrect name format"
                return render(request, "football_tracker/tournament/update.html", {'error': error, 'players': players, 'clubs': clubs, 'tournament': tournament})
            if int(year) < 1850 or int(year) > timezone.now().year:
                error = "Incorrect year format"
                return render(request, "football_tracker/tournament/update.html", {'error': error, 'players': players, 'clubs': clubs, 'tournament': tournament})
            if int(winner_score) < 0 or int(winner_score) > 10:
                error = "Incorrect winner score"
                return render(request, "football_tracker/tournament/update.html", {'error': error, 'players': players, 'clubs': clubs, 'tournament': tournament})
            if int(winner_score) < int(second_place_score):
                error = "Winner score must be equal or higher than the second place score"
                return render(request, "football_tracker/tournament/update.html", {'error': error, 'players': players, 'clubs': clubs, 'tournament': tournament})
            if int(second_place_score) < 0 or int(second_place_score) > 10:
                error = "Incorrect second place score"
                return render(request, "football_tracker/tournament/update.html", {'error': error, 'players': players, 'clubs': clubs, 'tournament': tournament})
            if not city[0].isupper() or not city.isalpha():
                error = "Incorrect city format"
                return render(request, "football_tracker/tournament/update.html", {'error': error, 'players': players, 'clubs': clubs, 'tournament': tournament})
            if not venue[0].isupper() or len(venue) < 2:
                error = "Incorrect venue format"
                return render(request, "football_tracker/tournament/update.html", {'error': error, 'players': players, 'clubs': clubs, 'tournament': tournament})

            try:
                final_winner_obj = Club.objects.get(id=final_winner_id)
            except:
                error = "The club that won the tournament doesn't exist in the database"
                return render(request, "football_tracker/tournament/update.html", {'error': error, 'players': players, 'clubs': clubs, 'tournament': tournament})
            try:
                final_second_place_obj = Club.objects.get(id=final_second_place_id)
            except:
                error = "The club that lost the finale of the tournament doesn't exist in the database"
                return render(request, "football_tracker/tournament/update.html", {'error': error, 'players': players, 'clubs': clubs, 'tournament': tournament})
            try:
                man_of_the_match_obj = Player.objects.get(id=man_of_the_match_id)
            except:
                error = "The given man of the match doesn't exist in the database"
                return render(request, "football_tracker/tournament/update.html", {'error': error, 'players': players, 'clubs': clubs, 'tournament': tournament})  
            
            tournament.name = name
            tournament.year = year
            tournament.final_winner = final_winner_obj
            tournament.final_second_place = final_second_place_obj
            tournament.man_of_the_match = man_of_the_match_obj
            tournament.winner_score = winner_score
            tournament.second_place_score = second_place_score
            tournament.city = city
            tournament.venue = venue

            tournament.save()
            return redirect('tournament-details', id=tournament.id)
        else:
            error="All fields are required to update the tournament"
            return render(request, "football_tracker/tournament/update.html", {'error': error, 'players': players, 'clubs': clubs, 'tournament': tournament})

# endregion
