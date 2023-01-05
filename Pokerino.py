import random
import os

suits = ["Hearts", "Diamonds", "Spades", "Clubs"]
cardDisplay = [2,3,4,5,6,7,8,9,10,'J','Q','K','A']
cardValues = [2,3,4,5,6,7,8,9,10,11,12,13,14]

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
        
class Deck:
    deck = []
    def __init__(self):
        for suit in suits:
            for value in cardValues:
                self.deck.append(Card(value, suit, cardDisplay[cardValues.index(value)]))
    def shuffle(self):
        random.shuffle(self.deck)

class Table:
    def __init__(self, amountCards):
        self.listTableCards = []
        for card in range(amountCards):
            self.listTableCards.append(deck.deck.pop(0))
        self.printCards()

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

class Player:
    def __init__(self):
        self.name = input("Enter Player Name: ")
        print("What class are you?\n(w)arrior - Can destroy on card on the table\n(m)age - Can change the values of up to 2 cards by 1")
        self.ability = input("(t)hief - Can trade one card from their hand with one card on the table\n")
        playerList.append(self)
        self.handsize=2
        self.handCards = []
        self.pairs = []
        self.triples = []
        self.quads = []
        self.pentas = []
        self.hexas = []
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

    def activateAbility(self):
        while(self.abilityCount > 0):
            choice = input(f"\n{self.name.capitalize()}, do you want to activate an ability? - ")
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
                case 'n':
                    return False

    def addScore(self, x):
        self.score += x

    def getScore(self):
        print(f"{self.getName()}: {self.score} points\n")

    def printHand(self):
        print(f"--- {self.getName()}'s Hand ({self.playerClass})---")
        for card in self.handCards:
            print(card)
        print()
    
def nextTurnWithDraw():
    print("\n\n")
    os.system("pause")
    os.system("cls")
    for player in playerList:
        player.printHand()
    table.revealCard()
    if len(table.listTableCards) < 5:
        if(playerList[0].activateAbility()):
            nextTurnNoDraw()
        else:
            nextTurnWithDraw()

def nextTurnNoDraw():
    print("\n\n")
    os.system("pause")
    os.system("cls")
    for player in playerList:
        player.printHand() 
    table.printCards()
    if len(table.listTableCards) < 5:
            if(playerList[0].activateAbility()):
                nextTurnNoDraw()
            else:
                nextTurnWithDraw()
    else:
        pass

def checkStraight(player):
    count=0
    straightCards = []
    hasStraight=False
    for i in range(0,len(player.handCards)-1):
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
        if straightCards[0].getValue() == 14:
            return "Royal Straight"
        else:
            return "Straight"
    
def checkFlush(player):
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
        # print(f"{player.getName()} has a Flush of Diamonds!")
        hasFlush = True
    elif heartCount >= 5:
        # print(f"{player.getName()} has a Flush of Hearts!")
        hasFlush = True
    elif spadeCount >= 5:
        # print(f"{player.getName()} has a Flush of Spades!")
        hasFlush = True
    elif clubCount >= 5:
        # print(f"{player.getName()} has a Flush of Clubs!")
        hasFlush = True
    return hasFlush

def checkMultiples(player):
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
                print(f"{player.getName()} has 6 of {cardDisplay[cardValues.index(card)]}")
                player.addScore(100)
        elif pentaCardValues:
            for card in pentaCardValues:
                print(f"{player.getName()} has 5 of {cardDisplay[cardValues.index(card)]}")
                player.addScore(50)
        elif quadCardValues:
            for card in quadCardValues:
                print(f"{player.getName()} has 4 of {cardDisplay[cardValues.index(card)]}")
                player.addScore(20)
        elif tripleCardValues:
            for card in tripleCardValues:
                print(f"{player.getName()} has 3 of {cardDisplay[cardValues.index(card)]}")
                player.addScore(7)
        elif doubleCardValues:
            for card in doubleCardValues:
                print(f"{player.getName()} has 2 of {cardDisplay[cardValues.index(card)]}")
                player.addScore(2)
    return hasMultiples

def highestCard(player):
    player.addScore(1)
    print(f"{player.getName()}'s highest card is {cardDisplay[cardValues.index(player.handCards[0].getValue())]}")

def values(player):
    #Karten vom Tisch zu Händen hinzufügen
    for card in table.listTableCards:
        player.handCards.append(card)
    def getCardValue(card):
        return card.getValue()
    player.handCards.sort(key=getCardValue, reverse=True)
    while True:
        if checkStraight(player) == "Straight":
            if checkFlush(player):
                player.addScore(30)
                print(f"{player.getName()} has a Straight Flush!")
                break
            else:
                player.addScore(10)
                print(f"{player.getName()} has a Straight!")
            break
        elif checkStraight(player) == "Royal Straight":
            if checkFlush(player):
                player.addScore(40)
                print(f"{player.getName()} has a ROYAL FLUSH!!!") #FIX PLEASE FIX PLEASE FIX PLEASE FIX PLEASE FIX PLEASE FIX PLEASE
                break
            else:
                player.addScore(10)
                print(f"{player.getName()} has a Straight!")
                break
        elif checkFlush(player):
            player.addScore(12)
            print(f"{player.getName()} has a Flush!")
            break
        elif checkMultiples(player):
            break
        else: 
            highestCard(player)
            break

def stackDeck():
    deck.deck[0] = Card(10,"Diamonds", 10)
    deck.deck[1] = Card(13,"Spades", 'K')
    deck.deck[2] = Card(11,"Clubs", 'J')
    deck.deck[3] = Card(11,"Diamonds", 'J')
    deck.deck[4] = Card(10,"Diamonds", 10)

deck = Deck()
deck.shuffle()
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
table = Table(2)
nextTurnWithDraw()
print("\n")
for player in playerList:
    values(player)
    player.getScore()
os.system("pause")
