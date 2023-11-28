from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

from .models import TextProcess
from .models import BetRound
from .models import GameProfit
from . import models

from django.http import JsonResponse
from .engine import bet_analyzer
from .engine import betscrap

import pandas as pd
from datetime import datetime

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
  # print("new crash!!!!!!!!")
  return HttpResponse(template.render(context, request))

def scrap(request):
  print("dsffffffffffffffffffffffffff")
  betscrap.start()
  # gameprofits = GameProfit.objects.all()
  # reversedprofits = reversed(gameprofits)      
  # template = loader.get_template('scrap.html')
  # context = {
  #   'reversedprofits': reversedprofits,
  # }
  # return HttpResponse(template.render(context, request))


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





