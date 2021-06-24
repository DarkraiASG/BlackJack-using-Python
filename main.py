# To play a hand of Blackjack the following steps must be followed:

# Create a deck of 52 cards
# Shuffle the deck
# Ask the Player for their bet
# Make sure that the Player's bet does not exceed their available chips
# Deal two cards to the Dealer and two cards to the Player
# Show only one of the Dealer's cards, the other remains hidden
# Show both of the Player's cards
# Ask the Player if they wish to Hit, and take another card
# If the Player's hand doesn't Bust (go over 21), ask if they'd like to Hit again.
# If a Player Stands, play the Dealer's hand. The dealer will always Hit until the Dealer's value meets or exceeds 17
# Determine the winner and adjust the Player's chips accordingly
# Ask the Player if they'd like to play again

''' A standard deck of playing cards has four suits (Hearts, Diamonds, Spades and Clubs) and thirteen ranks (2 through 10, then the face cards Jack, Queen, King and Ace) for a total of 52 cards per deck.
Jacks, Queens and Kings all have a rank of 10. Aces have a rank of either 11 or 1 as needed to reach 21 without busting  '''


# Step 1: Import the random module. This will be used to shuffle the deck prior to dealing.
# Then, declare variables to store suits, ranks and values.
# Finally, declare a Boolean value to be used to control while loops.

import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven':7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10,
         'Queen': 10, 'King': 10, 'Ace': 11}

playing = True

# Step 2: Create a card class where each object has suit and rank --------------------------------------------------------------------------------------------------------------------------


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    # string method inside class to print a Card, returns a string in the form "Two of Hearts"
    def __str__(self):
        return self.rank + " of " + self.suit


# Step 3: deck class to store 52 cards --------------------------------------------------------------------------------------------------------------------------

class Deck:

    def __init__(self):
        self.deck = [] # an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank)) # build Card objects and add them to the list


    def __str__(self):
        deck_comp = ' ' # an empty string
        for card in self.deck:
            deck_comp = deck_comp + '\n' + card.__str__() # adding each card object's print string
        return "The deck has : " + deck_comp

    # shuffling of cards
    def shuffle(self):
        random.shuffle(self.deck)

    # picking one card at a time during HIT
    def deal(self):
        single_card = self.deck.pop()
        return single_card


#Step 4: creating hand class to calculate value of cards from deck using values of dictionary

class Hand:
    def __init__(self):
        self.cards = []  # an empty list
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]

    # If a hand's value exceeds 21 but it contains an Ace,
    # we can reduce the Ace's value from 11 to 1 and continue playing.
    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


# Step 5: Create a betting chips class

class Chips:
    def __init__(self):
        self.total = 100 # This can be set to a default value or supplied by a user input
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet

# Step 6: Function definitions

# function for betting chips
def take_bet(chips):
    while (True):
        try:
            chips.bet = int(input("How many chips would you like to bet ? : "))
        except ValueError:
            print("Sorry, a bet must be an integer !")
        else:
            if chips.bet > chips.total:
                print(f"Sorry, your bet can't exceed {chips.total}")
            else:
                break


# function for HIT

def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

def hit_or_stand(deck, hand):
    global playing

    while (playing == True):
        x = input("Would you like to Hit or Stand ? Enter 'h' or 's' : ")

        if x[0].lower() == 'h':
            hit(deck,hand)
        elif x[0].lower() == 's':
            print("Player Stands. Dealer is playing...")
            playing = False
        else:
            print("Sorry, please try again")
            continue
        break


# function to display cards
def show_some(player,dealer):
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('', dealer.cards[1])
    print("\nPlayer's Hand:", *player.cards, sep='\n ')

def show_all(player, dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand =", dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =", player.value)


# functions on end game scenarios
def player_busts(player,dealer,chips):
    print("Player Busts !")
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print("Player Wins !")
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print("Dealer Busts !")
    chips.win_bet()

def dealer_wins(player, dealer, chips):
    print("Deale Wins !")
    chips.lose_bet()

def push(player,dealer):
    print("Dealer and Player Tie ! It's a Push...")


while True:
    print('Welcome to BlackJack! Get as close to 21 as you can without going over!\n\
      Dealer hits until it reaches 17. Aces count as 1 or 11.')

    # create and shuffle the deck
    deck = Deck()
    deck.shuffle()

    # Two cards to player
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    # Two cards to dealer
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # Player's Chips
    player_chips = Chips() # default value is 100

    #prompt the player for their bet
    take_bet(player_chips)

    # show cards(but keep one dealer card hidden)
    show_some(player_hand, dealer_hand)

    while playing:
        # Prompt for Player to Hit or Stand
        hit_or_stand(deck, player_hand)

         # Show cards (but keep one dealer card hidden)
        show_some(player_hand,dealer_hand)

        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
            break


    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if player_hand.value <= 21:

        while dealer_hand.value < 17:
            hit(deck,dealer_hand)

        # show all cards
        show_all(player_hand, dealer_hand)

        # Run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)

        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)

        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)

        else:
            push(player_hand,dealer_hand)


    # inform player of their total chips
    print(f" \n Player's winnings stand at {player_chips.total}")

    #ask to play again
    new_game = input("Would you like to play another hand ? Enter 'y' or 'n' : ")

    if new_game[0].lower() == 'y':
        playing = True
        continue
    else:
        print("Thanks for Playing")
        break




