from django.contrib import admin
from .models import Team, TeamPokemon, Tag

# Register your models here.
admin.site.register(Team)
admin.site.register(TeamPokemon)
admin.site.register(Tag)
