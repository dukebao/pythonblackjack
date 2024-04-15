import pygame
import sys
from model.game_logic import BlackjackGame

class GameView:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1500, 960))
        self.background = pygame.image.load('images/background.png').convert()  # Load the background image
        self.clock = pygame.time.Clock()
        self.game = BlackjackGame()
        self.card_images = {}
        self.load_card_images()
        self.game_over = False  # Indicates whether the game is over
        self.game_outcome = ''  # Stores the outcome message
        self.font = pygame.font.Font(None, 36) # basic font for text
        self.game.player.current_bet = 100

    def load_card_images(self):
        """Loads all card images and stores them in a dictionary."""
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
        for suit in suits:
            for rank in ranks:
                image_path = f'images/{rank}_of_{suit}.png'
                original_image = pygame.image.load(image_path)
                # Resize image - Adjust the target size to maintain aspect ratio if needed
                resized_image = pygame.transform.scale(original_image, (80, 100))  # Resize to 100x800
                self.card_images[f'{rank}_of_{suit}'] = resized_image

    def draw_button(self, text, position, size, font_size=36):
        font = pygame.font.Font(None, font_size)
        button_color = (34, 139, 34)  # Dark green color
        border_color = (0, 100, 0)  # Even darker green for the border
        shadow_color = (0, 50, 0)  # Shadow color
        text_color = (255, 255, 255)  # White text
        x, y = position
        width, height = size

        # Draw shadow
        shadow_rect = pygame.Rect(x + 2, y + 2, width, height)
        pygame.draw.rect(self.screen, shadow_color, shadow_rect)

        # Draw button
        button_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, button_color, button_rect)

        # Optionally draw a border around the button for better visibility
        pygame.draw.rect(self.screen, border_color, button_rect, 2)  # Width of 2 for the border

        # Draw text
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=button_rect.center)
        self.screen.blit(text_surface, text_rect)

        return button_rect

    def init_ui(self):
        self.bet_button_rect = self.draw_button("Increase Bet", (1300, 100), (200, 50))  # Adjust position and size as needed
        self.stand_button_rect = self.draw_button("Stand", (700, 790), (80, 50))
        self.hit_button_rect = self.draw_button("Hit", (700, 860), (80, 50))
        self.reset_button_rect = self.draw_button("Next Hand", (1300, 500), (200, 50))

    def init_double_down(self):
        self.double_down_button_rect = self.draw_button("Double Down", (800, 790), (80, 50), 24)

    def increase_bet(self):
        additional_bet = 100  # Define how much the bet increases each click
        if self.game.player.balance >= additional_bet:
            self.game.player.current_bet += additional_bet
            print(f"Bet increased by ${additional_bet}, total bet: ${self.game.player.current_bet}")
        else:
            print("Not enough balance to increase bet")

    def draw_card(self, card, position):
        """Draws a card image at the specified position."""
        card_key = f'{card.rank}_of_{card.suit}'
        card_image = self.card_images[card_key]
        self.screen.blit(card_image, position)

    def display_hand(self, hand, start_pos, hide_dealer_card=False):
        """Displays a hand of cards starting from a specific position."""
        x, y = start_pos
        for card in hand:
            self.draw_card(card, (x, y))
            if hide_dealer_card and card == hand[1]:
                # Draw a card back image for the second card if hide_second_card is True
                card_back = pygame.image.load('images/card_black.png')
                card_back = pygame.transform.scale(card_back, (80, 100))
                self.screen.blit(card_back, (x, y))
            x += 140  # Adjust spacing between cards

    def display_text(self, text, position):
        font = pygame.font.Font(None, 36)
        text_surface = font.render(text, True, (255, 255, 255))
        self.screen.blit(text_surface, position)

    def update_player_balance(self):
        bet_amount = self.game.player.current_bet

    def update_display(self, hide_dealer_card=False):
        self.screen.blit(self.background, (0, 0))
        #
        self.draw_button("Increase Bet", (1300, 100), (200, 50))  # Redraw button

        # Display the remaining number of cards in the deck
        card_count = f"Cards left: {len(self.game.decks.cards)}"
        self.display_text(card_count, (1300, 10))

        self.display_hand(self.game.player_hand, (100, 800))
        self.display_hand(self.game.dealer_hand, (100, 100), hide_dealer_card=hide_dealer_card)
        # Display outcome messages
        if self.game_over:
            self.display_text(self.game_outcome, (600, 480))
        balance_info = f"Balance: ${self.game.player.balance}"
        self.display_text(balance_info, (1300, 40))
        # display bet amount
        bet_info = f"Bet: ${self.game.player.current_bet}"
        self.display_text(bet_info, (1300, 70))
        # display double down button
        if len(self.game.player_hand) == 2:
            self.init_double_down()

        # display the buttons
        self.draw_button("Stand", (700, 790), (80, 50))
        self.draw_button("Hit", (700, 860), (80, 50))
        self.draw_button("Next Hand", (1300, 500), (200, 50))

        pygame.display.flip()

    def reset_game(self):
        """Resets the game to initial state without reshuffling the deck."""
        # Clear player and dealer hands
        self.game.player_hand = []
        self.game.dealer_hand = []

        # Deal new cards from the existing deck
        self.game.deal_initial_cards()

        self.game_over = False  # Reset the game over flag
        self.game_outcome = ''  # Clear the previous outcome

        self.update_display()  # Refresh the display to show the new game state

    def handle_hit(self):
        self.game.hit(self.game.player_hand)
        if self.game.is_busted(self.game.player_hand):
            self.game_over = True
            self.game_outcome = "Player busts!"
            self.display_text(self.game_outcome, (600, 480))

    def handle_stand(self):
        self.game.dealer_plays()
        self.game_outcome = self.game.check_winner()
        # update player balance based on outcome
        if self.game_outcome == "Player wins":
            self.game.player.win_bet()
        elif self.game_outcome == "Dealer wins":
            self.game.player.lose_bet()
        elif self.game_outcome == "Push":
            self.game.player.push()
        elif self.game_outcome == "Blackjack":
            self.game.player.blackjack()
        self.game_over = True
        self.display_text(self.game_outcome, (600, 480))

    def handle_double_down(self):
        if len(self.game.player_hand) == 2:  # Can only double down on the initial two cards
            if self.game.player.double_down():
                self.game.hit(self.game.player_hand)  # Player receives exactly one more card
                self.game.dealer_plays()  # Then it's the dealer's turn
                self.game_outcome = self.game.check_winner()
                # update player balance based on outcome
                if self.game_outcome == "Player wins":
                    self.game.player.win_bet()
                elif self.game_outcome == "Dealer wins":
                    self.game.player.lose_bet()
                elif self.game_outcome == "Push":
                    self.game.player.push()
                elif self.game_outcome == "Blackjack":
                    self.game.player.blackjack()
                # reset the current bet amount after double down
                self.game.player.current_bet = self.game.player.current_bet // 2
                self.game_over = True
            else:
                print("Not enough balance to double down")

    def main_loop(self):
        running = True
        self.game.deal_initial_cards()  # Start by dealing two cards each
        self.init_ui()  # Initialize the UI elements
        hide_dealer_card = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.bet_button_rect.collidepoint(event.pos):
                        self.increase_bet()
                    if self.double_down_button_rect.collidepoint(event.pos) and len(self.game.player_hand) == 2:
                        # Double down logic here
                        self.handle_double_down()
                        hide_dealer_card = False
                    if self.hit_button_rect.collidepoint(event.pos):
                        # Hit logic here
                        self.handle_hit()
                    if self.stand_button_rect.collidepoint(event.pos):
                        # Stand logic here
                        self.handle_stand()
                        hide_dealer_card = False
                    if self.reset_button_rect.collidepoint(event.pos) and self.game_over:
                        # Reset or new game logic here
                        hide_dealer_card = True
                        self.update_player_balance()
                        self.reset_game()


            self.update_display(hide_dealer_card=hide_dealer_card)
            self.clock.tick(60)  # Maintain 60 FPS

        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    gv = GameView()
    gv.main_loop()
