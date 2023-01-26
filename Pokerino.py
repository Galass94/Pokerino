import random
import os
import pandas as pd

suits = ["Hearts", "Diamonds", "Spades", "Clubs"]
short_suits = ["h", "d", "s", "c"]
card_display = [2,3,4,5,6,7,8,9,10,'J','Q','K','A']
card_values = [2,3,4,5,6,7,8,9,10,11,12,13,14]
player_classes = ["w", "m", "t", "d", "b", "p", "v", "g", "r"]
player_classes_dict = { "Warrior": "Can destroy one card on the table. - 1 use", 
                        "Mage": "Can change the values of a card on the table by 1. - 2 uses",
                        "Trader": "Can trade one card from their hand with one card on the table. - 1 use",
                        "Deprived": "BONK! - 3 uses",
                        "Bard": "Gets a free mulligan. - 1 use",
                        "Priest": "Can change the value or suit of the top card of the deck. - 2 uses",
                        "Viking" : "Plunders card values from the table and adds them to their hand. - 1 use",
                        "Gambler": "Merges all cards together, shuffles them and redistributes them. - 1 use",
                        "Random": "Gets a random ability. The ability is rerolled every turn! - 2 uses*"
                    }

class Card:
    def __init__(self, value, suit, display, index):
        self.value = value
        self.suit = suit
        self.display = display
        self.index = index
        self.winners = {"Pair": False, "Triple": False, "Quad": False, "Penta":False, "Hexa":False}

    def getValue(self):
        return self.value
    def setValue(self, x):
        self.value = x
    def getSuit(self):
        return self.suit
    def setSuit(self, suit):
        self.suit = suit
    def getDisplay(self):
        return self.display
    def setDisplay(self, display):
        self.display = display

    def __str__(self):
        return f"{card_display[card_values.index(self.value)]:>2} of {self.suit}"
    def __eq__(self, other):
        if isinstance(other, Card):
            return self.value == other.value and self.suit == other.suit and self.index == other.index
        return False
class Deck:
    deck = []
    def __init__(self):
        count=0
        for suit in suits:
            for value in card_values:
                self.deck.append(Card(value, suit, card_display[card_values.index(value)], count+1))
                count += 1
    def shuffle(self):
        random.shuffle(self.deck)
class Table:
    def __init__(self):
        self.listTableCards = []
    def revealCard(self):
        self.listTableCards.append(deck.deck.pop(0))
        self.printCards()
    def printCards(self):
        index=1
        print("--- Table Cards ---")
        for card in self.listTableCards:
            print(f"({index}) {card}")
            index+=1
    def replaceCards(self, newCardList):
        self.listTableCards = newCardList
    def removeCard(self, index):
        self.listTableCards.pop(index)
    def turnOne(self):
        # for player in playerList:
        #     player.printHand()
        for i in range(0,3):
            self.listTableCards.append(deck.deck.pop(0))
        # self.printCards()
        if len(self.listTableCards) < 5:
            # if(playerList[0].activateAbility()):
                nextTurnWithAbilities(False, 0)
            # else:
            #     nextTurnWithAbilities(True, 0)
class Player:
    def __init__(self):
        while True:
            try:
                self.name = input("Enter Player Name: ")
                if len(self.name) == 0: raise ValueError
                break
            except ValueError:
                print("You need a name!")
        while True:
            try:
                os.system("cls")
                print(f"What class are you, {self.getName()}?\n")
                for index, (key,value) in enumerate(player_classes_dict.items(), start=1):
                    print(f"({index}) - {key}: {value}")
                print("* - EXCEPTIONS : Gambler ability not available and Bard uses both activations!")
                self.ability = int(input("\nChoose class: "))
                if self.ability > len(player_classes) or self.ability < 1: raise ValueError
                break
            except ValueError as e:
                print("Please choose a class!")
                os.system("pause")
                os.system("cls")
        player_list.append(self)
        self.handsize=2
        self.money=200
        self.has_bet = False
        self.has_bet_big_blind = False
        self.bet = 0
        self.current_bet = 0
        self.handCards = []
        self.handValues = []
        self.highestCard: str
        self.pairs = []
        self.triples = []
        self.quads = []
        self.pentas = []
        self.hexas = []
        self.flush: str
        self.straightFlush = []
        self.royalFlush = []
        self.score=0
        if   self.ability == 1:
            self.player_class = "Warrior"
            self.abilityCount = 1
        elif self.ability == 2:
            self.player_class = "Mage"
            self.abilityCount = 2
        elif self.ability == 3:
            self.player_class = "Thief"
            self.abilityCount = 1
        elif self.ability == 4:
            self.player_class = "Deprived"
            self.abilityCount = 3
        elif self.ability == 5:
            self.player_class = "Bard"
            self.abilityCount = 1
        elif self.ability == 6:
            self.player_class = "Priest"
            self.abilityCount = 2
        elif self.ability == 7:
            self.player_class = "Viking"
            self.abilityCount = 1
        elif self.ability == 8:
            self.player_class = "Gambler"
            self.abilityCount = 1
        elif self.ability == len(player_classes):
            self.player_class = "Random"
            self.abilityCount = 2
        for card in range(self.handsize):
            self.handCards.append(deck.deck.pop(0))
        print(f"{self.getName()} joins the table!")
        os.system("pause")
        os.system("cls")

    def getName(self):          # get player name and capitalize it
        return self.name.capitalize()
    def getHandCSV(self):       # format cards for output as value in CSV file
        handCSV = []
        for card in self.handCards:
            handCSV.append(f"{card.getDisplay():>2} of {card.getSuit()}")
        return handCSV
    def warriorAbility(self):   # Warrior who destroys one card on the table
        print("You activated your ability to destroy one card on the table")
        while True:
            try:
                choice2 = int(input("Which one do you want to remove? - "))
                if choice2 > len(table.listTableCards): raise ValueError
                break
            except ValueError as e:
                print("Enter a valid number!")
        table.listTableCards.pop(choice2-1)
    def mageAbility(self):      # Mage who changes the value of up to 2 cards on the table
        print("You activated your ability to change the value of one card on the table!")
        while True:
            try:
                choice2 = int(input("Which card would you like to change?  "))
                if choice2 > len(table.listTableCards): raise ValueError
                break
            except ValueError as e:
                print("Enter a valid number!")
        choice3 = input("Would you like to increase(+) or decrease(-) the card's value?  ")
        if choice3=='+':
            if table.listTableCards[choice2-1].getValue() == 14:
                table.listTableCards[choice2-1].setValue(2)
            else:
                table.listTableCards[choice2-1].setValue(card_values[card_values.index(table.listTableCards[choice2-1].value)+1])
        elif '-':
            if table.listTableCards[choice2-1].getValue() == 2:
                table.listTableCards[choice2-1].setValue(14)
            else:
                table.listTableCards[choice2-1].setValue(card_values[card_values.index(table.listTableCards[choice2-1].value)-1])
    def traderAbility(self):    # Trader who exchanges one card from his hand with one from the table
        print("You activated your ability to switch one card from the table with one from your hand!")
        while True:
            try:
                choiceT = int(input("Which card from the table would you like to take? "))
                if choiceT > len(table.listTableCards): raise ValueError
                break
            except ValueError as e:
                print("Enter a valid number!")
        while True:
            try:
                choiceT2 = int(input("Which card from your hand do you want to put on the table? "))
                if choiceT2 > 2: raise ValueError
                break
            except ValueError as e:
                print("Enter a valid number!")
        self.handCards.append(table.listTableCards.pop(choiceT-1))
        table.listTableCards.append(self.handCards.pop(choiceT2-1))
    def deprivedAbility(self):  # BONK
        temp = random.randint(0, 99)
        if temp <= 4:
            print(f"{player_list[random.randint(0,len(player_list)-1)].getName()} got BONKed!!!")
        else :
            print("BONK!")
    def bardAbility(self):      # Bard who gets one free mulligan
        self.printHand()
        print(f"{self.getName()}, do you want to draw a new hand? (Y/N)")
        choiceB = input().lower()
        match(choiceB):
            case "y":
                for i in range(2):
                    # print(f"{self.handCards[0]} was put into the deck.")
                    deck.deck.append(self.handCards.pop(0))
                deck.shuffle()
                print()
                for i in range(0,2):
                    # print(f"{self.getName()} drew a {deck.deck[0]}")
                    self.handCards.append(deck.deck.pop(0))
                self.abilityCount -= 1
            case "n":
                self.abilityCount -= 1
                pass
        pass
    def priestAbility(self):    # Priest who can influence cards on top of the deck instead of the table
        print("You activated your ability to change the value or suit of the top card of the deck!")
        print(f"The next card is {deck.deck[0]}")
        while True:
            try:
                choice_p = input("Do you want to change the value or the suit of the card? (v/s) -> ").lower()
                # if choice_p != 'v' or choice_p != 's': raise ValueError
                break
            except ValueError as e:
                print("Please choose between \'v\' and \'s\'!")
        match choice_p:
            case "v":
                choice_p2 = input("Do you want to increase or decrease the value? (+/-) -> ")
                if choice_p2=='+':
                    if deck.deck[0].getValue() == 14:
                        deck.deck[0].setValue(2)
                    else:
                        deck.deck[0].setValue(card_values[card_values.index(deck.deck[0].value)+1])
                elif '-':
                    if deck.deck[0].getValue() == 2:
                        deck.deck[0].setValue(14)
                    else:
                        deck.deck[0].setValue(card_values[card_values.index(deck.deck[0].value)-1])
            case "s":
                while True:
                    try:
                        choice_p2 = input("Which suit do you want the card to have? -> ").lower()
                        if choice_p2 not in short_suits: raise ValueError
                        break
                    except ValueError as e:
                        print("Enter a correct Suit! (d,h,c or s)")
                match choice_p2:
                    case "d":
                        deck.deck[0].setSuit("Diamonds")
                    case "h":
                        deck.deck[0].setSuit("Hearts")
                    case "c":
                        deck.deck[0].setSuit("Clubs")
                    case "s":
                        deck.deck[0].setSuit("Spades")
        print(f"Changed the top card to {deck.deck[0]}")
    def vikingAbility(self):    # Viking can plunder card values from the table to raise their own hand values while lowering values on the table
        print("You activated your ability to plunder!")
        count = 0
        for card in table.listTableCards:
            chance = random.randint(0,len(table.listTableCards)*20)
            handChoice = random.randint(0,1)
            if chance < 5:
                if card.getValue() > 5:
                    card.setValue(card.getValue() - 3)
                    if self.getHandCards()[handChoice].getValue()+3 <= 14:
                        self.getHandCards()[handChoice].setValue(self.getHandCards()[handChoice].getValue()+3)
                    else: 
                        self.getHandCards()[handChoice].setValue(self.getHandCards()[handChoice].getValue()+3-13)
                    count += 1
                elif card.getValue() <= 4:
                    card.setValue(13+card.getValue() - 3)
                    if self.getHandCards()[handChoice].getValue()+3 <= 14:
                        self.getHandCards()[handChoice].setValue(self.getHandCards()[handChoice].getValue()+3)
                    else: 
                        self.getHandCards()[handChoice].setValue(self.getHandCards()[handChoice].getValue()+3-13)
                    count += 1
            elif chance < 20:
                if card.getValue() > 4:
                    card.setValue(card.getValue() - 2)
                    if self.getHandCards()[handChoice].getValue()+2 <= 14:
                        self.getHandCards()[handChoice].setValue(self.getHandCards()[handChoice].getValue()+2)
                    else: 
                        self.getHandCards()[handChoice].setValue(self.getHandCards()[handChoice].getValue()+2-13)
                    count += 1
                elif card.getValue() <= 3:
                    card.setValue(13+card.getValue() - 2)
                    if self.getHandCards()[handChoice].getValue()+2 <= 14:
                        self.getHandCards()[handChoice].setValue(self.getHandCards()[handChoice].getValue()+2)
                    else: 
                        self.getHandCards()[handChoice].setValue(self.getHandCards()[handChoice].getValue()+2-13)
                    count += 1
            elif chance < 50:
                if card.getValue() > 3:
                    card.setValue(card.getValue() - 1)
                    if self.getHandCards()[handChoice].getValue()+1 <= 14:
                        self.getHandCards()[handChoice].setValue(self.getHandCards()[handChoice].getValue()+1)
                    else: 
                        self.getHandCards()[handChoice].setValue(self.getHandCards()[handChoice].getValue()+1-13)
                    count += 1
                elif card.getValue() <= 2:
                    card.setValue(13+card.getValue() - 1)
                    if self.getHandCards()[handChoice].getValue()+1 <= 14:
                        self.getHandCards()[handChoice].setValue(self.getHandCards()[handChoice].getValue()+1)
                    else: 
                        self.getHandCards()[handChoice].setValue(self.getHandCards()[handChoice].getValue()+1-13)
                    count += 1
        print(f"You plundered from {count} cards!")
        os.system("pause")
    def gamblerAbility(self):
        newList = []
        for card in table.listTableCards:
            newList.append(card)
        for i in range(len(player_list)):
            for card in player_list[i].getHandCards():
                newList.append(card)
        for i in range(7):
            random.shuffle(newList)
        for player in player_list:
            player.setHandCards([newList.pop(0), newList.pop(1)])
        table.replaceCards(newList)
    def randomAbility(self):    # Get a random ability every time you activate yours
        temp = random.randint(0, len(player_classes)-3)
        match temp:
            case 0:
                print("WARRIOR ABILITY") 
                self.warriorAbility()
            case 1: 
                print("MAGE ABILITY") 
                self.mageAbility()
            case 2: 
                print("TRADER ABILITY") 
                self.traderAbility()
            case 3: 
                print("DEPRIVED ABILITY") 
                self.deprivedAbility()
            case 4:
                print("BARD ABILITY")
                self.bardAbility()
            case 5:
                print("PRIEST ABILITY")
                self.priestAbility()
            case 6: 
                print("VIKING ABILITY")
                self.vikingAbility()            
        pass
    def activateAbility(self):
        while self.abilityCount > 0:
            choice = input(f"\n{self.getName()}, do you want to activate an ability? - ")
            match(choice):
                case 'y':
                    self.abilityCount -= 1
                    if   self.player_class == "Warrior":
                        self.warriorAbility()
                        return True
                    elif self.player_class == "Mage":
                        self.mageAbility()
                        return True
                    elif self.player_class == "Trader":
                        self.traderAbility()
                        return True
                    elif self.player_class == "Deprived":
                        self.deprivedAbility()
                        return True
                    elif self.player_class == "Priest":
                        self.priestAbility()
                        return True
                    elif self.player_class == "Viking":
                        self.vikingAbility()
                        return True
                    elif self.player_class == "Gambler":
                        self.gamblerAbility()
                        return True
                    elif self.player_class == "Random":
                        self.randomAbility()
                        return True
                case 'n':
                    return False
    def getAbility(self):
        return self.ability
    def getPlayerClass(self):
        return self.player_class
    def addScore(self, x):
        self.score += x
    def getScore(self):
        return self.score
    def printScore(self):
        print(f"{self.getName()}: {self.score} points")
    def printHand(self):
        print(f"--- {self.getName()}'s Hand ({self.player_class})---   (Current Bet: {self.getBet()})")
        for card in self.handCards:
            print(card)
        print()
    def addMoney(self, x):
        self.money += x
    def getMoney(self):
        return self.money
    def betMoney(self, x):
        if x >= self.money:
            print(f"{self.getName()} goes ALL IN!")
            split_pot.addMoney(self.money)
            self.current_bet += self.money
            self.setBet(self.money)
            self.money = 0
        elif all_in_value > 0:
            split_pot.addMoney(all_in_value)
            pot.addMoney(x-all_in_value)
            self.current_bet += x
            self.setBet(x)
            self.money -= x
        else:
            self.money -= x
            pot.addMoney(x)
            self.current_bet += x
            self.setBet(x)
        self.has_bet = True
    def setHasBetBigBlind(self, has_bet_big_blind):
        self.has_bet_big_blind = has_bet_big_blind
    def getHasBetBigBlind(self):
        return self.has_bet_big_blind
    def setBet(self, bet):
        self.bet += bet
        self.has_bet = True
    def getBet(self):
        return self.bet
    def getCurrentBet(self):
        return self.current_bet
    def setCurrentBet(self, x):
        self.current_bet = x
    def getHasBet(self):
        return self.has_bet
    def setHandValues(self):
        self.handValues.clear()
        for card in self.handCards:
            self.handValues.append(card.getValue())
    def getHandValues(self):
        short_hand_values = self.handValues
        for value in short_hand_values:
            if short_hand_values.count(value) >1:
                short_hand_values.remove(value)
        return short_hand_values
    def setgetHandValues(self):
        self.handValues.clear()
        for card in self.handCards:
            self.handValues.append(card.getValue())
            return self.handValues
    def getHandCards(self):
        return self.handCards
    def setHandCards(self, newCards):
        self.handCards = newCards
    def setHighestCard(self, card):
        self.highestCard = card
    def getHighestCard(self):
        return self.highestCard
    def setStraight(self, cards):
        self.straight = cards
    def getStraight(self):
        return self.straight
    def setRoyalFlush(self, card):
        self.royalFlush.append(card)
    def getRoyalFlush(self):
        return self.royalFlush
    def setStraightFlush(self, suit, cards):
        self.straightFlush = [suit, cards]
    def getStraightFlush(self):
        return self.straightFlush
    def emptyRoyalFlush(self):
        self.royalFlush.clear()
    def setFlush(self, suit):
        self.flush = suit
    def getFlush(self):
        return self.flush
    def setPairs(self, value):
        self.pairs.append(value)
class Pot:
    def __init__(self):
        self.money = 0
    def clearPot(self):
        self.money = 0
    def getMoney(self):
        return self.money
    def addMoney(self, x):
        self.money += x
    def potToWinner(self):
        for player in playerWin:
            player.addMoney(int(self.money/len(playerWin)))
def nextTurn(draw):                     # Advance one turn - boolean draw to decide whether the table gets an extra card or not
    print("\n\n")
    os.system("pause")
    os.system("cls")
    for player in player_list:
        player.printHand()
    if draw:
        table.revealCard()
    else:
        table.printCards()
    if len(table.listTableCards) < 5:
        if(player_list[0].activateAbility()):
            nextTurn(False)
        else:
            nextTurn(True)
    else: pass
def nextTurnWithAbilities(draw, index): # Next turn where every player can activate their ability once per turn - Multiplayer
    os.system("\n\npause")
    os.system("cls")
    if draw:
        table.listTableCards.append(deck.deck.pop(0))
    # for index in len(playerList):
    print(f"{player_list[index].getName()}, it is your turn to play!")
    os.system("pause")
    os.system("cls")
    player_list[index].printHand()
    table.printCards()
    player_list[index].activateAbility()
    if len(table.listTableCards) < 5:
        if index == len(player_list)-1:
            startGameBets(False)
            nextTurnWithAbilities(True, 0)
        else:
            nextTurnWithAbilities(False, index+1)
    elif index!= len(player_list)-1 and len(table.listTableCards) == 5: 
        nextTurnWithAbilities(False, index+1)
        # lastTurn()
    else:
        lastTurn()
def lastTurn():                         # Finishing turn where all players can activate their abilities one more time
    for player in player_list:
        player.printHand()
    table.printCards()
def checkRoyalFlush(player):            # Check player's hand for a Royal Flush
    royalFlush = [[Card(14, "Diamonds", "A"), Card(13, "Diamonds", "K"), Card(12, "Diamonds", "Q"), Card(11, "Diamonds", "J"), Card(10, "Diamonds", 10)],
    [Card(14, "Hearts", "A"), Card(13, "Hearts", "K"), Card(12, "Hearts", "Q"), Card(11, "Hearts", "J"), Card(10, "Hearts", 10)],
    [Card(14, "Clubs", "A"), Card(13, "Clubs", "K"), Card(12, "Clubs", "Q"), Card(11, "Clubs", "J"), Card(10, "Clubs", 10)],
    [Card(14, "Spades", "A"), Card(13, "Spades", "K"), Card(12, "Spades", "Q"), Card(11, "Spades", "J"), Card(10, "Spades", 10)]]
    for i in range(4):
        count=0
        player.emptyRoyalFlush()
        for j in range(5):
            for card in player.handCards:
                if card == royalFlush[i][j]:
                    # print(f"{card}: I'm in there")
                    count += 1
                    player.setRoyalFlush(royalFlush[i][j])
                    break
        if count==5:
            break
    if count==5:
        return True
    else:
        return False
def checkStraight(player):              # Check player's hand for Flush
    count=0
    straightCards = []
    hasStraight=False
    values = player.setgetHandValues()
    for i in range(0,len(values)-1):
        if player.handCards[i].getValue() == player.handCards[i+1].getValue():
            continue
        elif (player.handCards[i].getValue())-1 == player.handCards[i+1].getValue():
            count += 1
            straightCards.append(player.handCards[i])
        else: 
            count=0
            straightCards.clear()
        if count>=4:
            if len(straightCards)==4:
                straightCards.append(player.handCards[i+1])
            hasStraight = True
            break
    if hasStraight:
        if checkRoyalFlush(player):
            return "Royal Flush"
        player.setStraight(straightCards)
        if checkFlush(player):
            player.setStraightFlush(straightCards[0].getSuit(), straightCards)
            return "Straight Flush"
        else:
            return "Straight"
def checkFlush(player):                 # Check if player has Flush and if they do, return the suit of the flush
    diamondCount = 0
    heartCount = 0
    spadeCount = 0
    clubCount = 0
    hasFlush = False
    for card in player.handCards:
        if card.getSuit() == "Diamonds":
            diamondCount += 1
        if card.getSuit() == "Hearts":
            heartCount += 1
        if card.getSuit() == "Spades":
            spadeCount += 1
        if card.getSuit() == "Clubs":
            clubCount += 1
    if diamondCount >= 5:
        player.setFlush("Diamonds")
        # print(f"{player.getName()} has a Flush of Diamonds!")
        hasFlush = True
    elif heartCount >= 5:
        player.setFlush("Hearts")
        # print(f"{player.getName()} has a Flush of Hearts!")
        hasFlush = True
    elif spadeCount >= 5:
        player.setFlush("Spades")
        # print(f"{player.getName()} has a Flush of Spades!")
        hasFlush = True
    elif clubCount >= 5:
        player.setFlush("Clubs")
        # print(f"{player.getName()} has a Flush of Clubs!")
        hasFlush = True
    return hasFlush
def checkMultiples(player):             # Check if player has multiples of a value and if they do, return the highest multiple
    for card in player.handCards:
        card.winners["Pair"] = False
        card.winners["Triple"] = False
        card.winners["Quad"] = False
        card.winners["Penta"] = False
        card.winners["Hexa"] = False
        count = 0
        hasMultiples = False
        for cardToComp in player.handCards:
            if player.handCards.index(card) == player.handCards.index(cardToComp):
                continue
            if card.getValue() == cardToComp.getValue():
                count += 1
                if count==5:
                    card.winners["Hexa"] = True
                elif count==4:
                    card.winners["Penta"] = True
                elif count==3:
                    card.winners["Quad"] = True
                elif count == 2:
                    card.winners["Triple"] = True
                elif count == 1:
                    card.winners["Pair"] = True
    doubleCardValues = []
    doubleCardValues.clear()
    tripleCardValues = []
    tripleCardValues.clear()
    quadCardValues = []
    quadCardValues.clear()
    pentaCardValues=[]
    pentaCardValues.clear()
    hexaCardValues=[]
    hexaCardValues.clear()
    listFullHouse = []
    listFullHouse.clear()
    triple=0
    double=0
    hasFullHouse = False
    for card in player.handCards:
        if card.winners["Hexa"]:
            if card.getValue() not in hexaCardValues:
                hexaCardValues.append(card.getValue())
                hasMultiples=True
        elif card.winners["Penta"]:
            if card.getValue() not in pentaCardValues:
                pentaCardValues.append(card.getValue())
                hasMultiples=True
        elif card.winners["Quad"]:
            if card.getValue() not in quadCardValues:
                quadCardValues.append(card.getValue())
                hasMultiples=True
        elif card.winners["Triple"]:
            if card.getValue() not in tripleCardValues:
                tripleCardValues.append(card.getValue())
                hasMultiples=True
                triple = 1
                listFullHouse.append(card)
        elif card.winners["Pair"]:
            if card.getValue() not in doubleCardValues:
                doubleCardValues.append(card.getValue())
                hasMultiples=True
                double = 1
        if triple == 1 and double == 1 : # Check for Full House
            hasFullHouse = True
    if hasFullHouse:
        player.addScore(15)
        print(f"{player.getName()} has a Full House!")
    else:
        if hexaCardValues:
            for card in hexaCardValues:
                print(f"{player.getName()} has 6 {card_display[card_values.index(card)]}s")
                player.addScore(100)
        elif pentaCardValues:
            for card in pentaCardValues:
                print(f"{player.getName()} has 5 {card_display[card_values.index(card)]}s")
                player.addScore(50)
        elif quadCardValues:
            for card in quadCardValues:
                print(f"{player.getName()} has 4 {card_display[card_values.index(card)]}s")
                player.addScore(20)
        elif tripleCardValues:
            for card in tripleCardValues:
                print(f"{player.getName()} has 3 {card_display[card_values.index(card)]}s")
                player.addScore(7)
        elif doubleCardValues:
            for card in doubleCardValues:
                print(f"{player.getName()} has a pair of {card_display[card_values.index(card)]}s")
                player.addScore(2)
    return hasMultiples
def highestCard(player):                # If player has nothing else, output the highest card in their Hand
    player.addScore(1)
    print(f"{player.getName()}'s highest card is {card_display[card_values.index(player.handCards[0].getValue())]}")
    player.setHighestCard(player.getHandCards()[0])
def values(player):                     # Check all cards from player's hand and decide what the most valuable combination is
    # Add cards from table to hand of each player for easier comparison
    for card in table.listTableCards:
        player.handCards.append(card)
    player.handCards.sort(key=Card.getValue,reverse=True)
    while True:
        if checkStraight(player) == "Royal Flush":
            player.addScore(40)
            if player.getAbility() != "d":
                print(f"{player.getName()} has a ROYAL FLUSH!!!")
            else:
                print(f"{player.getName()}: Such Royal Flush, Much Wow, Great!")
            for card in player.getRoyalFlush():
                print(card)
            break
        elif checkStraight(player) == "Royal Straight":
            player.addScore(25)
            print(f"{player.getName()} has a Royal Straight!")
            for card in player.getStraight():
                print(card)
            break
        elif checkStraight(player) == "Straight Flush":
            player.addScore(20)
            print(f"{player.getName()} has a Straight Flush of", end=" ")
            print(player.getStraightFlush()[0])
            for card in player.getStraightFlush()[1]:
                print(f"{card.getValue():>2} of {player.getStraightFlush()[0]}")
            break
        elif checkStraight(player) == "Straight":
            player.addScore(10)
            print(f"{player.getName()} has a Straight!")
            break
        elif checkFlush(player):
            player.addScore(12)
            print(f"{player.getName()} has a Flush of", end=" ")
            print(player.getFlush())
            break
        elif checkMultiples(player):
            break
        else: 
            highestCard(player)
            break
def stackDeckCheck():
    deck.deck[0] = Card(8,"Hearts", 8, 1)        #P1
    deck.deck[1] = Card(6,"Hearts", 6, 2)        #P1
    deck.deck[2] = Card(11,"Clubs", 'J', 3)     #P2
    deck.deck[3] = Card(2,"Hearts", 2, 4)        #P2
    deck.deck[4] = Card(3,"Clubs", 3, 5)        #P3
    deck.deck[5] = Card(7,"Spades", 7, 6)        #P3
    deck.deck[6] = Card(9,"Hearts", 9, 7)        #Table vvvvv
    deck.deck[7] = Card(6,"Clubs", 6, 8)
    deck.deck[8] = Card(13,"Clubs", 'K', 9)
    deck.deck[9] = Card(10,"Hearts", 10, 10)
    deck.deck[10] = Card(2,"Hearts", 2, 11)
def stackDeck1PFlush():
    deck.deck[0] = Card(2,"Diamonds", 2)
    deck.deck[1] = Card(3,"Diamonds", 3)
    deck.deck[2] = Card(4,"Diamonds", 4)
    deck.deck[3] = Card(5,"Diamonds", 5)
    deck.deck[4] = Card(6,"Diamonds", 6)
    deck.deck[5] = Card(4, "Spades", 4)
def stackDeck2PSameCards():
    deck.deck[0] = Card(2,"Diamonds", 2, 1) #P1
    deck.deck[1] = Card(3,"Spades", 3, 2) #P1
    deck.deck[2] = Card(3,"Clubs", 3, 3) #P2
    deck.deck[3] = Card(3,"Diamonds", 3, 4) #P2
    deck.deck[4] = Card(2,"Hearts", 2, 5) #Table vvvvv
    deck.deck[5] = Card(3,"Diamonds", 3, 6)
    deck.deck[6] = Card(4,"Clubs", 4, 7)
    deck.deck[7] = Card(5,"Hearts", 5, 8)
    deck.deck[8] = Card(6,"Diamonds", 6, 9)
def compareCards(players):
    # print("\n--- DEBUG : compareCards begins ---")
    if len(players)>=1:
        playerWin = players[0]
        playerWin.setHandValues()
        for i in range(len(players)):
            if playerWin == player_list[i]:
                continue
            player_list[i].setHandValues()
            for j in range(len(players[0].getHandValues())):
                # print("DEBUG : "+playerWin.getName()+": "+str(playerWin.getHandValues()[j]))
                # print("DEBUG : "+players[i].getName()+": "+str(players[i].getHandValues()[j]))
                if playerWin.getHandCards()[j].getValue() > players[i].getHandCards()[j].getValue():
                    # print("DEBUG : PlayerWin stays")
                    break
                elif playerWin.getHandCards()[j].getValue() == players[i].getHandCards()[j].getValue():
                    pass
                else:
                    playerWin = player_list[i]
                    # print("DEBUG : PlayerWin changes to "+players[i].getName())
                    break
        # print("--- DEBUG : compareCards ends ---")
        return playerWin
def blinds():
    global big_blind
    big_blind = 5
    small_blind = 2
    print(f"{big_blind_player.getName()} throws {big_blind} gold into the pot.")
    big_blind_player.betMoney(big_blind)
    print(f"{player_list[player_list.index(big_blind_player)+1].getName()} throws {small_blind} gold into the pot.")
    player_list[player_list.index(big_blind_player)+1].betMoney(small_blind)
    global last_bet
    last_bet = big_blind
def startGameBets(is_blind_round):
    random.shuffle(player_list)
    global big_blind_player
    global last_bet
    global big_blind
    for player in player_list:
        player.setCurrentBet(0)
    if is_blind_round:
        big_blind_player = player_list[0]
        blinds()
    pass_count = 0
    turn_count = 0
    while(pass_count < len(player_list)):
        if is_blind_round and turn_count == 0:
            current_bet = big_blind
        elif not is_blind_round and turn_count == 0:
            current_bet = 0
        for player in player_list:
            if player == big_blind_player and turn_count == 0 and is_blind_round:
                # player.setHasBetBigBlind(True)
                # last_player = player
                continue
            os.system("cls")
            print(f"\n{player.getName()}, it is your turn to bet!")
            os.system("pause")
            os.system("cls")
            player.printHand()
            if not is_blind_round:
                table.printCards()
            print(f"\n{player.getName()}, you have {player.getMoney()} gold.")
            while True:
                try:
                    # for p in playerList:
                    #     print(f"{p.getName()} has bet {p.getBet()} gold")
                    print(f" --- DEBUG : Current Bet = {current_bet} ---")
                    if player.getMoney() == 0:
                        break
                    elif player.getCurrentBet() == current_bet or (not is_blind_round and player == player_list[0]):
                        print("Fold - Quit this game and lose your current bet.")
                        print("Call - Raise your bet to the current bet.")
                        print("Raise - Raise your bet and put more gold into the pot. Total gold has to be higher than the current bet.")
                        print("Pass - Pass your turn without raising your bet.")
                        turn_action = input(f"\nDo you want to fold, call, raise or pass? (F/C/R/P) -> ").lower()
                        last_betting_action = turn_action
                        if turn_action not in ["f", "c", "r", "p"]: raise ValueError
                        else: break
                    elif player.getBet() != current_bet or last_betting_action.lower() == 'p':
                        print("Fold - Quit this game and lose your current bet.")
                        print("Call - Raise your bet to the current bet.")
                        print("Raise - Raise your bet and put more gold into the pot. Total gold has to be higher than the current bet.")
                        turn_action = input(f"Do you want to fold, call or raise? (F/C/R) -> ").lower()
                        if turn_action not in ["f", "c", "r"]: raise ValueError
                        else: break
                    else: 
                        break
                except ValueError as e:
                    print("Not a legal action!")
            os.system("cls")
            match turn_action:
                case "f":
                    print(f"{player.getName()} folds!")
                    player_list.remove(player)
                case "c":
                    if player.getBet() == current_bet:
                        print(f"{player.getName()} passes.")
                        last_betting_action = "p"
                    else:
                        print(f"{player.getName()} calls the bet.")
                        # player.betMoney(last_bet - player.getBet())
                        if(current_bet > player.getBet()):
                            player.betMoney(current_bet - player.getBet())
                        print(f"{player.getName()} has {player.getMoney()} gold left.")
                        # print(f"--- DEBUG {player.getName()} has bet a total of {player.getBet()} gold. ---")
                    pass_count += 1
                case "r":
                    while True:
                        try:
                            raised_bet = int(input("How much gold do you want to throw in the pot? -> "))

                            # If player tries to raise to an amount less than the current bet, raise an error
                            if raised_bet + player.getBet() <= current_bet: raise ValueError

                            player.betMoney(raised_bet)
                            # print(f" --- DEBUG : Last Bet:{last_bet} \t Player Bet:{player.getBet()} --- ")
                            last_bet = player.getBet()
                            print(f"{player.getName()} raises the bet to {player.getBet()}!")
                            print(f"{player.getName()} has {player.getMoney()} gold left.")
                            pass_count = 0
                            current_bet = player.getBet()
                            break
                        except ValueError as e:
                            print("Raised bet has to be higher than the current bet!")
                case "p":
                    pass_count += 1
                    last_betting_action = "p"
                    print(f"{player.getName()} passes!")
            print(f"There is {pot.getMoney()} gold in the pot.")
            if split_pot.getMoney() >0:
                print(f"The split pot has {split_pot.getMoney()} gold!")
            # last_player = player
            if pass_count >= len(player_list):
                break
        # print(f"--- DEBUG Turn {turn_count} ends! ---")
        turn_count += 1
    os.system("pause")
    os.system("cls")
def main():
    global last_bet
    global pot
    global split_pot
    global deck 
    global all_in_value
    all_in_value = 0
    pot = Pot()
    split_pot = Pot()
    deck = Deck()
    for i in range(7): # shuffle deck 7 times
        deck.shuffle()
    # stackDeck2PSameCards()
    os.system("cls")
    global player_list
    player_list = []
    global playerCount
    while True: # ask for player count and raise error if wrong input
        try:
            playerCount = int(input("How many players? "))
            if playerCount > 5: raise ValueError
            break
        except ValueError as e:
            print("Enter a valid number!")
    for i in range(playerCount): # Create players according to player count
        Player()

    #Takes care of betting, also embedded in the turn loop
    startGameBets(True)

    # for player in playerList: # print every player's hand
    #     player.printHand()
    for player in player_list: # Let bards mulligan if they want
        if player.getPlayerClass() == "Bard":
            print(f"{player.getName()}'s turn.")
            os.system("pause")
            player.bardAbility()
    # os.system("pause")
    os.system("cls")
    global table
    table = Table()
    table.turnOne()
    print("\n")

    # Game ends and now scores are being calculated
    for player in player_list: # check every player's cards and print their final score
        values(player)
        player.printScore()
    #Sort players by score, highest first. Then check if players have the same score
    player_list.sort(key=Player.getScore, reverse=True)
    playersToCompare = []
    global playerWin
    playerWin = []
    playerWin.append(player_list[0])
    if len(player_list) > 1:
        if player_list[0].getScore() > player_list[1].getScore():
            pass
        else: # add players with equal score to a list that's compared later
            for i in range(playerCount-1):
                if player_list[i].getScore() == player_list[i+1].getScore():
                    if player_list[i] not in playersToCompare:
                        playersToCompare.append(player_list[i])
                    if player_list[i+1] not in playersToCompare:
                        playersToCompare.append(player_list[i+1])
                        # print(f"DEBUG : Added {playerList[i].getName()} to playersToCompare")
    # print(f"--- DEBUG : playersToCompare List ---")
    # for player in playersToCompare:
    #     print(player.getName())
    # print(f"--- DEBUG END ---")
    #If more than 2 players have the same score, check who has the highest value card
    #Compare highest card between 2 players, if they're the same, compare the next cards
    #If one card is higher than the other, compare the winning player with the next player
    if len(playersToCompare)>=2:
        playerWin[0] = compareCards(playersToCompare)
    else:
        playerWin[0] = player_list[0]
        for j in range(0, playerCount):
            if playerWin[0] == player_list[j]:
                continue
            if playerWin[0].getScore() < player_list[j].getScore():
                playerWin[0] = player_list[j]
                # print(f"--- DEBUG : {playerList[j].getName()} is new playerWin")
    for player in player_list: # compare every player's hand with winner's hand. If they have the same cards, add other player to winners
        if player == playerWin[0]:
            # print(f" --- DEBUG : Same Player! ---")
            continue
        # print(f" --- DEBUG : {playerWin[0].getName()} has {playerWin[0].getHandValues()} ---")
        # print(f" --- DEBUG : {player.getName()} has {player.getHandValues()} ---")
        if playerWin[0].getHandValues() == player.getHandValues() and playerWin[0].getScore() == player.getScore():
            # print(f" --- DEBUG : {player.getName()} added to winning players! ---")
            playerWin.append(player)
    print()
    pot.potToWinner()
    if split_pot.getMoney() > 0:
        split_pot.potToWinner()
    for player in player_list:
        if player in playerWin:
            print(f"Player {player.getName()} has won and has {player.getMoney()} gold.")
        else:
            print(f"Player {player.getName()} has {player.getMoney()} gold left.")
    # DEBUG ONLY
    # finalPlayerScores = []
    # for player in playerList:
    #    finalPlayerScores.append({"Winner": bool(player in playerWin), "Name": player.getName(), "Score": player.getScore(), "Class": player.getPlayerClass(), "Money Bet": player.getBet(),"Hand": player.getHandCSV()})
    # df = pd.DataFrame.from_records(finalPlayerScores)
    # df.to_csv("results.csv", index=False, mode="a", header=True)
    # with open("results.csv", "a") as file:
    #    file.write("\n")
    # DEBUG ONLY
    os.system("pause")

if __name__ == '__main__':
    main()
