class Player:
    def __init__(self, starting_balance=1000):
        self.balance = starting_balance  # Player starts with $1000
        self.current_bet = 0

    def place_bet(self):
        """Places a bet, reducing the balance by the bet amount."""
        amount = self.current_bet
        if amount <= self.balance:
            self.current_bet = amount
            self.balance -= amount
            return True
        return False  # Bet could not be placed if amount exceeds balance

    def double_down(self):
        print("Before double down: ", self.balance, self.current_bet)
        if self.balance >= self.current_bet:  # Check if the player has enough balance to double the bet
            self.current_bet *= 2  # Double the current bet
            print("After double down: ", self.balance, self.current_bet)
            return True
        return False  # Return False if the player doesn't have enough balance

    def win_bet(self):
        """Player wins the bet; wins double the bet amount."""
        self.balance += 2 * self.current_bet
        # self.current_bet = 0

    def lose_bet(self):
        """Player loses the bet; bet amount is already deducted."""
        self.balance -= self.current_bet
        # self.current_bet = 0

    def blackjack(self):
        """Player wins with a Blackjack; wins 1.5 times the bet amount."""
        self.balance += 1.5 * self.current_bet
        # self.current_bet = 0

    def push(self):
        """Handle a push (tie); the bet is returned to the player."""
        self.balance += self.current_bet
        # self.current_bet = 0
