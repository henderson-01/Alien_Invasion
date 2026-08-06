import pygame.font


class Dropdown:
    """A dropdown menu to pick a saved username."""

    def __init__(self, ai_game, options, rect):
        """Initialize dropdown attributes."""
        self.screen = ai_game.screen
        self.options = options
        self.rect = rect
        self.expanded = False
        self.selected_index = -1
        self.font = pygame.font.SysFont(None, 32)
        self.item_height = 36
        self.max_visible = 5
        self.text_color = (30, 30, 30)
        self.bg_color = (255, 255, 255)
        self.border_color = (50, 50, 50)
        self.highlight_color = (0, 135, 0)

    def handle_mouse_click(self, mouse_pos):
        """Process a mouse click. Returns the selected option index, or -1."""
        if self.expanded:
            for i, item_rect in enumerate(self._item_rects()):
                if item_rect.collidepoint(mouse_pos):
                    self.selected_index = i
                    self.expanded = False
                    return i
            self.expanded = False
            return -1
        else:
            if self.rect.collidepoint(mouse_pos):
                self.expanded = True
            return -1

    def handle_keydown(self, event):
        """Process a key press when open. Returns True if the key was consumed."""
        if not self.expanded:
            return False
        if event.key == pygame.K_UP:
            if self.selected_index < 0:
                self.selected_index = len(self.options) - 1
            else:
                self.selected_index = (self.selected_index - 1) % len(self.options)
            return True
        elif event.key == pygame.K_DOWN:
            self.selected_index = (self.selected_index + 1) % len(self.options)
            return True
        elif event.key == pygame.K_RETURN:
            if self.selected_index >= 0:
                self.expanded = False
            return True
        elif event.key == pygame.K_ESCAPE:
            self.expanded = False
            return True
        return False

    def selected_value(self):
        """Return the currently selected username, or None."""
        if 0 <= self.selected_index < len(self.options):
            return self.options[self.selected_index]
        return None

    def _item_rects(self):
        """Return the rects for the expanded option list."""
        start_y = self.rect.bottom + 4
        return [
            pygame.Rect(self.rect.x, start_y + i * self.item_height,
                        self.rect.width, self.item_height - 4)
            for i in range(min(len(self.options), self.max_visible))
        ]

    def draw(self):
        """Draw the collapsed box and, if open, the option list."""
        if not self.options:
            return
        pygame.draw.rect(self.screen, self.bg_color, self.rect, border_radius=6)
        pygame.draw.rect(self.screen, self.border_color, self.rect, 2, border_radius=6)
        label = self.selected_value() or "Select existing user..."
        label_img = self.font.render(label, True, self.text_color)
        label_rect = label_img.get_rect(midleft=(self.rect.x + 10, self.rect.centery))
        self.screen.blit(label_img, label_rect)

        if self.expanded:
            for i, item_rect in enumerate(self._item_rects()):
                if i == self.selected_index:
                    pygame.draw.rect(self.screen, self.highlight_color, item_rect, border_radius=4)
                    text_color = (255, 255, 255)
                else:
                    pygame.draw.rect(self.screen, self.bg_color, item_rect, border_radius=4)
                    text_color = self.text_color
                item_img = self.font.render(self.options[i], True, text_color)
                item_rect_img = item_img.get_rect(
                    midleft=(item_rect.x + 10, item_rect.centery))
                self.screen.blit(item_img, item_rect_img)
                pygame.draw.rect(self.screen, self.border_color, item_rect, 1, border_radius=4)
