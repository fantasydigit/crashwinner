totalBangAmount = 0.00
totalProfitAmount = 0.00
totalBetAmount = 0.00
curBettingAmount = 0.00
bangString = "bang"
bettingString = "betting"
siteProfit = 0.00
crashPoint = 0.00
greenBet = 0.00
redBet = 0.00

def is_float_convertible(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
def char_distance(string, char1, char2):
    try:
        index_char1 = string.index(char1)
        index_char2 = string.index(char2)
        distance = abs(index_char1 - index_char2)
        return distance
    except ValueError:
        return "One or both characters not found in the string."
    
#define calcuate current betting amount function, yes current round is in progress, not bang yet
def calculateBettingAmount(message):
    #print(message)
    global curBettingAmount
    
    lines = message.splitlines()
    for current_line, next_line in zip(lines, lines[1:]):
        #.......analyze the betting blocks........
            #    betting

            #Pelani01
            #betting
            #$ 3.15
        if bettingString in current_line:
            next_line = next_line.replace(',', '')
            if len(next_line) > 0:
              if "$" == next_line[0]:
                dollar_line = next_line
                #print(dollar_line)
                dollar_line = dollar_line.strip('$\n ')
                if is_float_convertible(dollar_line) == True:
                    curBettingAmount += float(dollar_line)
    # print bang amount
    print(f"Current Betting: ${curBettingAmount}")


#define calcuate totalBangAmount function, yeah~~ round end already
def calculateTotalBangAmount(message):
    global totalBangAmount
    global totalBetAmount
    # Step 1: get bang message from parameter
    lines = message.splitlines()
    for current_line, next_line in zip(lines, lines[1:]):
        # Step 2: Process each line
        #.......analyze the bang blocks........
        # Jducjhphnyb
        # bang	
        # $ 24.01
            
        # $ 24.01
        if bangString in current_line:
            #print(next_line)
            next_line = next_line.replace(',', '')
            if "$" == next_line[0]:
                next_line = next_line.strip('$\n ')
                if next_line != '' and is_float_convertible(next_line) == True:
                    totalBangAmount += float(next_line)
                    totalBetAmount += float(next_line)
        
    # print bang amount
    print(f"Total Bang: $ {totalBangAmount}")

#define calcuate players Profit Amount function, yeah round end already
def calculatePlayersProfitAmount(message):
    global totalProfitAmount, totalBetAmount, crashPoint
    # Step 1: get bang message from parameter
    crashPoint = -1.00
    lines = message.splitlines()
    for index, current_line in enumerate(lines):
    
            # Step 3: Process each line
            #.......analyze the profit blocks........

            #Rxdfetodmyb
            #1.80x	
            #$ 4.80
                
            # $ 3.84
            if len(current_line)>5 and "." in current_line: #7.06x 
                if "x" in current_line and char_distance(current_line, "x", ".") == 3:
                    #print("found x multiply profit player!!")
                    if crashPoint < 0:
                        try:
                            crashPoint = float(current_line.strip('x\t\r\n'))
                        except:
                            print(f"{current_line} is not convertable to float")
                    next_line = lines[index + 1]     
                    if next_line[0] == "$":
                        next_line = next_line.replace(',', '')
                        if next_line[0] == "$":
                            next_line = next_line.strip('$\n ')
                            totalBetAmount += float(next_line)
                            next_line = lines[index+3]
                            if next_line[0] == "$":
                                next_line = next_line.strip('$\n ')
                                next_line = next_line.replace(',', '')
                                totalProfitAmount += float(next_line)
    # print profit amount
    print(f"Total Player Profits: $ {totalProfitAmount}")
    # print bet amount
    print(f"Total Bet: $ {totalBetAmount}")

#define site profit on the issued round

def calculateSiteProfit(classic_message, redgreen_message):
    global siteProfit, totalBangAmount, totalProfitAmount, crashPoint, redBet, greenBet
    bang_message = preProcess(classic_message)
    initGlobalVariables()
    extractRedGreenTrenball(redgreen_message)
    calculateTotalBangAmount(classic_message)
    calculatePlayersProfitAmount(classic_message)

    if crashPoint < 2.00:
        print(f"redBet: {redBet}")
        siteProfit = totalBangAmount - totalProfitAmount + redBet * 1.96 - greenBet
    else:
        siteProfit = totalBangAmount - totalProfitAmount - redBet + greenBet * 2.00
    #insert BetRound Model
    betround = [totalBetAmount, totalBangAmount, totalProfitAmount, siteProfit, crashPoint, redBet, greenBet, 0.00]
    return betround

def preProcess(classic_message):
    #text = 'python model.textfield = "6449629 35.40x 🎉Congrats Hidden won the most! $10,481.41 Player Cash Out Amount Profit Fjqlcogqlyb bang $ 1.53 $ 1.53 Hidden bang $ 0.50 $ 0.50"'
    # Search sentence
    result = classic_message
    search_sentence = "Player Cash Out Amount Profit"
    # Split the text from the search sentence
    splitted_text = classic_message.split(search_sentence)
    # Get the second part of the splitted text
    if len(splitted_text) > 1:
        result = splitted_text[1]
        print(f"split1: {len(result)}")
    else:
        print(f"{search_sentence} not founded")
    search_sentence = "Latest bet & Race"
    splitted_text = result.split(search_sentence)
    if len(splitted_text) > 1:
        result = splitted_text[0]
        print(f"split0: {len(result)}")
    else:
        print(f"{search_sentence} not founded")
    return result

# initialize global variables...
def initGlobalVariables():
    global siteProfit, totalBangAmount, totalProfitAmount, totalBetAmount, greenBet, redBet, crashPoint
    siteProfit = 0.0
    totalBangAmount = 0.0
    totalProfitAmount = 0.0
    totalBetAmount = 0.0
    greenBet = 0.0
    redBet = 0.0
    crashPoint = -1.0

# calculate redbear greenbull profit
def extractRedGreenTrenball(redgreen_message):
    global greenBet, redBet
    #Players 230 $875.41 Players 589 $9,746.94
    words = redgreen_message.split(" ")
    redgreen_result = []
    for word in words:
        if "$" in word:
            word = word.strip('$\n ')
            word = word.replace(',', '')
            redgreen_result.append(word)
    if len(redgreen_result) == 2:
        try:
            redBet = float(redgreen_result[0])
            greenBet = float(redgreen_result[1])
        except:
            print("redbear or greenbull is not convertable to float")
    else:
        print("redgreen result wrong")
        print(redgreen_result)


    
    




