from django.contrib import admin
from .models import Player, Club, League, Manager, Tournament

class PlayerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'nationality', 'club']

class ClubAdmin(admin.ModelAdmin):
    list_display = ['club_name', 'manager', 'league']

class LeagueAdmin(admin.ModelAdmin):
    list_display = ['league_name', 'country', 'top_scorer']

class ManagerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'nationality']

class TournamentAdmin(admin.ModelAdmin):
    list_display = ['name', 'year', 'final_winner']

# Register your models here.
admin.site.register(Player, PlayerAdmin)
admin.site.register(Club, ClubAdmin)
admin.site.register(League, LeagueAdmin)
admin.site.register(Manager, ManagerAdmin)
admin.site.register(Tournament, TournamentAdmin)