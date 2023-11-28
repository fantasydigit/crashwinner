from .. import models
from . import utility
from .. import views
from django.http.request import HttpRequest

# sigma all players bet per round
playersBet = 0.00 
# most won like 10.00x payout per round
payOut = 0.00
# sigma site profit per round
playersProfit = 0.00
# sigma site profit per round
playersLoose = 0.00
# sigma site profit per round
siteProfit = 0.00
#latest continuous site profits 
lastSitePlus = 0.00
#latest continuous site loose
lastSiteMinus = 0.00
lastPeakValley = 0.00
# ###########~~~~~~~~~~~~~~real is real kk
# sigma all players bet per round
r_playersBet = 0.00 
# sigma site profit per round
r_playersProfit = 0.00
# sigma site profit per round
r_playersLoose = 0.00
# sigma site profit per round
r_siteProfit = 0.00
#latest continuous site profits 
r_lastSitePlus = 0.00
# moon sigma
moonSiteSigma = 0.00
#latest continuous site loose
r_lastSiteMinus = 0.00
r_lastPeakValley = 0.00
#last scrapping text
lastScrappingText = ""
#bot
botBetDollar = 1000.00

##### input all players bet data for last round
def inputBetData(text):
    analyzeSiteProfit(text)

##### analyze site profit on the issued round
def analyzeSiteProfit(play_text):
    #.......... players won
    # 1780502935500784944   
    # lVlasrapido
    # 2.00×	
    # +$ 0.07

    # ........ players fail
    # 1780502939443624751
    # Setare77
    # 0.00×	
    # $ 12.81
    global siteProfit, payOut, playersBet, playersProfit, siteSigmaProfit, playersLoose, lastSiteMinus, lastSitePlus, lastPeakValley
    global r_siteProfit, r_playersBet, r_playersProfit, r_siteSigmaProfit, r_playersLoose, r_lastSiteMinus, r_lastSitePlus, r_lastPeakValley, moonSiteSigma
    global botBetDollar
    if validate(play_text) == False:
        return False
    playersBet = 0.00
    payOut = -1.00
    playersLoose = 0.00
    playersProfit = 0.00
    siteProfit = 0.00
    siteSigmaProfit = 0.00
    r_playersBet = 0.00
    r_playersLoose = 0.00
    r_playersProfit = 0.00
    r_siteProfit = 0.00
    r_siteSigmaProfit = 0.00
    
    print("start bet")
    lines = play_text.splitlines()
    for index, current_line in enumerate(lines):
        if len(current_line) == 19 and current_line.isdigit():
            # 1780532030291529775	
            # $ 0.40
            #     09:54:35	1.96×	
            # +$ 0.38
            # avoid the case above since it's ...
            bet_id = current_line
            player_name = lines[index+1]
            payout = lines[index+2]
            player_profit = lines[index+3]
            check_payout = payout.replace('×', '')
            splits = check_payout.split(" ")
            if(len(splits) > 1):
                continue
            # payOut pick up
            payout = payout.replace('×','')
            if utility.is_float_convertible(payout):
                payout_float = float(payout)
                if payOut == -1.00:
                    if payout_float != 1.96 and payout_float != 2.00: # yes avoid for RedBear and GreenBull
                        payOut = payout_float
                        print(f"payOut:{payOut}")
            # playersLoose and playersBet
            if("0.00" in payout): #####...... player failed
                # 1780502939443624751
                # Setare77
                # 0.00×	
                # $ 12.81
                #print(f"yes I am {payout}")
                if "$" in player_profit:
                    # player_profit = player_profit.strip('$\n ')
                    player_profit = player_profit.replace(',', '')
                    player_profit = player_profit.replace('$', '')
                    player_profit = player_profit.replace(' ', '')
                    #print(f"payout: {payout} player_profit: {player_profit}" )  
                    if utility.is_float_convertible(player_profit):
                        player_loose_float = float(player_profit)
                        playersLoose += player_loose_float
                        playersBet += player_loose_float
                        if "Hidden" != player_name or player_loose_float < botBetDollar:
                            r_playersBet += player_loose_float
                            r_playersLoose += player_loose_float
                            
            else: ######...... player won
                if "$" in player_profit:
                    # 1780502935500784944   
                    # lVlasrapido
                    # 2.00×	
                    # +$ 0.07
                    #player_profit = player_profit.strip('+$\n ')
                    player_profit = player_profit.replace(',', '')
                    player_profit = player_profit.replace('+', '')
                    player_profit = player_profit.replace('$', '')
                    player_profit = player_profit.replace(' ', '')
                    #print(f"payout: {payout} player_profit: {player_profit}" )
                    if utility.is_float_convertible(player_profit):
                        player_profit_float = float(player_profit)
                        payout = payout.strip('×\t')
                        if utility.is_float_convertible(payout):
                            payout_float = float(payout)
                            playersProfit += player_profit_float
                            if "Hidden" != player_name or player_profit_float / (payout_float - 1.00) < botBetDollar:
                                r_playersProfit += player_profit_float
                            if(payout_float != 1.00):
                                playersBet += player_profit_float / (payout_float - 1.00)
                                if "Hidden" != player_name or player_profit_float / (payout_float - 1.00) < botBetDollar:
                                    r_playersBet += player_profit_float / (payout_float - 1.00)
                            else:
                                print(f"{player_profit_float}/{payout_float - 1.00}=??")
    #insert GameProfit Model
    siteProfit = playersLoose - playersProfit
    r_siteProfit = r_playersLoose - r_playersProfit
    if payOut < 10.00:
        moonSiteSigma += r_siteProfit
    else:
        moonSiteSigma = r_siteProfit

    if models.GameProfit.objects.all().exists():
        roundcount = len(models.GameProfit.objects.all())
        lastobject = models.GameProfit.objects.all()[roundcount-1]
        # if utility.is_float_convertible(lastobject.site_profit_sigma) == True:
        siteSigmaProfit = float(lastobject.site_profit_sigma) + siteProfit
        r_siteSigmaProfit = float(lastobject.r_site_profit_sigma) + r_siteProfit
    else:    
        siteSigmaProfit = siteProfit
        r_siteSigmaProfit = r_siteProfit

    if(siteProfit > 0):
        lastSitePlus += siteProfit
        lastSiteMinus = 0.00
        lastPeakValley = lastSitePlus
    else:
        lastSiteMinus += siteProfit
        lastSitePlus = 0.00
        lastPeakValley = lastSiteMinus

    if(r_siteProfit > 0):
        r_lastSitePlus += r_siteProfit
        r_lastSiteMinus = 0.00
        r_lastPeakValley = r_lastSitePlus
    else:
        r_lastSiteMinus += r_siteProfit
        r_lastSitePlus = 0.00
        r_lastPeakValley = r_lastSiteMinus

    players_bet_str = utility.getFormatted(playersBet)
    players_loose_str = utility.getFormatted(playersLoose)
    players_profit_str = utility.getFormatted(playersProfit)
    site_profit_str = utility.getFormatted(siteProfit)
    site_sigma_profit_str = utility.getFormatted(siteSigmaProfit)
    peak_valley_str = utility.getFormatted(lastPeakValley)
    r_players_bet_str = utility.getFormatted(r_playersBet)
    r_players_loose_str = utility.getFormatted(r_playersLoose)
    r_players_profit_str = utility.getFormatted(r_playersProfit)
    r_site_profit_str = utility.getFormatted(r_siteProfit)
    r_site_sigma_profit_str = utility.getFormatted(r_siteSigmaProfit)
    r_peak_valley_str = utility.getFormatted(r_lastPeakValley)
    moon_site_sigma_str = utility.getFormatted(moonSiteSigma)
    gameprofit = models.GameProfit(players_bet = players_bet_str, r_players_bet = r_players_bet_str, payout = str(payOut), players_loose = players_loose_str, r_players_loose = r_players_loose_str,
                            players_profit = players_profit_str, site_profit = site_profit_str, site_profit_sigma = site_sigma_profit_str, site_peak_valley = peak_valley_str, 
                            r_players_profit = r_players_profit_str, r_site_profit = r_site_profit_str, r_site_profit_sigma = r_site_sigma_profit_str, r_site_peak_valley = r_peak_valley_str, moon_site_sigma = moon_site_sigma_str)
    gameprofit.save()
    
    models.lastSiteMinus = utility.getFormatted(lastSiteMinus)
    models.lastSitePlus = utility.getFormatted(lastSitePlus)

    # request = HttpRequest()
    # request.__init__()
    # views.crash(request)

    return True
    
def analyzeProgressData(progress_dataframe):
   print(progress_dataframe)
   
##### upcoming validate
def validate(message):
    global lastScrappingText
    if lastScrappingText == message:
        return False
    else:
        lastScrappingText = message
        return True


