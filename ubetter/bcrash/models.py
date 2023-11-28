from django.db import models
from django.core.files.base import ContentFile
from bcrash.engine import bang_analyzer

# Create your models here.
# def process_text_field(text):
#     processed_text = text.lower()
#     processed_text = 'Processed Text:\n' + processed_text
#     return processed_text

# class TextProcess(models.Model):
#     original = models.TextField()
#     processed = models.TextField()

#     def save(self, *args, **kwargs):
#         self.processed = process_text_field(self.original)
#         return super().save(*args, **kwargs)

################ process classic & trenball bet text input 
def process_text_field(classic_text, redgreen):
    #file_analyzer.calculateBettingAmount(text)
    if classic_text == "":
        return ""
    betround = bang_analyzer.calculateSiteProfit(classic_text, redgreen)
    print(betround[0])
    # formatted_players_bet = "{:.2f}".format(betround[0])
    # formatted_players_bang = "{:.2f}".format(betround[1])
    # formatted_players_profit = "{:.2f}".format(betround[2])
    # formatted_site_profit = "{:.2f}".format(betround[3])
    # formatted_crash_point = "{:.2f}".format(betround[4])
    # formatted_site_historical_profit = "{:.2f}".format(betround[5])
    if BetRound.objects.exists():
        round_count = len(BetRound.objects.all())
        last_bet = BetRound.objects.all()[round_count - 1]
        site_historical_profit = last_bet.site_historical_profit + betround[3]
        last_bet = BetRound(players_bet = betround[0], players_bang = betround[1],
                            players_profit = betround[2], site_profit = betround[3], crash_point = betround[4], 
                            redbear = betround[5], greenbull = betround[6],
                            site_historical_profit = site_historical_profit)
        last_bet.save()
    else:
        site_historical_profit = betround[3]
        last_bet = BetRound(players_bet = betround[0], players_bang = betround[1],
                            players_profit = betround[2], site_profit = betround[3], crash_point = betround[4], 
                            redbear = betround[5], greenbull = betround[6],
                            site_historical_profit = site_historical_profit)
        last_bet.save()

    # round_count = len(BetRound.objects.all())
    # last_bet = BetRound.objects.all()[round_count - 1]
    # formatted_players_bet = "{:.2f}".format(last_bet.players_bet)
    # formatted_players_bang = "{:.2f}".format(last_bet.players_bang)
    # formatted_players_profit = "{:.2f}".format(last_bet.players_profit)
    # formatted_site_profit = "{:.2f}".format(last_bet.site_profit)
    # formatted_site_historical_profit = "{:.2f}".format(last_bet.site_historical_profit)
    # formatted_crash_point = "{:.2f}".format(last_bet.crash_point)
    # processed_text = f"site_profit: ${formatted_site_profit}"
    # print(processed_text)
    # return processed_text
    return ""

#################### process all player text input
def process_gameProfitData(gameprofit_text):
    #file_analyzer.calculateBettingAmount(text)
    if gameprofit_text == "":
        return ""
    betround = bang_analyzer.calculateSiteProfit(classic_text, redgreen)
    print(betround[0])
    # formatted_players_bet = "{:.2f}".format(betround[0])
    # formatted_players_bang = "{:.2f}".format(betround[1])
    # formatted_players_profit = "{:.2f}".format(betround[2])
    # formatted_site_profit = "{:.2f}".format(betround[3])
    # formatted_crash_point = "{:.2f}".format(betround[4])
    # formatted_site_historical_profit = "{:.2f}".format(betround[5])
    if BetRound.objects.exists():
        round_count = len(BetRound.objects.all())
        last_bet = BetRound.objects.all()[round_count - 1]
        site_historical_profit = last_bet.site_historical_profit + betround[3]
        last_bet = BetRound(players_bet = betround[0], players_bang = betround[1],
                            players_profit = betround[2], site_profit = betround[3], crash_point = betround[4], 
                            redbear = betround[5], greenbull = betround[6],
                            site_historical_profit = site_historical_profit)
        last_bet.save()
    else:
        site_historical_profit = betround[3]
        last_bet = BetRound(players_bet = betround[0], players_bang = betround[1],
                            players_profit = betround[2], site_profit = betround[3], crash_point = betround[4], 
                            redbear = betround[5], greenbull = betround[6],
                            site_historical_profit = site_historical_profit)
        last_bet.save()
    return ""


class TextProcess(models.Model):
    original = models.TextField()
    processed = models.TextField()
    redgreen = models.TextField()
    def save(self, *args, **kwargs):
        self.processed = process_text_field(self.original, self.redgreen)
        return super().save(*args, **kwargs)

class BetRound(models.Model):
    players_bet = models.FloatField()
    players_bang = models.FloatField()
    players_profit = models.FloatField()
    site_profit = models.FloatField()
    crash_point = models.FloatField()
    redbear = models.FloatField()
    greenbull = models.FloatField()
    site_historical_profit = models.FloatField()

### class for single player
class Player(models.Model):
    # 1780502935527151919 ->bet_id
    # ebrahim641 -> name    
    # 2.00×	-> payout
    # +$ 0.01 -> profit

    bet_id = models.CharField(max_length=100) 
    name = models.CharField(max_length=100)
    payout = models.CharField(max_length=100)
    profit = models.CharField(max_length=100)

### class for GameProfit
class GameProfit(models.Model):
    players_bet = models.CharField(max_length=100)
    payout = models.CharField(max_length=10)
    crashout = models.CharField(max_length=10)
    players_loose = models.CharField(max_length=100)
    players_profit = models.CharField(max_length=100)
    site_profit = models.CharField(max_length=100)
    site_profit_sigma = models.CharField(max_length=100)
    site_peak_valley = models.CharField(max_length=100)
    r_players_bet = models.CharField(max_length=100)
    r_players_loose = models.CharField(max_length=100)
    r_players_profit = models.CharField(max_length=100)
    r_site_profit = models.CharField(max_length=100)
    r_site_profit_sigma = models.CharField(max_length=100)
    r_site_peak_valley = models.CharField(max_length=100)
    moon_site_sigma = models.CharField(max_length=100)
lastSitePlus = "0"
lastSiteMinus = "0"
gameProgress = ""




