from django.contrib import admin

from games.models import Game, Genre

# Register your models here.
@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre')
    list_filter = ('genre',)
    search_fields = ('title', 'description')


admin.site.register(Genre)