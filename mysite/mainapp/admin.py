from django.contrib import admin

from .models import *
# Register your models here.

admin.site.register(Tournament)
admin.site.register(Typesoftour)
admin.site.register(Team)
admin.site.register(Tourteam)
admin.site.register(Player)
admin.site.register(Game)
admin.site.register(PlayerTeam)


