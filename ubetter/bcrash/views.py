from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

from .models import TextProcess
from .models import BetRound
from .models import GameProfit
from . import models

from django.http import JsonResponse
from .engine import bet_analyzer
from .engine import betscrap

import pandas as pd
from datetime import datetime
import websockets

lastGameText = ""
# def bcrash(request):
#     obj_instance = None

#     if request.method == 'POST':
#         original = request.POST.get('text')
#         obj_instance = TextProcess.objects.create(original=original)

#     return render(request, "bang.html",{'text': obj_instance})


def bcrash(request):
  if request.method == 'POST':
        bet_text = request.POST.get('text')
        redgreen_text = request.POST.get('redgreen')
        TextProcess.objects.create(original = bet_text, redgreen = redgreen_text)
  mybets = BetRound.objects.all()
  reversed_bets = reversed(mybets)
  template = loader.get_template('bang.html')
  context = {
    'reversed_bets': reversed_bets,
  }
  return HttpResponse(template.render(context, request))

def crash(request):
  # global lastGameText
  # if request.method == 'POST':
  #     bet_text = request.POST.get('text')
  #     if lastGameText != bet_text:    
  #       lastGameText = bet_text
  #       bet_analyzer.inputBetData(bet_text)      
  gameprofits = GameProfit.objects.all()
  reversedprofits = reversed(gameprofits)
  last_site_minus = models.lastSiteMinus
  last_site_plus = models.lastSitePlus
  game_progress = models.gameProgress
  template = loader.get_template('crash.html')
  context = {
    'reversedprofits': reversedprofits,
    'last_site_minus': last_site_minus,
    'last_site_plus': last_site_plus,
    'game_progress': game_progress
  }
  print("new crash!!!!!!!!")
  return HttpResponse(template.render(context, request))

def scrap(request):
  print("dsffffffffffffffffffffffffff")
  betscrap.start()
  gameprofits = GameProfit.objects.all()
  reversedprofits = reversed(gameprofits)
  template = loader.get_template('scrap.html')
  context = {
    'reversedprofits': reversedprofits,
  }
  return HttpResponse(template.render(context, request))


def delete_all_rows(request):
  if request.method == 'POST':
      BetRound.objects.all().delete()
      return JsonResponse({'message': 'All rows deleted successfully.'})
  
  # Add an else block to handle other HTTP methods
  else:
      return JsonResponse({'message': 'Invalid request method.'}, status=400)

def delete_game_rows(request):
  if request.method == 'POST':
      GameProfit.objects.all().delete()
      return JsonResponse({'message': 'All rows deleted successfully.'})
  
  # Add an else block to handle other HTTP methods
  else:
      return JsonResponse({'message': 'Invalid request method.'}, status=400)
  
def save_game_rows(request):
  if request.method == 'POST':
      # Fetch all GameProfit records
      game_profits = GameProfit.objects.all()

      # Convert the queryset to a pandas DataFrame
      data_frame = pd.DataFrame(list(game_profits.values()))
      # Generate a unique filename using the current date and time
      current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
      filename = f"game_profits_{current_datetime}.xlsx"
      # Save DataFrame to Excel file
      data_frame.to_excel(filename, index=False)

      return JsonResponse({'message': 'All rows saved successfully.'})
  
  # Add an else block to handle other HTTP methods
  else:
      return JsonResponse({'message': 'Invalid request method.'}, status=400)
def genie(request):
  if request.method == 'POST':
      models.GameProfit.objects.all().delete()
      betscrap.start()
      # betscrap.test()
      return JsonResponse({'message': 'genie started successfully.'})
  
  # Add an else block to handle other HTTP methods
  else:
      return JsonResponse({'message': 'Invalid request method.'}, status=400)
  
def get_model_data(request):
  data = list(GameProfit.objects.values())
  return JsonResponse(data, safe=False)

def get_last_object(request):
  last_object = GameProfit.objects.last()
  if last_object:
     data = {
        'players_bet': last_object.players_bet,
        'players_loose': last_object.players_loose,
        'players_profit': last_object.players_profit,
        'site_profit': last_object.site_profit,
        'site_peak_valley': last_object.site_peak_valley,
        'site_profit_sigma': last_object.site_profit_sigma,
        'r_players_bet': last_object.r_players_bet,
        'r_players_loose': last_object.r_players_loose,
        'r_players_profit': last_object.r_players_profit,
        'payout': last_object.payout,
        'r_site_profit': last_object.r_site_profit,
        'r_site_peak_valley': last_object.r_site_peak_valley,
        'moon_site_sigma': last_object.moon_site_sigma,
        'r_site_profit_sigma': last_object.r_site_profit_sigma,
     }
     return JsonResponse(data, safe=False)
  else:
     return JsonResponse({}, safe=False) 
   
def get_profit_data(request):
  profit_objects = GameProfit.objects.all()
  data = [{'date': '2023/12/05', 'open': profit_obj.r_site_profit_sigma, 'high': profit_obj.r_site_profit_sigma, 'low': profit_obj.r_site_profit_sigma, 'close': profit_obj.r_site_profit_sigma} for profit_obj in profit_objects]
  return JsonResponse(data, safe=False)

def get_progress_data(request):
   progress_data = models.gameProgress
   data = {
      'progress': progress_data,
   }   
   print(data)
   return JsonResponse(data, safe=False)

