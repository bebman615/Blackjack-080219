from random import shuffle
import TestInheritance

class Game:

    def __init__(self):
        self.gameDeck = deck()
        self.players = self.GetPlayerList()
        self.nonDealerPlayers = len(self.players) - 1

    def GetPlayerList(self):
        enterInputString = "Please enter the number of players. \n" 
        playerCount = input(enterInputString)
        verifyInput = InputValidation(playerCount)
        while verifyInput.ValidNumPlayers() == False:
            verifyInput.outputValue = input(enterInputString)
        playerList = [player(input("Please enter a player name. \n")) for x in range(0,verifyInput.outputValue)]
        playerList.insert(len(playerList), dealer("Dealer"))
        return playerList

    def RunGame(self):
        self.InitializeGame()
        self.CheckPlayerHands()

    def InitializeGame(self):
        print("___________________________ \n")
        for player in self.players:
            player.hand.HitCard(self.gameDeck, 2)
            player.CheckProgress()

    def CheckPlayerHands(self):
        
        ## Fix this fucking thing first thing in the morning!!
        for player in self.players:
            if self.nonDealerPlayers != 0:
                if player.CheckHand(self.gameDeck):
                    self.nonDealerPlayers -= 1

class InputValidation:

    def __init__(self, outputValue):
        self.outputValue = outputValue

    def IntegerValidation(self):
        try:
           self.outputValue = int(self.outputValue)
        except ValueError:
           print("You did not enter a valid number, please try again.")
           self.outputValue = 0
    
    def ValidNumPlayers(self):
        validCount = True
        maxNumber = 5
        self.IntegerValidation()
        if self.outputValue < 1 or self.outputValue > 5 :
            print("Please enter a valid number between 1 and 5.")
            validCount = False
        return validCount

    def HitStayValidation(self):
        validInput = False
        while not validInput:
            self.outputValue = self.outputValue.upper()
            validInput = (self.outputValue == "HIT" or self.outputValue == "STAY")
            if not validInput:
                self.outputValue = input("Please enter either hit or stay \n").upper()
        return self.outputValue
    
    def ChangeAceValidation(self):
        validInput = False
        while not validInput:
            self.outputValue = self.outputValue.upper()
            validInput = (self.outputValue == "11" or self.outputValue == "1")
            if not validInput:
                self.outputValue = input("Please enter either 11 or 1 \n").upper()
        return self.outputValue  


class deck:
    
    def __init__(self):
        self.cards = self.CreateDeck()
    
    def CreateDeck(self):
        suitSymbols = ['♠', '♦', '♥', '♣']
        cardValues = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}
        finalCards = [Card(x + y, cardValues[x]) for x in cardValues for y in suitSymbols]
        shuffle(finalCards)
        return finalCards

    def DrawCard(self):
        return self.cards.pop(0)

    def GetCardValues(self, listOfCards, checkAce=False):
        return sum([int(InputValidation(input('Would you like the value of {} to be 11 or 1?'.format(card.image))).ChangeAceValidation()) if 
                    (card.IsAce and checkAce) else card.value for card in listOfCards])

class player:
    
    def __init__(self, playerName):
        self.name = playerName
        self.bust = False
        self.hand = hand()

    def CheckBust(self, gameDeck):
        return self.hand.handValue > 21

    def CheckProgress(self):
        print(self.name + ": " + ",".join([card.image for card in self.hand.cards]) + " || HandValue: " + str(self.hand.handValue))

     ##   need to get rid of the ace checking
    def CheckHand(self, gameDeck):
        print("___________________________ \n")
        hitString = self.name + ", Would you like to hit/stay? \n"
        playerOption = InputValidation(input(hitString)).HitStayValidation()
        while playerOption == "HIT":
            self.hand.HitCard(gameDeck, 1, True)
            self.CheckProgress()
            if self.CheckBust(gameDeck):
                playerOption = "BUST"
                print(self.name + ", You have busted!")
                self.bust = True
            else:
                playerOption = InputValidation(input(hitString)).HitStayValidation()
        return self.bust
                
class hand:
   
    def __init__(self):
        self.cards = []
        self.numberOfAces = len([x for x in self.cards if x[1] == 'A'])
        self.handValue = 0

    def HitCard(self, deck, numCards, checkAce=False):
        for counter in range(numCards):
            self.cards.append(deck.DrawCard())
        self.handValue = deck.GetCardValues(self.cards, checkAce)

class dealer(player):
    
    def __init__(self, playerName):
        player.__init__(self, playerName)

    def CheckStay(self):
        MinStayValue = 17
        return (self.hand.handValue >= MinStayValue)

    def CheckHand(self, gameDeck):
        print("___________________________ \n")
        checkStay = self.CheckStay()
        self.CheckProgress()
        while not checkStay:
            self.hand.HitCard(gameDeck, 1, True)
            self.CheckProgress()
            checkStay = self.CheckStay()
            checkBust = self.CheckBust(gameDeck)
            if checkBust:
                print(self.name + ", You have busted!")
                self.bust = True

class Card:

    def __init__(self, image, value):
        self.image = image
        self.value = value
        self.IsAce = self.image[0] == 'A'

                

#na = TestInheritance.TestFunction().testFunction1()
NewGame = Game()
NewGame.RunGame()