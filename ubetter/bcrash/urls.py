from django.urls import path

from . import views

urlpatterns = [
    path('scrap/', views.scrap, name='scrap'),
    path('crash/', views.crash, name='crash'),
    path('bcrash/', views.bcrash, name='bcrash'),
    path('delete-all-rows/', views.delete_all_rows, name='delete_all_rows'),
    path('delete-game-rows/', views.delete_game_rows, name='delete_game_rows'),
    path('save-game-rows/', views.save_game_rows, name='save_game_rows'),
]