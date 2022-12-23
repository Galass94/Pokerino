import random
import os

suits = ["Hearts", "Diamonds", "Spades", "Clubs"]
cardValues = [2,3,4,5,6,7,8,9,10,'J','Q','K','A']

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        self.display = value
        self.winners = {"Pair": False, "Triple": False, "Quad": False}

    def getValue(self):
        return self.value
    def setValue(self, x):
        self.value = x

    def getDisplay(self):
        return self.display

    def __str__(self):
        return f"{self.value:>2} of {self.suit}"
        
class Deck:
    deck = []
    def __init__(self):
        for suit in suits:
            for value in cardValues:
                self.deck.append(Card(value, suit))
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
    def __init__(self, name, ability):
        playerList.append(self)
        self.name = name
        self.ability = ability
        self.handsize=2
        self.handCards = []
        self.score=0
        if self.ability == "w":
            self.abilityCount = 1
        elif self.ability == "m":
            self.abilityCount = 2
        elif self.ability == "t":
            self.abilityCount = 1
        for card in range(self.handsize):
            self.handCards.append(deck.deck.pop(0))
        print(f"{self.name} joins the table!")

    def warriorAbility(self):
        print("You activated your ability to remove one card from the table")
        choice2 = int(input("Which one do you want to remove? - "))
        table.listTableCards.pop(choice2-1)

    def mageAbility(self):
        print("You activated your ability to change the value of one card on the table!")
        choice2 = int(input("Which card would you like to change?  "))
        choice3 = input("Would you like to increase(+) or decrease(-) the card's value?  ")
        if choice3=='+':
            table.listTableCards[choice2-1].value = cardValues[cardValues.index(table.listTableCards[choice2-1].value)+1]
        elif '-':
            table.listTableCards[choice2-1].value = cardValues[cardValues.index(table.listTableCards[choice2-1].value)-1]
    
    def thiefAbility(self):
        print("You activated your ability to switch one card from the table with one from your hand!")
        choiceT = int(input("Which card from the table would you like to take? "))
        choiceT2 = int(input("Which card frmo your hand do you want to put on the table? "))
        self.handCards.append(table.listTableCards.pop(choiceT-1))
        table.listTableCards.append(self.handCards.pop(choiceT2-1))

    def activateAbility(self):
        while(self.abilityCount > 0):
            choice = input("\nDo you want to activate an ability? - ")
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

    def printHand(self):
        print(f"--- {self.name}'s Hand ---")
        # for index in range(0,2):
        #     print(self.handCards[index])
        for card in self.handCards:
            print(card)
    
def nextTurnWithDraw():
    print("\n\n")
    os.system("pause")
    os.system("cls")
    player1.printHand()
    print()
    table.revealCard()
    if len(table.listTableCards) < 5:
        if(player1.activateAbility()):
            nextTurnNoDraw()
        else:
            nextTurnWithDraw()

def nextTurnNoDraw():
    print("\n\n")
    os.system("pause")
    os.system("cls")
    player1.printHand()
    print()
    table.printCards()
    if len(table.listTableCards) < 5:
        if(player1.activateAbility()):
            nextTurnNoDraw()
        else:
            nextTurnWithDraw()
    else: player1.activateAbility()

def values(player):
    #Karten vom Tisch zu Händen hinzufügen
    for card in table.listTableCards:
        for player in playerList:
            player.handCards.append(card)
    playerCardValues = []
    #Face Cards in Zahlen umwandeln
    for card in player.handCards:
        if card.getValue() != 'J' and card.getValue() != 'Q' and card.getValue() != 'K' and card.getValue() != 'A':
            playerCardValues.append(card.getValue())
        elif card.getValue() == 'J':
            card.setValue(11)
            playerCardValues.append(11)
        elif card.getValue() == 'Q':
            card.setValue(12)
            playerCardValues.append(12)
        elif card.getValue() == 'K':
            card.setValue(13)
            playerCardValues.append(13)
        elif card.getValue() == 'A':
            card.setValue(14)
            playerCardValues.append(14)
    #Hände absteigend nach Wert sortieren
    playerCardValues.sort(reverse=True)
    for value in playerCardValues:
        print(value)
    playerCardSame = [0,0,0,0,0,0,0,0,0,0,0,0,0]
    #Werte in Hand zählen
    for value in playerCardValues:
        playerCardSame[value-2] += 1
    #Werte Doppelte, Dreifache und Vierfache von Hand ausgeben
    offset=0
    for value in playerCardSame:
        if value==4:
            print(f"Quad of {playerCardSame.index(value)+2-offset}s")
            playerCardSame.pop(playerCardSame.index(value))
            offset+=1
        elif value==3:
            print(f"Triple of {playerCardSame.index(value)+2-offset}s")
            playerCardSame.pop(playerCardSame.index(value))
            offset+=1
        elif value==2:
            print(f"Pair of {playerCardSame.index(value)+2-offset}s")
            playerCardSame.pop(playerCardSame.index(value))
            offset+=1
    # for card in player.handCards:
    #     if value==4:
    #         print(f"Quad of {playerCardSame.index(value)+2-offset}s")
    #         playerCardSame.pop(playerCardSame.index(value))
    #         offset+=1
    #     elif value==3:
    #         print(f"Triple of {playerCardSame.index(value)+2-offset}s")
    #         playerCardSame.pop(playerCardSame.index(value))
    #         offset+=1
    #     elif value==2:
    #         print(f"Pair of {playerCardSame.index(value)+2-offset}s")
    #         playerCardSame.pop(playerCardSame.index(value))
    #         offset+=1
    if playerCardValues.__len__>=12: print(f"Höchste Karte : {playerCardValues[0]}")

def compareCard(card, cardValues):
    pass

deck = Deck()
deck.shuffle()
os.system("cls")
name = input("Enter Player Name: ")
print("What class are you?\n(w)arrior - Can destroy on card on the table\n(m)age - Can change the values of up to 2 cards by 1")
playerClass = input("(t)hief - Can trade one card from their hand with one card on the table\n")
playerList = []
print()
player1 = Player(name, playerClass)
#print("--- Player 1 Hand ---")
player1.printHand()
table = Table(2)
nextTurnWithDraw()
print("\n\n")
for player in playerList:
    values(player)