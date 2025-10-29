import streamlit as st
st.title('Texas Holdem Poker')
st.write("Hello World")
# List of possible card values
values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

# List of possible suits (H = Hearts, S = Spades, C = Clubs, D = Diamonds)
suits = ["H", "S", "C", "D"]


import random

class Deck:
    def __init__(self):
        self.cards = []
        self.create_deck()
    def __repr__(self):
        row1 = ' '.join(str(card) for card in self.cards[:13])
        row2 = ' '.join(str(card) for card in self.cards[13:26])
        row3 = ' '.join(str(card) for card in self.cards[26:39])
        row4 = ' '.join(str(card) for card in self.cards[39:52])
        # return (f"{row1}\n{row2}\n{row3}\n{row4}")
        
        return str(self.cards)
    def create_deck(self):
        for i in suits:
                for j in values:
                    self.cards.append(Card(j, i)) 
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def deal_one(self):
        card = self.cards.pop(0)
        return str(card)
        

class Card:
    def __init__(self, num, suit):
        self.num = num
        self.suit = suit

    def __repr__(self):
        return(f"{self.num}{self.suit}")
        
class Hand:
    def __init__(self, owner = "Player"):
        self.owner = owner
        self.cards = []
        
    def show(self):
        return f"{self.owner} - {self.cards}"
        
    def add_card(self, card):
        self.cards.append(card)

# Test full deck
print("--- Testing Deck ---")
deck = Deck()
deck.create_deck()
print(f"deck:\n{deck}")  # prints the whole deck

# Test shuffle()
print("--- Testing shuffle() ---")
deck.shuffle()
print(f"deck:\n{deck}")

# Hand class & test deal_one()
print("--- Hand class & test deal_one() ---")

# Create players with their own Hand objects
players = [Hand("Alice"), Hand("Bob")]

# Deal one card from the deck to each player
for player in players:
    player.add_card(deck.deal_one())
    print(player.show())

# Show final result of deck
print("--- Final result of deck ---")
print(f"deck:\n{deck}")

playerCount = st.slider('Amount Of Players', 2, 10)

for i in range(playerCount):
    title = st.text_input("Name:", "")