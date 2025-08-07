from django.contrib import admin

from commons.models import GameList, Review


# Register your models here.
@admin.register(GameList)
class GameListAdmin(admin.ModelAdmin):
    list_display = ('user', 'game', 'added_at')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'game', 'rating', 'created_at')
