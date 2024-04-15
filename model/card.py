class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = self.assign_value(rank)

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    @staticmethod
    def assign_value(rank):
        """Assigns the Blackjack value to the card based on its rank."""
        if rank in ['jack', 'queen', 'king']:
            return 10
        elif rank == 'ace':
            return 11  # The adjustment for Ace being 1 or 11 is usually handled in the hand total calculation
        else:
            return int(rank)


if __name__ == '__main__':
    # Example usage
    card = Card('hearts', 'ace')
    print(card)
    print(card.value)
