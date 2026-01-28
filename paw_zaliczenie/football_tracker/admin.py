from django.contrib import admin
from .models import Player, Club, League, Manager, Tournament

# Register your models here.
admin.site.register(Player)
admin.site.register(Club)
admin.site.register(League)
admin.site.register(Manager)
admin.site.register(Tournament)