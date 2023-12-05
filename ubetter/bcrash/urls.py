from django.urls import path

from . import views

urlpatterns = [
    path('genie/', views.genie, name='genie'),
    path('scrap/', views.scrap, name='scrap'),
    path('crash/', views.crash, name='crash'),
    path('bcrash/', views.bcrash, name='bcrash'),
    path('delete-all-rows/', views.delete_all_rows, name='delete_all_rows'),
    path('delete-game-rows/', views.delete_game_rows, name='delete_game_rows'),
    path('save-game-rows/', views.save_game_rows, name='save_game_rows'),
    path('refresh-page/', views.refresh_page, name='refresh_page'),
    path('api/get_model_data/', views.get_model_data, name='get_model_data'),
    path('api/get_last_object/', views.get_last_object, name='get_last_object'),
]