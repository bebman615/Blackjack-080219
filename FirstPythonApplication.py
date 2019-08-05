from random import shuffle
import TestInheritance

class Game:

    def __init__(self):
        self.gameDeck = deck()
        self.players = self.GetPlayerList()
        self.nonDealerPlayerList = self.players[:len(self.players) - 1]
        self.nonDealerPlayers = len(self.players) - 1

    def GetPlayerList(self):
        playerCount = InputValidation(input("Please enter the number of players. \n")).ValidNumPlayers()
        playerList = [player(input("Please enter a player name. \n")) for x in range(0,playerCount)]
        playerList.append(dealer("Dealer"))
        return playerList

    def RunGame(self):
        self.InitializeGame()
        self.CheckPlayerHands()

    def InitializeGame(self):
        print("___________________________ \n")
        print(" Current Chip Stacks: \n {} \n {} \n___________________________ \n".format(" || ".join([player.name for player in self.nonDealerPlayerList]),
        " || ".join([str(player.chipStack) + (" " * (len(player.name) - len(str(player.chipStack))))  for player in self.nonDealerPlayerList])))

        for player in self.players:
            player.currentBet = player.AskBet()
        print("___________________________ \n")
        for player in self.players:
            player.hand.HitCard(self.gameDeck, 2)
            player.CheckProgress()

    def CheckPlayerHands(self):
        
        for player in self.players:
            if self.nonDealerPlayers != 0:
                if player.CheckHand(self.gameDeck):
                    self.nonDealerPlayers -= 1

class InputValidation:

    def __init__(self, outputValue):
        self.outputValue = outputValue

    def IntegerValidation(self):
        while True:
            try:
                return int(self.outputValue)
            except ValueError:
                self.outputValue = input("You did not enter a valid number, please try again. \n")
    
    def ValidNumPlayers(self):
        maxNumber = 5
        while True:
            self.outputValue = self.IntegerValidation()
            if self.outputValue < 1 or self.outputValue > maxNumber:
                self.outputValue = input("Please enter a valid number between 1 and 5. \n")
            else:
                return self.outputValue
    
    def MaxBetValidation(self, playerChips):
        self.outputValue = self.IntegerValidation()
        return min(self.outputValue, playerChips)

    def HitStayValidation(self):
        while True:
            self.outputValue = self.outputValue.upper()
            validInput = (self.outputValue == "HIT" or self.outputValue == "STAY")
            if validInput:
                return self.outputValue
            else:
                self.outputValue = input("Please enter either hit or stay \n").upper()
        
    def ChangeAceValidation(self):
        while True:
            validInput = (self.outputValue == "11" or self.outputValue == "1")
            if validInput:
                return self.outputValue  
            else:
                self.outputValue = input("Please enter either 11 or 1 \n")


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
        self.chipStack = 500
        self.currentBet = 0

    def AskBet(self):
        return InputValidation(input("{}, how much would you like to bet? \n".format(self.name))).MaxBetValidation(self.chipStack)

    def CheckBust(self, gameDeck):
        return self.hand.handValue > 21

    def CheckProgress(self):
        print(self.name + ": " + ",".join([card.image for card in self.hand.cards]) + " || HandValue: " + str(self.hand.handValue) +
              " || CurrentBet: " + str(self.currentBet))

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
        self.secondCardUp = False

    def AskBet(self):
        return 0

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

    def CheckProgress(self):
        if not self.secondCardUp:
            print(self.name + ": " + self.hand.cards[0].image + "[]")
            self.secondCardUp = True
        else:
            print(self.name + ": " + ",".join([card.image for card in self.hand.cards]) + " || HandValue: " + str(self.hand.handValue))

class Card:

    def __init__(self, image, value):
        self.image = image
        self.value = value
        self.IsAce = self.image[0] == 'A'

                

#na = TestInheritance.TestFunction().testFunction1()
NewGame = Game()
NewGame.RunGame()