# Texas Hold'em Poker - Soumil Voona (4th Pd. Finnegan)
import streamlit as st
import random as rd


# List of possible card values (0=10 for images)
values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "0", "J", "Q", "K"]
# List of possible suits (H = Hearts, S = Spades, C = Clubs, D = Diamonds)
suits = ["H", "S", "C", "D"]

class Card:
   def __init__(self, num, suit):
       self.num = num
       self.suit = suit
   def __repr__(self):
       return f"{self.num}{self.suit}"

class Deck:
   def __init__(self):
       self.cards = []
       self.create_deck()
   def __repr__(self):
       return str(self.cards)
   def create_deck(self):
       for s in suits:
           for v in values:
               self.cards.append(Card(v, s))
   def shuffle(self):
       rd.shuffle(self.cards)
   def deal_one(self):
       return str(self.cards.pop(0))


class Hand:
   def __init__(self, owner="Player"):
       self.owner = owner
       self.cards = []
   def show(self):
       return f"{self.owner} - {self.cards}"
   def add_card(self, card):
       self.cards.append(card)


st.set_page_config(page_title="Texas Hold'em Poker", page_icon=":black_joker:", layout="centered")
st.title("Texas Hold'em Poker")


def check_winner(cards):
   returnDict = {}
   cardList = []
   suitList = []
   #Creates Card List with values as integers
   for c in cards:
       card, suit = c[0], c[1]
       suitList.append(suit)
       if card not in ["A", "0", "J", "Q", "K"]:
           cardList.append(int(card))
       else:
           match card:
               case '0':
                   cardList.append(10)
               case 'J':
                   cardList.append(11)
               case 'Q':
                   cardList.append(12)
               case 'K':
                   cardList.append(13)
               case 'A':
                   cardList.append(14)
  
   cardList.sort(reverse=True)
   #Check for straight flush and royal flush
   for suit in ["H", "S", "C", "D"]:
       suited_cards = [cardList[i] for i in range(len(cards)) if suitList[i] == suit]
       if len(suited_cards) >= 5:
           suited_cards.sort(reverse=True)
           for i in range(len(suited_cards) - 4):
               if suited_cards[i] - suited_cards[i+4] == 4:
                   if suited_cards[i] == 14:
                       returnDict["royal_flush"] = suited_cards[i:i+5]
                       returnDict["rank"] == 9
                   else:
                       returnDict["straight_flush"] = suited_cards[i:i+5]
                       returnDict["rank"] = 8
                       return returnDict


   # Check for four of a kind
   freq = {} #Stack Overflow
   for num in cardList: #Stack Overflow
       freq[num] = freq.get(num, 0) + 1 #Stack Overflow
   for num, count in freq.items():
       if count == 4:
           returnDict["four_kind"] = [num]
           returnDict["rank"] = 7
           return returnDict


   # Check for full house
   three_kind = None
   pair = None
   for num, count in freq.items():
       if count == 3:
           three_kind = num
       elif count == 2:
           pair = num
   if three_kind and pair:
       returnDict["full_house"] = [three_kind, pair]
       returnDict["rank"] = 6
       return returnDict


   # Check for flush
   for suit in ["H", "S", "C", "D"]: #Copilot AI
       suited_cards = [cardList[i] for i in range(len(cards)) if suitList[i] == suit] #Copilot AI
       if len(suited_cards) >= 5:
           returnDict["flush"] = sorted(suited_cards, reverse=True)[:5]
           returnDict["rank"] = 5
           return returnDict


   # Check for straight
   unique_cards = sorted(set(cardList), reverse=True)
   for i in range(len(unique_cards) - 4):
       if unique_cards[i] - unique_cards[i+4] == 4:
           returnDict["straight"] = unique_cards[i:i+5]
           returnDict["rank"] = 4
           return returnDict


   # Check for three of a kind
   for num, count in freq.items():
       if count == 3:
           returnDict["three_kind"] = [num]
           returnDict["rank"] = 3
           return returnDict


   # Check for two pair
   pairs = []
   for num, count in freq.items():
       if count == 2:
           pairs.append(num)
   if len(pairs) >= 2:
       returnDict["two_pair"] = sorted(pairs, reverse=True)[:2]
       returnDict["rank"] = 2
       return returnDict


   # Check for one pair
   if pairs:
       returnDict["pair"] = [max(pairs)]
       returnDict["rank"] = 1
       return returnDict


   # High card
   returnDict["high"] = [cardList[0]]
   returnDict["rank"] = 0
   return returnDict

#Checks if they are already playing or not
if "submitted" not in st.session_state:
   st.session_state.submitted = False
if "playing" not in st.session_state:
   st.session_state.playing = True

#Initial page - asks for user count and player names
if not st.session_state.submitted:
   col1, col2 = st.columns([1, 5])
   with col1: st.markdown("**Player Count:**")
   with col2:
       playerCount = st.select_slider(
           label="Player Count", label_visibility="collapsed",
           options=list(range(2, 11)), value=2
       )
   playerNames = []
   for i in range(playerCount):
       col1, col2 = st.columns([1, 5.25])
       with col1: st.markdown(f"**Player {i+1} Name:**")
       with col2:
           playerName = st.text_input(
               label=f"Player {i+1} name",
               label_visibility="collapsed",
               key=f"player{i+1}"
           )
       playerNames.append(playerName)
   #Initializes state variables for users playing
   if st.button("Ready To Play!"):
       st.session_state.submitted = True
       st.session_state.playerNames = playerNames
       st.session_state.deck = Deck()
       st.session_state.deck.shuffle()
       st.session_state.players = []
       st.session_state.money = []
       st.session_state.pot = 0
       st.session_state.turn = 0
       st.session_state.showing_cards = False
       st.session_state.round = 0
       st.session_state.current_bet = 10
       st.session_state.player_bets = []
       st.session_state.players_playing = []
       st.session_state.betting_round = 0
       st.session_state.players_played = []
       st.session_state.eliminated = []

       for i in range(len(playerNames)):
           st.session_state.players.append(Hand(playerNames[i]))
           for _ in range(2):
               st.session_state.players[i].add_card(st.session_state.deck.deal_one())


       st.session_state.openCards = [st.session_state.deck.deal_one() for _ in range(5)]
       for _ in range(len(playerNames)):
           st.session_state.money.append(200)
           st.session_state.player_bets.append(0)
           st.session_state.players_playing.append(True)
           st.session_state.players_played.append(False)


       small_blind = st.session_state.round % len(playerNames)
       big_blind = (st.session_state.round + 1) % len(playerNames)
       st.session_state.money[small_blind] -= 5
       st.session_state.money[big_blind] -= 10
       st.session_state.player_bets[small_blind] = 5
       st.session_state.player_bets[big_blind] = 10
       st.session_state.pot = 15
       st.session_state.players_played[small_blind] = True
       st.session_state.players_played[big_blind] = True
       st.session_state.currentPlayer = (st.session_state.round + 2) % len(playerNames)
       st.rerun()


else:
   if st.session_state.playing:
       while not st.session_state.players_playing[st.session_state.currentPlayer]:
           st.session_state.currentPlayer = (st.session_state.currentPlayer + 1) % len(st.session_state.players)
       st.session_state.neededMoney = st.session_state.current_bet - st.session_state.player_bets[st.session_state.currentPlayer]


       st.markdown(f"**Pot: ${st.session_state.pot}**")
       st.markdown(f"**Current Highest Bet: ${st.session_state.current_bet}**")


       for i in range(len(st.session_state.players)):
           status = "FOLDED" if not st.session_state.players_playing[i] else "Playing"
           st.text(f"{st.session_state.playerNames[i]} - Money: ${st.session_state.money[i]} | Bet: ${st.session_state.player_bets[i]} | Need: ${st.session_state.current_bet - st.session_state.player_bets[i]} | {status}")


       col1, col12, col2 = st.columns([1, .5, 1])
       with col1:
           col1_1, col1_2_1, col1_2_2 = st.columns([1, 1, 1])
           with col1_1:
               st.markdown(f"**{st.session_state.playerNames[st.session_state.currentPlayer]}**")
          
           hand = st.session_state.players[st.session_state.currentPlayer]
          
           with col1_2_1:
               st.image(f"https://deckofcardsapi.com/static/img/{('back', hand.cards[0])[st.session_state.showing_cards]}.png", width=80)


           with col1_2_2:
               st.image(f"https://deckofcardsapi.com/static/img/{('back', hand.cards[1])[st.session_state.showing_cards]}.png", width=80)


           st.write("")


       with col2:
           cards_to_show = {0: 0, 1: 3, 2: 4, 3: 5}


           cards_revealed = cards_to_show.get(st.session_state.betting_round, 0)
         
           col2_1, col2_2, col2_3 = st.columns([1, 1, 1])
           with col2_1:
               st.image(f"https://deckofcardsapi.com/static/img/{('back', st.session_state.openCards[0])[cards_revealed >= 1]}.png", width=80)
               st.write("")
               st.image(f"https://deckofcardsapi.com/static/img/{('back', st.session_state.openCards[3])[cards_revealed >= 4]}.png", width=80)


           with col2_2:
               st.image(f"https://deckofcardsapi.com/static/img/{('back', st.session_state.openCards[1])[cards_revealed >= 2]}.png", width=80)
               st.write("")
               st.image(f"https://deckofcardsapi.com/static/img/{('back', st.session_state.openCards[4])[cards_revealed >= 5]}.png", width=80)


           with col2_3:
               st.image(f"https://deckofcardsapi.com/static/img/{('back', st.session_state.openCards[2])[cards_revealed >= 3]}.png", width=80)
       col1, col2 = st.columns([1,5])
       with col1:
           st.text("Custom Bet:")
       with col2:
           if st.session_state.money[st.session_state.currentPlayer] <= st.session_state.neededMoney:
               st.write("Not enough money to raise - must go all in or fold")
               st.session_state.amountOfMoney = st.session_state.money[st.session_state.currentPlayer]
           else:
               remaining_money = st.session_state.money[st.session_state.currentPlayer]
               min_bet = max(st.session_state.neededMoney, 0)
               if min_bet <= remaining_money:
                   st.session_state.amountOfMoney = st.select_slider(
                       label="Bet Amount",
                       label_visibility="collapsed",
                       options=list(range(min_bet, remaining_money + 1)),
                       value=min_bet,
                       key=f"bet_slider_{st.session_state.currentPlayer}_{st.session_state.turn}"
                   )
               else:
                   st.write("Must go all in or fold")
                   st.session_state.amountOfMoney = remaining_money


       def round_complete():
           active_count = sum(st.session_state.players_playing)
           if active_count <= 1:
               return True
           for i in range(len(st.session_state.players)):
               if st.session_state.players_playing[i] and st.session_state.money[i] > 0:
                   if not st.session_state.players_played[i] or st.session_state.player_bets[i] < st.session_state.current_bet:
                       return False
           return True


       def next_round():
           active_count = sum(st.session_state.players_playing)
           if active_count <= 1 or st.session_state.betting_round >= 3 or all(v == 0 for v in st.session_state.money):
               st.session_state.showing_cards = False
               st.session_state.playing = False
               return
           st.session_state.betting_round += 1
           st.session_state.current_bet = 0
           for i in range(len(st.session_state.players)):
               st.session_state.player_bets[i] = 0
               st.session_state.players_played[i] = False


       col1, col2, col3, col4, col5 = st.columns(5)
       with col1:
           if st.button("Raise", use_container_width=True):
               if st.session_state.amountOfMoney > st.session_state.neededMoney:
                   amt = st.session_state.amountOfMoney
                   st.session_state.money[st.session_state.currentPlayer] -= amt
                   st.session_state.pot += amt
                   st.session_state.player_bets[st.session_state.currentPlayer] += amt
                   st.session_state.current_bet = st.session_state.player_bets[st.session_state.currentPlayer]
                   st.session_state.players_played[st.session_state.currentPlayer] = True
                   for i in range(len(st.session_state.players)):
                       if i != st.session_state.currentPlayer and st.session_state.players_playing[i]:
                           st.session_state.players_played[i] = False
                   st.session_state.currentPlayer = (st.session_state.currentPlayer + 1) % len(st.session_state.players)
                   st.session_state.turn += 1
                   st.session_state.showing_cards = False
                   if round_complete(): next_round()
                   st.rerun()
               else:
                   st.error("Raise amount must be greater than needed amount")


       with col2:
           if st.button("Fold", use_container_width=True):
               st.session_state.players_playing[st.session_state.currentPlayer] = False
               st.session_state.players_played[st.session_state.currentPlayer] = True
               st.session_state.currentPlayer = (st.session_state.currentPlayer + 1) % len(st.session_state.players)
               st.session_state.turn += 1
               st.session_state.showing_cards = True
               if round_complete(): next_round()
               st.rerun()


       with col3:
           if st.session_state.neededMoney > 0:
               if st.button("Call", use_container_width=True):
                   amt = min(st.session_state.neededMoney, st.session_state.money[st.session_state.currentPlayer])
                   st.session_state.money[st.session_state.currentPlayer] -= amt
                   st.session_state.pot += amt
                   st.session_state.player_bets[st.session_state.currentPlayer] += amt
                   st.session_state.players_played[st.session_state.currentPlayer] = True
                   st.session_state.currentPlayer = (st.session_state.currentPlayer + 1) % len(st.session_state.players)
                   st.session_state.turn += 1
                   st.session_state.showing_cards = False
                   if round_complete(): next_round()
                   st.rerun()
           else:
               if st.button("Check", use_container_width=True):
                   st.session_state.players_played[st.session_state.currentPlayer] = True
                   st.session_state.currentPlayer = (st.session_state.currentPlayer + 1) % len(st.session_state.players)
                   st.session_state.turn += 1
                   st.session_state.showing_cards = False
                   if round_complete(): next_round()
                   st.rerun()


       with col4:
           if st.button("All In", use_container_width=True):
               all_in = st.session_state.money[st.session_state.currentPlayer]
               st.session_state.money[st.session_state.currentPlayer] = 0
               st.session_state.pot += all_in
               st.session_state.player_bets[st.session_state.currentPlayer] += all_in
               if st.session_state.player_bets[st.session_state.currentPlayer] > st.session_state.current_bet:
                   st.session_state.current_bet = st.session_state.player_bets[st.session_state.currentPlayer]
                   for i in range(len(st.session_state.players)):
                       if i != st.session_state.currentPlayer and st.session_state.players_playing[i]:
                           st.session_state.players_played[i] = False
               st.session_state.players_played[st.session_state.currentPlayer] = True
               st.session_state.currentPlayer = (st.session_state.currentPlayer + 1) % len(st.session_state.players)
               st.session_state.turn += 1
               st.session_state.showing_cards = False
               if round_complete(): next_round()
               st.rerun()


       with col5:
           if st.button("Show Cards", use_container_width=True):
               st.session_state.showing_cards = not st.session_state.showing_cards
               st.rerun()


   else:
       col1, col2_1, col2_2 = st.columns([1, 2, 2])
       ranks = []
       active_players = []
      
       for i in range(len(st.session_state.playerNames)):
           if st.session_state.players_playing[i]:
               with col1:
                   st.markdown(f"**{st.session_state.playerNames[i]}:**")
                   for _ in range(4): st.write("")
               hand = st.session_state.players[i]
               with col2_1: st.image(f"https://deckofcardsapi.com/static/img/{hand.cards[0]}.png", width=65)
               with col2_2: st.image(f"https://deckofcardsapi.com/static/img/{hand.cards[1]}.png", width=65)
               ranks.append(check_winner(hand.cards + st.session_state.openCards))
               active_players.append(i)


       # Display community cards
       col1, col2, col3 = st.columns(3)
       with col1:
           st.image(f"https://deckofcardsapi.com/static/img/{st.session_state.openCards[0]}.png", width=80)
           st.write("")
           st.image(f"https://deckofcardsapi.com/static/img/{st.session_state.openCards[3]}.png", width=80)


       with col2:
           st.image(f"https://deckofcardsapi.com/static/img/{st.session_state.openCards[1]}.png", width=80)
           st.write("")
           st.image(f"https://deckofcardsapi.com/static/img/{st.session_state.openCards[4]}.png", width=80)


       with col3:
           st.image(f"https://deckofcardsapi.com/static/img/{st.session_state.openCards[2]}.png", width=80)

       
       # Determine winner
       hand_names = {
           0: "High Card",
           1: "Pair",
           2: "Two Pair",
           3: "Three of a Kind",
           4: "Straight",
           5: "Flush",
           6: "Full House",
           7: "Four of a Kind",
           8: "Straight Flush",
           9: "Royal Flush"
       }
      
       best_rank = max(r["rank"] for r in ranks)
       winners = [i for i, r in enumerate(ranks) if r["rank"] == best_rank]
       if best_rank == 8:  # Straight Flush
           highest_card = max(ranks[i]["straight_flush"][0] for i in winners)
           winners = [i for i in winners if ranks[i]["straight_flush"][0] == highest_card]
      
       elif best_rank == 7:  # Four of a Kind
           highest_four = max(ranks[i]["four_kind"][0] for i in winners)
           winners = [i for i in winners if ranks[i]["four_kind"][0] == highest_four]
      
       elif best_rank == 6:  # Full House
           highest_three = max(ranks[i]["full_house"][0] for i in winners)
           tied = [i for i in winners if ranks[i]["full_house"][0] == highest_three]
           if len(tied) == 1:
               winners = tied
           highest_pair = max(ranks[i]["full_house"][1] for i in tied)
           winners = [i for i in tied if ranks[i]["full_house"][1] == highest_pair]
      
       elif best_rank == 5:  # Flush
           for card_pos in range(5):
               highest = max(ranks[i]["flush"][card_pos] for i in winners)
               winners = [i for i in winners if ranks[i]["flush"][card_pos] == highest]
      
       elif best_rank == 4:  # Straight
           highest_card = max(ranks[i]["straight"][0] for i in winners)
           winners = [i for i in winners if ranks[i]["straight"][0] == highest_card]
      
       elif best_rank == 3:  # Three of a Kind
           highest_three = max(ranks[i]["three_kind"][0] for i in winners)
           winners = [i for i in winners if ranks[i]["three_kind"][0] == highest_three]
      
       elif best_rank == 2:  # Two Pair
           highest_first = max(ranks[i]["two_pair"][0] for i in winners)
           tied = [i for i in winners if ranks[i]["two_pair"][0] == highest_first]
           if len(tied) == 1:
               winners = tied
           highest_second = max(ranks[i]["two_pair"][1] for i in tied)
           winners = [i for i in tied if ranks[i]["two_pair"][1] == highest_second]
      
       elif best_rank == 1:  # Pair
           highest_pair = max(ranks[i]["pair"][0] for i in winners)
           winners = [i for i in winners if ranks[i]["pair"][0] == highest_pair]

       if best_rank == 0:  # High card situation
           highest_card = max(ranks[i]["high"][0] for i in winners)
           winners = [i for i in winners if ranks[i]["high"][0] == highest_card] #Copilot AI
      
       if "pot_distributed" not in st.session_state:
           st.session_state.pot_distributed = False
          
       if not st.session_state.pot_distributed:
           pot_to_distribute = st.session_state.pot
          
           if len(winners) == 1:
               winner = active_players[winners[0]]
               st.success(f"{st.session_state.playerNames[winner]} wins with {hand_names[ranks[winners[0]]['rank']]}!")
               st.session_state.money[winner] += pot_to_distribute
           else:
               split_amount = pot_to_distribute // len(winners)
               remainder = pot_to_distribute % len(winners)
               winner_names = [st.session_state.playerNames[active_players[i]] for i in winners]


               for i in winners:
                   st.session_state.money[active_players[i]] += split_amount
          
               st.success(f"Split pot between {', '.join(winner_names)} with {hand_names[ranks[winners[0]]['rank']]}!")
          
           st.write(f"Pot distributed: ${pot_to_distribute}")
          
           st.session_state.pot_distributed = True
      
       st.write("**Final money totals:**")
       for i in range(len(st.session_state.playerNames)):
           st.text(f"{st.session_state.playerNames[i]}: ${st.session_state.money[i]}")
       
       money1 = st.session_state.money
       money2 = []
       playerNames = []
       eliminated = []
       print(money1)
       for i in range (len(money1)):
           if money1[i] == 0:
               eliminated += st.session_state.playerNames[i]
               st.session_state.eliminated += st.session_state.playerNames[i]
               st.session_state.submitted = True
           else:
               money2.append(money1[i])
               playerNames.append(st.session_state.playerNames[i])
               print(f"player names - {playerNames}")
       st.session_state.money = money1
       st.session_state.playerNames = playerNames
       print(st.session_state.playerNames)

       eliminatedString = ", ".join(eliminated)
       if 0 in money1:
           st.toast(f"Players {eliminatedString} eliminated!\nStarting next round")

       if st.button("Play Next Game", use_container_width=True):
           existing_money = money
           existing_names = st.session_state.playerNames.copy() #Stack Overflow
           st.session_state.deck = Deck()
           st.session_state.deck.shuffle()
           st.session_state.players = []
           st.session_state.pot = 15
           st.session_state.turn = 0
           st.session_state.showing_cards = False
           st.session_state.round += 1
           st.session_state.current_bet = 10
           st.session_state.player_bets = []
           st.session_state.players_playing = []
           st.session_state.betting_round = 0
           st.session_state.players_played = []
           st.session_state.playing = True
           st.session_state.pot_distributed = False


           for i in range(len(existing_names)):
               st.session_state.players.append(Hand(existing_names[i]))
               for _ in range(2):
                   st.session_state.players[i].add_card(st.session_state.deck.deal_one())
               st.session_state.player_bets.append(0)
               st.session_state.players_playing.append(True)
               st.session_state.players_played.append(False)


           st.session_state.openCards = [st.session_state.deck.deal_one() for _ in range(5)]
           st.session_state.money = existing_money


           small_blind = st.session_state.round % len(existing_names)
           big_blind = (st.session_state.round + 1) % len(existing_names)
          
           if st.session_state.money[small_blind] >= 5:
               st.session_state.money[small_blind] -= 5
               st.session_state.player_bets[small_blind] = 5
          
           if st.session_state.money[big_blind] >= 10:
               st.session_state.money[big_blind] -= 10
               st.session_state.player_bets[big_blind] = 10
          
           st.session_state.players_played[small_blind] = True
           st.session_state.players_played[big_blind] = True
           st.session_state.currentPlayer = (st.session_state.round + 2) % len(existing_names)
           st.session_state.playing = True
           st.rerun()