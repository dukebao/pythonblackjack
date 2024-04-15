from .deck import Deck
from .player import Player

class BlackjackGame:
    def __init__(self):
        self.decks = self.create_decks(3)  # Use 3 decks
        self.decks.shuffle()
        self.player_hand = []
        self.dealer_hand = []
        self.player = Player()
        self.dealer = Player()

    def create_decks(self, num_decks):
        """Creates a combined deck consisting of `num_decks` decks."""
        deck = Deck()
        for _ in range(num_decks - 1):
            deck.cards.extend(Deck().cards)
        deck.shuffle()
        return deck

    def place_bet(self, amount=100):
        """Places a bet for the player."""
        # this updates the player's current_bet and balance
        return self.player.place_bet(amount)

    def deal_initial_cards(self):
        self.player_hand = [self.decks.deal_card() for _ in range(2)]
        self.dealer_hand = [self.decks.deal_card() for _ in range(2)]

    def hit(self, hand):
        """Adds a card to the hand from the deck."""
        hand.append(self.decks.deal_card())

    def calculate_score(self, hand):
        """Calculates the score of a hand."""
        score = 0
        ace_count = 0
        for card in hand:
            if card.rank == 'Ace':
                ace_count += 1
                score += 11
            else:
                score += card.value

        # Adjust score for Aces if score is over 21
        while score > 21 and ace_count:
            score -= 10
            ace_count -= 1

        return score

    def is_busted(self, hand):
        return self.calculate_score(hand) > 21

    def dealer_plays(self):
        """Handles the dealer's moves until the dealer stands or busts."""
        while self.calculate_score(self.dealer_hand) < 17:
            self.hit(self.dealer_hand)

    def check_winner(self):
        player_score = self.calculate_score(self.player_hand)
        dealer_score = self.calculate_score(self.dealer_hand)

        # add a logic for blackjack
        if player_score == 21 and len(self.player_hand) == 2 and dealer_score != 21 and len(self.dealer_hand) != 2:
            return "Blackjack"
        if player_score > 21:
            return "Dealer wins"
        elif dealer_score > 21:
            return "Player wins"
        elif player_score > dealer_score:
            return "Player wins"
        elif dealer_score > player_score:
            return "Dealer wins"
        if player_score == dealer_score:
            return "Push"

    def print_hand(self, hand):
        """Returns a string representation of a hand."""
        return ', '.join(str(card) for card in hand)

    def play(self):
        # Place a bet for the player
        bet_amount = 100
        print(f"Player's balance: {self.player.balance}")
        if not self.place_bet(bet_amount):
            print("Insufficient balance to place the bet.")
            return
        print(f"Player's bet: {bet_amount}"
              f"\nPlayer's balance after placing the bet: {self.player.balance}"    )

        self.deal_initial_cards()
        print("Player's hand:", self.print_hand(self.player_hand), "score:", self.calculate_score(self.player_hand))
        print("Dealer's hand: [", self.print_hand([self.dealer_hand[0]]), ", ?]")

        player_action = ''
        while player_action != 'stand' and not self.is_busted(self.player_hand):
            player_action = input("Do you want to 'hit' or 'stand'? ").lower()
            if player_action == 'hit':
                self.hit(self.player_hand)
                print("Player's hand:", self.print_hand(self.player_hand), "score:", self.calculate_score(self.player_hand))
                if self.is_busted(self.player_hand):
                    print("Player busts! Dealer wins.")
                    return

        if not self.is_busted(self.player_hand):
            print("Dealer's full hand:", self.print_hand(self.dealer_hand), "score:", self.calculate_score(self.dealer_hand))
            self.dealer_plays()
            print("Dealer's final hand:", self.print_hand(self.dealer_hand), "score:", self.calculate_score(self.dealer_hand))

        print(self.check_winner())

# Example usage
if __name__ == "__main__":
    game = BlackjackGame()
    game.play()
