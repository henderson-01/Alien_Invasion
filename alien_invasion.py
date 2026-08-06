import sys
from time import sleep

import pygame

from alien import Alien
from bullet import Bullet
from button import Button
from dropdown import Dropdown
from game_stats import GameStats
from high_score_manager import load_all_scores, load_user_high_score, save_high_score
from scoreboard import Scoreboard
from settings import Settings
from ship import Ship


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((800, 600))
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        # Create an instance to store game statistics.
        self.stats: GameStats = GameStats(self)
        self.sb: Scoreboard = Scoreboard(self)
        self.ship: Ship = Ship(self)
        self.bullets: pygame.sprite.Group = pygame.sprite.Group()
        self.aliens: pygame.sprite.Group = pygame.sprite.Group()
        self._create_fleet()
        # Start alien invasion in an inactive state.
        self.game_active = False
        self.game_state = 'MENU'
        self.user_name_input = ""
        self.dropdown = None
        self.font = pygame.font.SysFont(None, 48)
        # Make the play button.
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            # Redraw the screen during each pass through the loop.
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_high_score(self.stats.score, self.user_name_input)
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if self.game_state == 'NAME_INPUT':
                    self._handle_name_input(event)
                else:
                    self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.game_state == 'MENU':
                    self._check_play_button(mouse_pos)
                elif self.game_state == 'NAME_INPUT' and self.dropdown is not None:
                    selected = self.dropdown.handle_mouse_click(mouse_pos)
                    if selected >= 0:
                        self.user_name_input = self.dropdown.options[selected]

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            save_high_score(self.stats.score, self.user_name_input)
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_play_button(self, mouse_pos):
        """Transition to name input state when the play button is clicked."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self._prepare_dropdown()
            self.game_state = 'NAME_INPUT'

    def _prepare_dropdown(self):
        """Rebuild the dropdown from the currently saved usernames."""
        users = sorted(load_all_scores().keys())
        rect = pygame.Rect(0, 0, 400, 40)
        rect.center = (self.settings.screen_width // 2, self.settings.screen_height // 2 + 85)
        self.dropdown = Dropdown(self, users, rect) if users else None

    def _start_game(self):
        """Reset game state and start the gameplay."""
        # Reset the game settings.
        self.settings.initialize_dynamic_settings()
        # Reset the game statistics.
        self.stats.reset_stats()
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()
        self.stats.high_score = load_user_high_score(self.user_name_input)
        self.sb.prep_high_score()
        self.game_active = True
        self.game_state = 'GAMEPLAY'
        # Get rid of any remaining bullets and aliens.
        self.bullets.empty()
        self.aliens.empty()
        # Create a new fleet and center the ship.
        self._create_fleet()
        self.ship.center_ship()
        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

    def _handle_name_input(self, event):
        """Handle keyboard input for the username."""
        if (self.dropdown is not None and self.dropdown.expanded
                and self.dropdown.handle_keydown(event)):
            if event.key == pygame.K_RETURN:
                selected = self.dropdown.selected_value()
                if selected is not None:
                    self.user_name_input = selected
            return
        if event.key == pygame.K_RETURN:
            if not self.user_name_input.strip():
                # Default to 'Player' if no name is entered.
                self.user_name_input = "Player"
            self._start_game()
        elif event.key == pygame.K_BACKSPACE:
            self.user_name_input = self.user_name_input[:-1]
        elif event.key == pygame.K_ESCAPE:
            # Allow the player to go back to the menu.
            self.game_state = 'MENU'
        else:
            # Only allow print characters.
            if event.unicode.isprintable() and len(self.user_name_input) < 15:
                self.user_name_input += event.unicode

    def _draw_name_input_screen(self):
        """Draw a clean, well-aligned username input screen."""
        self.screen.fill(self.settings.bg_color)

        # Prompt Title
        prompt_img = self.font.render("Enter Username:", True, (30, 30, 30))
        prompt_rect = prompt_img.get_rect(
            center=(self.settings.screen_width // 2, self.settings.screen_height // 2 - 110)
        )
        self.screen.blit(prompt_img, prompt_rect)

        # Input Box (Crisp white box with dark border)
        box_width, box_height = 400, 50
        box_rect = pygame.Rect(0, 0, box_width, box_height)
        box_rect.center = (self.settings.screen_width // 2, self.settings.screen_height // 2 - 35)
        
        pygame.draw.rect(self.screen, (255, 255, 255), box_rect, border_radius=6)
        pygame.draw.rect(self.screen, (50, 50, 50), box_rect, 2, border_radius=6)

        # Text & Blinking Cursor
        cursor = "_" if (pygame.time.get_ticks() // 500) % 2 == 0 else " "
        display_text = self.user_name_input + cursor
        
        text_img = self.font.render(display_text, True, (0, 0, 0))
        text_rect = text_img.get_rect(center=box_rect.center)
        self.screen.blit(text_img, text_rect)

        # Dropdown for returning players
        if self.dropdown is not None:
            self.dropdown.draw()

        # Instruction Hints
        sub_font = pygame.font.SysFont(None, 28)
        hint_img = sub_font.render("Press ENTER to Start  |  ESC to Cancel", True, (100, 100, 100))
        hint_rect = hint_img.get_rect(
            center=(self.settings.screen_width // 2, self.settings.screen_height // 2 + 150)
        )
        self.screen.blit(hint_img, hint_rect)

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of the bullets and get rid of the old bullets."""
        # Updated bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullets-alien collisions."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(self.aliens, self.bullets, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Destroy existing bullets and create a new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            # Increase level.
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """Check if the fleet is at an edge, then update positions."""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens): # type:ignore
            self._ship_hit()
        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and keep adding aliens until there's no room left.
        # Space between aliens is one alien width and one alien height.
        alien = Alien(self)
        alien_width = alien.rect.width
        alien_height = alien.rect.height
        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            # Finished a row; reset x value, and increment y value.
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the fleet."""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.screen.get_rect().height:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrement ships_left, and update scoreboard.
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()
            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()
            # Pause
            sleep(0.5)
        else:
            self.game_active = False
            self.game_state = 'MENU'
            save_high_score(self.stats.score, self.user_name_input)
            pygame.mouse.set_visible(True)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Update image on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        # Draw the score information.
        self.sb.show_score()
        # Draw UI based on state.
        if not self.game_active:
            if self.game_state == 'MENU':
                self.play_button.draw_button()
            elif self.game_state == 'NAME_INPUT':
                self._draw_name_input_screen()

        pygame.display.flip()


if __name__ == "__main__":
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()