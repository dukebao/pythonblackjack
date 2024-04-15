import random
from .card import Card

class Deck:
    def __init__(self):
        self.cards = self.create_deck()

    def create_deck(self):
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
        return [Card(suit, rank) for suit in suits for rank in ranks]

    def shuffle(self):
        """Shuffles the deck of cards."""
        random.shuffle(self.cards)

    def deal_card(self):
        """Deals (removes and returns) one card from the deck."""
        return self.cards.pop()

    def __str__(self):
        return '\n'.join(str(card) for card in self.cards)


if __name__ == '__main__':
    deck = Deck()
    print("Original deck:")
    print(deck)

    deck.shuffle()
    print("\nShuffled deck:")
    print(deck)

    card_dealt = deck.deal_card()
    print(f"\nDealt card: {card_dealt}")
    print("\nDeck after dealing one card:")
    print(deck)