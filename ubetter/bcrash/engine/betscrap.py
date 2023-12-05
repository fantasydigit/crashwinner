from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from . import bet_analyzer
from .bet_analyzer import inputBetData
import time
import pandas as pd
from .. import models
from . import utility

scrappingResult = ""
driver = None
lastGameID = ""
siteSigmaProfit = 0.0
lastPeakValley = 0.0
r_siteSigmaProfit = 0.0
r_lastPeakValley = 0.0
moonSiteSigma = 0.0

def fetch_last_game():
    print("fet_last")
    global driver, lastGameID
    # click last game-item on 1.20x 2.32x 20.33x tab line
    #game_items =  driver.find_elements(By.XPATH, "//div[contains(@class, 'game-item')]")
    #game_items = WebDriverWait(driver,1).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='recent-list']//div[contains(@class, 'game-item')]")))
    try:
        # recent_list = driver.find_element(By.XPATH, "//div[@class='recent-list']")
        # game_items = WebDriverWait(driver,1).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='recent-list']//div[contains(@class, 'game-item')]")))
        # game_items should be 7 items in 765 px width~~~~
        while True:
            last_index = 6
            # time.sleep(1)
            # game_items =  WebDriverWait(driver, 1).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[contains(@class, 'game-item')]")))
            game_items =  driver.find_elements(By.XPATH, "//div[contains(@class, 'game-item')]")
            if len(game_items) == 7:
                last_item = game_items[last_index]
                game_id = last_item.find_element(By.XPATH, ".//div[@class='issus']").text
                #print(f"game_id:{game_id}")
                #print(f"lastGameID:{lastGameID}")
                if game_id != "" and game_id != lastGameID:
                    lastGameID = game_id    
                    last_item.click()
                    # print(f"click issus:{lastGameID}")
                    # pick up game table data from game round dialog
                    #time.sleep(3)
                    timeout = 30 # 30s ?? too long do you think? it's timeout not sleep, kk so no worries.
                    #table_view =  driver.find_element(By.XPATH, "//div[@class='ui-scrollview a1wa45wx']")
                    # table_view = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='ui-scrollview a1wa45wx']")))
                    # table_view = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, "/html/body[1]/div[1]/div[1]/div[1]/div[1]/div[@class='ui-scrollview a1wa45wx']")))
                    table_view = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, "/html/body[1]/div[1]/div[1]/div[1]/div[1]/div[@class='ui-scrollview a45fdda']")))
                    #print(f"scroll:{table_view.text}")
                    global scrappingResult
                    scrappingResult = table_view.text
                    print("trying to input betdata.....")
                    bet_analyzer.inputBetData(scrappingResult)

                    # click close button on game result dialog
                    # close_button =  driver.find_element(By.XPATH, "//button[@class='close-icon i1gm0mn8 dialog-close']")
                    close_button =  driver.find_element(By.XPATH, "/html/body[1]/div[1]/div[1]/div[1]/div[1]/button[@class='close-icon i1gm0mn8 dialog-close']")
                    print(close_button.text)
                    close_button.click()
                    #################################### recursive call for fetch~~~~~~~~~~~~~~~~
                    # fetch_last_game()
                else:
                    time.sleep(0.1)      
            else:
                time.sleep(1)
            
    except:
        fetch_last_game()

def test():
    global driver
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors-spki-list')
    options.add_argument('--ignore-ssl-errors')
    driver = webdriver.Chrome(options=options)
    #driver = webdriver.Firefox()

    # Navigate to the url
    # Open the website
    driver.get("https://bc.game/game/crash")
    driver.set_window_size(765, 600)
    time.sleep(1)
    print("bet_analyzer.test()")
    bet_analyzer.test()
    
def start():
    print("start scrapppppppppppppppppppppping......")
    global driver
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors-spki-list')
    options.add_argument('--ignore-ssl-errors')
    driver = webdriver.Chrome(options=options)
    #driver = webdriver.Firefox()

    # Navigate to the url
    # Open the website
    driver.get("https://bc.game/game/crash")
    driver.set_window_size(765, 600)
    time.sleep(10)
    # click close button on spin dialog
    try:
        pop_dialog =  driver.find_element(By.XPATH, "//div[@class='pop s1583o6t']")
        close_button =  driver.find_element(By.XPATH, "//button[@class='close-icon i1gm0mn8']")
        print(close_button.text)
        close_button.click()
    except:
        print("No Lucky Spin~~")

    #click language icon on header
    # Define the maximum timeout for waiting
    # Use WebDriverWait with the expected condition visibility_of_all_elements_located
    time.sleep(0.2)
    #lang_icon = wait.until(EC._element_if_visible(By.XPATH, "//div[@class='header-language.header-lanitem']//svg"))                  
    lang_icon = driver.find_element(By.XPATH, "//div[@class='header-language header-lanitem']")
    print(f"lang_icon {lang_icon.text}")
    lang_icon.click()
    time.sleep(2)
    # click fiat_nav tab on language widget
    fiat_nav =  driver.find_element(By.XPATH, "//div[@class='ui-tabs tabs-line lan-fiat-tabs']//button[@class='tabs-nav']")
    #fiat_nav = wait.until(EC.element_to_be_clickable(By.XPATH, "//div[@class='l2ib5y0']//div[@class='ui-tabs tabs-line lan-fiat-tabs']//button[@class='tabs-nav']"))
    print(fiat_nav.text)
    fiat_nav.click()    
    # click dollar item
    time.sleep(1)
    dollar_item =  driver.find_element(By.XPATH, "//div[@class='ui-scrollview fiat-list-wrap']//div[@class='fiat-flex-list']//button[1]")
    # dollar_item = wait.until(EC.element_to_be_clickable(By.XPATH, "//div[@class='ui-scrollview fiat-list-wrap']//div[@class='fiat-flex-list']//button[1]"))
    print(dollar_item.text)
    dollar_item.click()
    # show more button click on game/crash/classic
    time.sleep(2)
    # showmore_item =  driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div[2]/div[2]/div[1]/div[3]/button[1]")
    # print(showmore_item.text)
    # showmore_item.click()
    # fetch the last game data
    fetch_last_game()
    # fetch the current game data
    # fetch_current_game()        
    # Close the driver
    driver.quit()

    

def fetch_current_game():
    global driver
    allbet_item =  driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div[2]/div[2]")
    state_item = allbet_item.find_element(By.XPATH, "./div[1]/div[1]")
    total_bet = 0.0
    escape_amount = 0.0
    betting_amount = 0.0
    profit_amount = 0.0    
    r_total_bet = 0.0
    r_escape_amount = 0.0
    r_betting_amount = 0.0
    r_profit_amount = 0.0
    global siteSigmaProfit, lastPeakValley, r_siteSigmaProfit, r_lastPeakValley, moonSiteSigma  
    game_is_win = False
    while True:
        state_str = state_item.get_attribute("class")
        if state_str.__contains__("state"):
            if state_str.__contains__("is-progress"):
                game_is_win = False
                try:
                    players_table = allbet_item.find_element(By.XPATH, "./div[1]/div[2]/table[1]")
                except:
                    time.sleep(0.1)
                    continue
                # table_body = players_table.find_element(By.TAG_NAME, 'tbody')
                # rows = table_body.find_elements(By.TAG_NAME, 'tr')
                # for row in rows:
                #     if row.get_attribute("class") == "user":
                #         print("playername{}")
                # bet_analyzer.analyzeProgressData(players_table.text)
                tbl = players_table.get_attribute('outerHTML')
                df = pd.read_html(tbl)[0]
                #bet_analyzer.analyzeProgressData(df)
                print(len(df))
                total_bet = 0.0
                escape_amount = 0.0
                betting_amount = 0.0
                profit_amount = 0.0    
                r_total_bet = 0.0
                r_escape_amount = 0.0
                r_betting_amount = 0.0
                r_profit_amount = 0.0
                player_count = len(df)  
                escape_count = 0
                for i in range(player_count):
                    # print(f"{i}{df.size}")
                    dollar_str = df.iloc[i,2]
                    if '$' in dollar_str:
                        dollar_str = dollar_str.replace('$','')
                        dollar_str = dollar_str.replace(',', '')
                        if "Betting" in df.iloc[i,1]:
                            total_bet += float(dollar_str)
                            betting_amount += float(dollar_str)
                            if df.iloc[i,0] == "Hidden" and float(dollar_str) > 1000.00:
                                continue
                            else:
                                r_total_bet += float(dollar_str)
                                r_betting_amount += float(dollar_str)
                        else:
                            escape_count += 1
                            profit_str = df.iloc[i,3]
                            profit_str = dollar_str.replace('$','')
                            profit_str = dollar_str.replace(',', '')    
                            total_bet += float(dollar_str)
                            escape_amount += float(dollar_str)
                            profit_amount += float(profit_str)
                            if df.iloc[i,0] == "Hidden" and float(dollar_str) > 1000.00:
                                continue
                            else:
                                r_total_bet += float(dollar_str)
                                r_escape_amount += float(dollar_str)
                                r_profit_amount += float(profit_str)
                                
                    else:
                        print("JB Coin")
                profit_amount = int(profit_amount)
                betting_amount = int(betting_amount)
                r_profit_amount = int(r_profit_amount)
                r_betting_amount = int(r_betting_amount)
                # print(f"{profit_amount}/{betting_amount}")
                models.gameProgress = f"{escape_count}/{player_count}\t\t{profit_amount}/{betting_amount}\t\t{r_profit_amount}/{r_betting_amount}"
                time.sleep(0.1)
            elif state_str.__contains__("is-win"):
                if game_is_win == True:
                    continue
                else:
                    game_is_win = True
                try:
                    players_table = allbet_item.find_element(By.XPATH, "./div[1]/div[2]/table[1]")
                except:
                    time.sleep(0.1)
                    continue
                tbl = players_table.get_attribute('outerHTML')
                df = pd.read_html(tbl)[0]
                total_bet = 0.0
                escape_amount = 0.0
                bang_amount = 0.0
                profit_amount = 0.0    
                r_total_bet = 0.0
                r_escape_amount = 0.0
                r_bang_amount = 0.0
                r_profit_amount = 0.0
                player_count = len(df)  
                escape_count = 0
                cash_out = 0.00
                for i in range(player_count):
                    # print(f"{i}{df.size}")
                    dollar_str = df.iloc[i,2]
                    if '$' in dollar_str:
                        dollar_str = dollar_str.replace('$','')
                        dollar_str = dollar_str.replace(',', '')
                        if "bang" in df.iloc[i,1]:
                            total_bet += float(dollar_str)
                            bang_amount += float(dollar_str)
                            if df.iloc[i,0] == "Hidden" and float(dollar_str) > 1000.00:
                                continue
                            else:
                                r_total_bet += float(dollar_str)
                                r_bang_amount += float(dollar_str)
                        else:
                            escape_count += 1
                            cashout_str = df.iloc[i,1]
                            cashout_str = cashout_str.replace('x','')
                            if (cash_out < float(cashout_str)):
                                cash_out = float(cashout_str)
                            profit_str = df.iloc[i,3]
                            profit_str = dollar_str.replace('$','')
                            profit_str = dollar_str.replace(',', '')    
                            total_bet += float(dollar_str)
                            escape_amount += float(dollar_str)
                            profit_amount += float(profit_str)
                            if df.iloc[i,0] == "Hidden" and float(dollar_str) > 1000.00:
                                continue
                            else:
                                r_total_bet += float(dollar_str)
                                r_escape_amount += float(dollar_str)
                                r_profit_amount += float(profit_str)
                                
                    else:
                        print("JB Coin")
                profit_amount = int(profit_amount)
                bang_amount = int(bang_amount)
                r_profit_amount = int(r_profit_amount)
                r_bang_amount = int(r_bang_amount)
                # print(f"{profit_amount}/{betting_amount}")
                models.gameProgress = f"{escape_count}/{player_count}\t\t{profit_amount}/{bang_amount}\t\t{r_profit_amount}/{r_bang_amount}"
                
                site_profit = bang_amount - profit_amount
                siteSigmaProfit += site_profit
                if lastPeakValley < 0 and site_profit > 0:
                    lastPeakValley = site_profit
                elif lastPeakValley > 0 and site_profit < 0:
                    lastPeakValley = site_profit
                else:
                    lastPeakValley += site_profit
                r_site_profit = r_bang_amount - r_profit_amount
                r_siteSigmaProfit += r_site_profit
                if r_lastPeakValley < 0 and r_site_profit > 0:
                    r_lastPeakValley = r_site_profit
                elif lastPeakValley > 0 and site_profit < 0:
                    r_lastPeakValley = r_site_profit
                else:
                    r_lastPeakValley += r_site_profit
                if cash_out < 10.00 :
                    moonSiteSigma += r_site_profit
                else:
                    moonSiteSigma = r_site_profit
                players_bet_str = utility.getFormatted(total_bet)
                players_loose_str = utility.getFormatted(total_bet-escape_amount)
                players_profit_str = utility.getFormatted(profit_amount)
                site_profit_str = utility.getFormatted(betting_amount-profit_amount)
                site_sigma_profit_str = utility.getFormatted(siteSigmaProfit)
                peak_valley_str = utility.getFormatted(lastPeakValley)
                r_players_bet_str = utility.getFormatted(r_total_bet)
                r_players_loose_str = utility.getFormatted(r_bang_amount)
                r_players_profit_str = utility.getFormatted(r_profit_amount)
                r_site_profit_str = utility.getFormatted(r_site_profit)
                r_site_sigma_profit_str = utility.getFormatted(r_siteSigmaProfit)
                r_peak_valley_str = utility.getFormatted(r_lastPeakValley)
                moon_site_sigma_str = utility.getFormatted(moonSiteSigma)
                gameprofit = models.GameProfit(players_bet = players_bet_str, r_players_bet = r_players_bet_str, payout = str(cash_out), players_loose = players_loose_str, r_players_loose = r_players_loose_str,
                                        players_profit = players_profit_str, site_profit = site_profit_str, site_profit_sigma = site_sigma_profit_str, site_peak_valley = peak_valley_str, 
                                        r_players_profit = r_players_profit_str, r_site_profit = r_site_profit_str, r_site_profit_sigma = r_site_sigma_profit_str, r_site_peak_valley = r_peak_valley_str, moon_site_sigma = moon_site_sigma_str)
                gameprofit.save()
                time.sleep(0.1)
                print("bang state now")
            else:
                print("something wrong!")
        else:
            print("state_item wrong...")
            break





    