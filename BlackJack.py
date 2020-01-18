import random

class Card():
    
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Deck():

    def __init__(self):
        self.cards = []
        self.suit = ('Hearts','Diamonds','Spades','Clubs')
        self.rank = ('2','3','4','5','6','7','8','9','10','Jack','Queen','King','Ace')
        self.value = {'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'Jack':10,'Queen':10,'King':10,'Ace':11}
        
        for suit in self.suit:
            for rank in self.rank:
                self.cards.append(Card(suit,rank))
                #Comment goes here!
    
    def shuffle_deck(self):
        random.shuffle(self.cards)
    
    def __str__(self):
        deck_order = ''
        for card in self.cards:
            deck_order += '\n' + card.__str__()
        return f"Deck Order: {deck_order}"

    def deal_cards(self):
        dealt_cards = []
        dealt_cards.append(self.cards.pop())
        dealt_cards.append(self.cards.pop())
        return dealt_cards

class Player():

    def __init__(self):
        self.hand = []
        self.chips = 100
        self.value = 0
        self.bet = 0

    def adjust_for_aces(self,deck,aces):          
        while self.value > 21 and aces:
            self.value -= 10
            aces -= 1

    def value_check(self,deck):                   
        ace_count = 0
        self.value = 0

        for card in self.hand:
            self.value += deck.value[card.rank]
            if card.rank == 'Ace':
                ace_count += 1
            
        self.adjust_for_aces(deck,ace_count)
    
    def place_bet(self):
        while True:
            try:
                self.bet = int(input("Place your bet: "))
            except:
                print("Please enter an integer.\n")
            else:
                if self.bet > self.chips:
                    print("You don't have enough chips!\n")
                    continue
                else:
                    print("Your bet has been placed!")
                    break
    
    def hit(self,deck):
        single_card = deck.cards.pop()
        self.hand.append(single_card)

class Dealer(Player):
    
    def __init__(self):
        self.hand = []
        self.value = 0

def check_for_naturals(player,dealer):
    player_turn = True
    player_ace = 0
    player_ten = 0
    dealer_ace = 0
    dealer_ten = 0

    for card in player.hand:
        if card.rank == 'Ace':
            player_ace = 1
        elif card.rank == '10':
            player_ten = 1 
        
    if player_ace and player_ten:
        for card in dealer.hand:
            if card.rank == 'Ace':
                dealer_ace = 1
            elif card.rank == '10':
                dealer_ten = 1
    
    if player_ace and player_ten and dealer_ace and dealer_ten:
        player_turn = False
        both_naturals(player,dealer)
    elif player_ace and player_ten and not dealer_ace and not dealer_ten:
        player_turn = False
        show_all(dealer,player)
        player_natural(player,dealer)
    
    return player_turn

def check_for_split(player,dealer):    
    cards = [] 
    
    for card in player.hand:
        cards.append(card.rank)

    if cards[0] == cards[1]:
        split = input("Would you like to split?: ")

        if split[0] == 'y':
            if player.bet * 2 > player.chips:
                print("You don't have enough chips to slit!")
                one_hand(player,deck)
            else:
                two_hands(player,deck)
        if split[0] == 'n':
            one_hand(player,deck)
    else:
        one_hand(player,deck)

def dealer_turn(dealer,deck):
    dealer.value_check(deck)
    while dealer.value < 17:
        dealer.hit(deck)
        dealer.value_check(deck)

def check_outcome(player,dealer,deck):
    show_all(dealer,player)
    dealer.value_check(deck)
    
    print(f"\nDealer has: {dealer.value}")
    print(f"You have: {player.value}")

    if dealer.value > 21:
        dealer_busts(player,dealer)
    elif dealer.value > player.value:
        dealer_wins(player,dealer)
    elif dealer.value < player.value:
        player_wins(player,dealer)
    else:
        push(player,dealer)

def one_hand(player,deck):
    player_turn = True

    while player_turn:
        player.value_check(deck)
        if player.value == 21:
            print("\nYou have 21!")
            dealer_turn(dealer,deck)
            check_outcome(player,dealer,deck)
            break
        else:
            # Hit or stand 
            player_turn = hit_or_stand(deck)

            # Check the value of the players hand
            player.value_check(deck)

            if player.value > 21:
                print(f"\nYou have: {player.value}")
                player_busts(player,dealer)
                break
            elif player.value == 21:
                print("\nYou have 21!")
                dealer_turn(dealer,deck)
                check_outcome(player,dealer,deck)
                break           

def two_hands(player,deck):
    player_turn = True

    while player_turn:
        first_hand = [player.hand[0]]
        second_hand = [player.hand[1]]
        
        print("\nFIRST HAND:")
        
        player.hand = first_hand
        player.hit(deck)

        show_some(dealer, player)

        round_one = check_for_naturals(player,dealer)

        while round_one:
            player.value_check(deck)
            if player.value == 21:
                print("\nYou have 21!")
                dealer_turn(dealer,deck)
                check_outcome(player,dealer,deck)
                break
            else:
                round_one = hit_or_stand(deck)
                player.value_check(deck)
                if player.value > 21:
                    player_busts(player,dealer)
                    print(f"\nYour chip total: {player.chips}")
                    break
                elif player.value == 21:
                    print("\nYou have 21!")
                    dealer_turn(dealer,deck)
                    check_outcome(player,dealer,deck)
                    break
        
        print(f"\nYour total chips: {player.chips}")
        print("\nSECOND HAND: ")
        
        player.hand = second_hand
        player.hit(deck)

        show_some(dealer,player)

        round_two = check_for_naturals(player,dealer)
        
        while round_two:
            player.value_check(deck)
            if player.value == 21:
                print("\nYou have 21!")
                dealer_turn(dealer,deck)
                check_outcome(player,dealer,deck)
                break
            else:
                round_two = hit_or_stand(deck)
                player.value_check(deck)
                if player.value > 21:
                    player_busts(player,dealer)
                    break
                elif player.value == 21:
                    print("\nYou have 21!")
                    dealer_turn(dealer,deck)
                    check_outcome(player,dealer,deck)
                    break
        player_turn = False
        
        

def show_some(dealer,player):
    print("\nDEALERS HAND:")
    print("Hidden Card")
    print(dealer.hand[1])

    print("\nYOUR HAND:")
    for card in player.hand:
        print(card)

def show_all(dealer,player):
    print("\nDEALERS HAND:")
    for card in dealer.hand:
        print (card)

    print("\nYOUR HAND:")
    for card in player.hand:
        print(card)

def hit_or_stand(deck):
    while True:
        player_move = input("\nWould you like to hit or stand?: ")

        if player_move[0].lower() == 'h':
            player.hit(deck)
            show_some(dealer,player)
            player_turn = True
        elif player_move[0].lower() == 's':
            dealer_turn(dealer,deck)
            check_outcome(player,dealer,deck)
            player_turn = False
        else:
            print("Invalid input. Try again.")
            continue
        break
    
    return player_turn

def both_naturals(player,dealer):
    print("It's a tie! You both have Blackjack!")

def player_natural(player,dealer):
    print("\nBLACKJACK! You win!")
    player.chips += int(player.bet * 1.5)

def player_busts(player,dealer):
    print("\nYou bust! Dealer wins.")
    player.chips -= player.bet

def dealer_busts(player,dealer):
    print("\nDealer busts! You win.")
    player.chips += player.bet

def player_wins(player,dealer):
    print("\nYou win!")
    player.chips += player.bet

def dealer_wins(player,dealer):
    print("\nDealer wins! You lose.")
    player.chips -= player.bet

def push(player,dealer):
    print("\nIt's a tie! Push.")

print("Welcome to Black Jack!")

player = Player()
dealer = Dealer()  

playing = True

while playing:
    # Set up deck, player, and dealer
    deck = Deck()
    deck.shuffle_deck()

    # Place bet
    player.place_bet()

    # Deal player and dealer hand
    player.hand = deck.deal_cards()
    dealer.hand = deck.deal_cards()

    # Show player hand and half of dealer hand
    show_some(dealer,player)

    # Check for automatic blackjacks
    player_turn = check_for_naturals(player,dealer)

    if player_turn:
        # Check for opportunity to split
        check_for_split(player,dealer)
            
    print(f"Your chip total: {player.chips}")

    if player.chips > 0:
        while True:
            keep_playing = input("\nWould you like to continue?: ")
            
            if keep_playing[0].lower() == 'y':
                playing = True
            elif keep_playing[0].lower() == 'n':
                print(f"\nYou're walking away with {player.chips} dollars!")
                print("Thanks for playing!")
                playing = False
            else:
                print("Invalid input. Try Again.")
                continue
            break
    else:
        print("\nYou're all out of chips!")
        print("Thanks for playing!")
        playing = False
        
    

    
    
