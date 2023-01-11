import random
import os

suits = ["Hearts", "Diamonds", "Spades", "Clubs"]
cardDisplay = [2,3,4,5,6,7,8,9,10,'J','Q','K','A']
cardValues = [2,3,4,5,6,7,8,9,10,11,12,13,14]
playerClasses = ["w", "m", "t", "d","b", "r"]

class Card:
    def __init__(self, value, suit, display):
        self.value = value
        self.suit = suit
        self.display = display
        self.winners = {"Pair": False, "Triple": False, "Quad": False, "Penta":False, "Hexa":False}

    def getValue(self):
        return self.value
    def setValue(self, x):
        self.value = x
    def getSuit(self):
        return self.suit
    def getDisplay(self):
        return self.display
    def setDisplay(self, display):
        self.display = display

    def __str__(self):
        return f"{cardDisplay[cardValues.index(self.value)]:>2} of {self.suit}"
    def __eq__(self, other):
        if isinstance(other, Card):
            return self.value == other.value and self.suit == other.suit
        return False
class Deck:
    deck = []
    def __init__(self):
        for suit in suits:
            for value in cardValues:
                self.deck.append(Card(value, suit, cardDisplay[cardValues.index(value)]))
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

    def removeCard(self, index):
        self.listTableCards.pop(index)

    def turnOne(self):
        for player in playerList:
            player.printHand()
        for i in range(0,3):
            self.listTableCards.append(deck.deck.pop(0))
        self.printCards()
        if len(self.listTableCards) < 5:
            if(playerList[0].activateAbility()):
                nextTurn(False)
            else:
                nextTurn(True)
class Player:
    def __init__(self):
        self.name = input("Enter Player Name: ")
        while True:
            try:
                print(f"What class are you, {self.getName()}?\n(W)arrior - Can destroy on card on the table\n(M)age - Can change the values of up to 2 cards by 1")
                print("(T)hief - Can trade one card from their hand with one card on the table\n(D)eprived - BONK")
                print("(R)andom - Get a random ability\n(B)ard - Gets 1 Mulligan")
                self.ability = input().lower()
                if self.ability not in playerClasses: raise ValueError
                break
            except ValueError as e:
                print("Please choose a class!")
                os.system("pause")
                os.system("cls")
        playerList.append(self)
        self.handsize=2
        self.money=100
        self.handCards = []
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
        if self.ability == "w":
            self.playerClass = "Warrior"
            self.abilityCount = 1
        elif self.ability == "m":
            self.playerClass = "Mage"
            self.abilityCount = 2
        elif self.ability == "t":
            self.playerClass = "Thief"
            self.abilityCount = 1
        elif self.ability == "d":
            self.playerClass = "Deprived"
            self.abilityCount = 3
        elif self.ability == "b":
            self.playerClass = "Bard"
            self.abilityCount = 1
        elif self.ability == "r":
            self.playerClass = "Random"
            self.abilityCount = 2
        for card in range(self.handsize):
            self.handCards.append(deck.deck.pop(0))
        print(f"{self.getName()} joins the table!")
        os.system("pause")
        os.system("cls")

    def getName(self):
        return self.name.capitalize()

    def warriorAbility(self):
        print("You activated your ability to remove one card from the table")
        while True:
            try:
                choice2 = int(input("Which one do you want to remove? - "))
                if choice2 > len(table.listTableCards): raise ValueError
                break
            except ValueError as e:
                print("Enter a valid number!")
        table.listTableCards.pop(choice2-1)
    def mageAbility(self):
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
                table.listTableCards[choice2-1].setValue(cardValues[cardValues.index(table.listTableCards[choice2-1].value)+1])
        elif '-':
            if table.listTableCards[choice2-1].getValue() == 2:
                table.listTableCards[choice2-1].setValue(14)
            else:
                table.listTableCards[choice2-1].setValue(cardValues[cardValues.index(table.listTableCards[choice2-1].value)-1])
    def thiefAbility(self):
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
    def deprivedAbility(self):
        temp = random.randint(0, 99)
        if temp <= 4:
            print(f"{playerList[random.randint(0,len(playerList)-1)].getName()} got BONKed!!!")
        else :
            print("BONK!")
    def bardAbility(self):
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
    def randomAbility(self):
        temp = random.randint(0, len(playerClasses)-2)
        match temp:
            case 0:
                print("WARRIOR ABILITY") 
                self.warriorAbility()
            case 1: 
                print("MAGE ABILITY") 
                self.mageAbility()
            case 2: 
                print("THIEF ABILITY") 
                self.thiefAbility()
            case 3: 
                print("DEPRIVED ABILITY") 
                self.deprivedAbility()
            case 4:
                print("BARD ABILITY")
                self.bardAbility()
        pass
    def activateAbility(self):
        while self.abilityCount > 0:
            choice = input(f"\n{self.getName()}, do you want to activate an ability? - ")
            match(choice):
                case 'y':
                    self.abilityCount -= 1
                    if self.ability == "w":
                        self.warriorAbility()
                        return True
                    elif self.ability == "m":
                        self.mageAbility()
                        return True
                    elif self.ability == "t":
                        self.thiefAbility()
                        return True
                    elif self.ability == "d":
                        self.deprivedAbility()
                        return True
                    elif self.ability == "r":
                        self.randomAbility()
                        return True
                case 'n':
                    return False
    def getAbility(self):
        return self.ability
    def addScore(self, x):
        self.score += x
    def getScore(self):
        return self.score
    def printScore(self):
        print(f"{self.getName()}: {self.score} points")
    def printHand(self):
        print(f"--- {self.getName()}'s Hand ({self.playerClass})---")
        for card in self.handCards:
            print(card)
        print()
    def addMoney(self, x):
        if x > self.money:
            self.money = 0
        else: self.money += x
    def setHandValues(self):
        self.handValues = []
        for card in self.handCards:
            self.handValues.append(card.getValue())
    def getHandValues(self):
        return self.handValues
    def setgetHandValues(self):
        self.handValues = []
        for card in self.handCards:
            self.handValues.append(card.getValue())
            return self.handValues
    def getHandCards(self):
        return self.handCards
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
def nextTurn(draw):
    print("\n\n")
    os.system("pause")
    os.system("cls")
    for player in playerList:
        player.printHand()
    if draw:
        table.revealCard()
    else:
        table.printCards()
    if len(table.listTableCards) < 5:
        if(playerList[0].activateAbility()):
            nextTurn(False)
        else:
            nextTurn(True)
    else: pass
def checkRoyalFlush(player):
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
def checkStraight(player):
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
def checkFlush(player):     # Check if player has Flush and if they do, return the suit of the flush
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
def checkMultiples(player): # Check if player has multiples of a value and if they do, return the highest multiple
    for card in player.handCards:
        card.winners["Pair"] = False
        card.winners["Triple"] = False
        card.winners["Quad"] = False
        card.winners["Penta"] = False
        card.winners["Hexa"] = False
        count = 0
        hasMultiples = False
        for cardToComp in player.handCards:
            if card.getValue() == cardToComp.getValue():
                count += 1
                if count==6:
                    card.winners["Hexa"] = True
                elif count==5:
                    card.winners["Penta"] = True
                elif count==4:
                    card.winners["Quad"] = True
                elif count == 3:
                    card.winners["Triple"] = True
                elif count == 2:
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
        if triple == 1 and double == 1 :
            hasFullHouse = True
    if hasFullHouse:
        player.addScore(15)
        print(f"{player.getName()} has a Full House!")
    else:
        if hexaCardValues:
            for card in hexaCardValues:
                print(f"{player.getName()} has 6 {cardDisplay[cardValues.index(card)]}s")
                player.addScore(100)
        elif pentaCardValues:
            for card in pentaCardValues:
                print(f"{player.getName()} has 5 {cardDisplay[cardValues.index(card)]}s")
                player.addScore(50)
        elif quadCardValues:
            for card in quadCardValues:
                print(f"{player.getName()} has 4 {cardDisplay[cardValues.index(card)]}s")
                player.addScore(20)
        elif tripleCardValues:
            for card in tripleCardValues:
                print(f"{player.getName()} has 3 {cardDisplay[cardValues.index(card)]}s")
                player.addScore(7)
        elif doubleCardValues:
            for card in doubleCardValues:
                print(f"{player.getName()} has a pair of {cardDisplay[cardValues.index(card)]}s")
                player.addScore(2)
    return hasMultiples
def highestCard(player):    # If player has nothing else, output the highest card in their Hand
    player.addScore(1)
    print(f"{player.getName()}'s highest card is {cardDisplay[cardValues.index(player.handCards[0].getValue())]}")
    player.setHighestCard(player.getHandCards()[0])
def values(player):
    #Karten vom Tisch zu Händen hinzufügen
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
def stackDeck():
    deck.deck[0] = Card(2,"Diamonds", 2)
    deck.deck[1] = Card(3,"Diamonds", 3)
    deck.deck[2] = Card(4,"Diamonds", 4)
    deck.deck[3] = Card(5,"Diamonds", 5)
    deck.deck[4] = Card(6,"Diamonds", 6)
    deck.deck[5] = Card(4, "Spades", 4)
def compareCards(players):
    if len(players)>=1:
        playerWin = players[0]
        for i in range(len(players)-1):
            if playerWin == playerList[i]:
                continue
            for j in range(7):
                # print("\nDEBUG : "+playerWin.getName()+": "+str(playerWin.getHandCards()[j]))
                # print("DEBUG : "+players[i].getName()+": "+str(players[i].getHandCards()[j]))
                if playerWin.getHandCards()[j].getValue() > players[i].getHandCards()[j].getValue():
                    # print("DEBUG : PlayerWin stays")
                    break
                elif playerWin.getHandCards()[j].getValue() == players[i].getHandCards()[j].getValue():
                    pass
                else:
                    playerWin = playerList[i]
                    # print("DEBUG : PlayerWin changes to "+players[i].getName())
                    break
        return playerWin

deck = Deck()
for i in range(7):
    deck.shuffle()
# stackDeck()
os.system("cls")
playerList = []
while True:
    try:
        playerCount = int(input("How many players? "))
        if playerCount > 5: raise ValueError
        break
    except ValueError as e:
        print("Enter a valid number!")
for i in range(playerCount):
    Player()
for player in playerList:
    player.printHand()
#TODO: Implement betting system
for player in playerList:
    if player.getAbility().lower() == "b":
        player.bardAbility()
os.system("pause")
os.system("cls")
table = Table()
table.turnOne()
print("\n")
for player in playerList:
    values(player)
    player.printScore()
    # print("Highest card: " + str(player.getHandCards()[0])+"\n")
#Check who has highest card
#Compare highest card between 2 players, if they're the same, compare the next cards
#If one card is higher than the other, compare the winning player with the next player
playerList.sort(key=Player.getScore, reverse=True)
for player in playerList:
    print(player.getName())
playersToCompare = []
playerWin = playerList[0]
for i in range(playerCount-1):
    if playerList[i].getScore() == playerList[i+1].getScore():
        if playerList[i] not in playersToCompare:
            playersToCompare.append(playerList[i])
        else: continue
if len(playersToCompare)>=2:
    playerWin = compareCards(playersToCompare)
else:
    playerWin = playerList[0]
    for j in range(0, playerCount):
        if playerWin.getScore() > playerList[j].getScore():
            playerWin = playerList[j]
        elif playerWin.getScore() == playerList[j].getScore():
            pass
        else:
            playerWin = playerList[j]
print("Winner is: "+ playerWin.getName())
os.system("pause")
