import pygame
from pathlib import Path

from .snake import Snake
from .food import Food

# Game Engine

WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (220, 60, 60)

DIFFICULTIES = {
    "Easy": 5,
    "Medium": 8,
    "Hard": 12,
}

DIFFICULTY_KEYS = {
    pygame.K_1: DIFFICULTIES["Easy"],
    pygame.K_2: DIFFICULTIES["Medium"],
    pygame.K_3: DIFFICULTIES["Hard"],
}

for key_name, difficulty_key in (("K_KP1", pygame.K_1), ("K_KP2", pygame.K_2), ("K_KP3", pygame.K_3)):
    keypad_key = getattr(pygame, key_name, None)
    if keypad_key is not None:
        DIFFICULTY_KEYS[keypad_key] = DIFFICULTY_KEYS[difficulty_key]

EXIT_KEYS = {pygame.K_4, pygame.K_ESCAPE}
keypad_four = getattr(pygame, "K_KP4", None)
if keypad_four is not None:
    EXIT_KEYS.add(keypad_four)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cell_size = 20
        self.grid_width = width // self.cell_size
        self.grid_height = height // self.cell_size

        self.snake = Snake(self.grid_width // 2, self.grid_height // 2, self.cell_size)
        self.food = Food(self.grid_width, self.grid_height, self.cell_size)

        self.score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.game_over_font = pygame.font.SysFont("Arial", 64, bold=True)
        self.game_over_message_font = pygame.font.SysFont("Arial", 28)

        self.moves_per_second = 8
        self._frame_counter = 0

        self.game_over = False
        self.quit_requested = False

        self.eat_sound = None
        self.game_over_sound = None
        self._initialize_audio()

    def _initialize_audio(self):
        try:
            if pygame.mixer.get_init() is None:
                pygame.mixer.init()

            sounds_directory = Path(__file__).resolve().parent.parent / "sounds"
            self.eat_sound = pygame.mixer.Sound(sounds_directory / "eat.wav")
            self.game_over_sound = pygame.mixer.Sound(sounds_directory / "game_over.wav")
        except (pygame.error, OSError):
            self.eat_sound = None
            self.game_over_sound = None

    def _set_game_over(self):
        if self.game_over:
            return

        self.game_over = True
        if self.game_over_sound is not None:
            self.game_over_sound.play()

    def handle_keydown(self, key):
        if self.game_over:
            if key in DIFFICULTY_KEYS:
                self.restart(DIFFICULTY_KEYS[key])
            elif key in EXIT_KEYS:
                self.quit_requested = True
            return

        # Direction changes are applied immediately on key press.
        if key in (pygame.K_UP, pygame.K_w):
            self.snake.set_direction(0, -1)
        elif key in (pygame.K_DOWN, pygame.K_s):
            self.snake.set_direction(0, 1)
        elif key in (pygame.K_LEFT, pygame.K_a):
            self.snake.set_direction(-1, 0)
        elif key in (pygame.K_RIGHT, pygame.K_d):
            self.snake.set_direction(1, 0)

    def restart(self, moves_per_second):
        self.snake = Snake(self.grid_width // 2, self.grid_height // 2, self.cell_size)
        self.food.respawn(self.snake.body)
        self.score = 0
        self.moves_per_second = moves_per_second
        self._frame_counter = 0
        self.game_over = False
        self.quit_requested = False

    def handle_input(self):
        # Reserved for continuously-held-key input (not used for a
        # grid-based snake, but kept here to mirror the engine's shape).
        pass

    def update(self):
        if self.game_over:
            return

        self._frame_counter += 1
        frames_per_move = max(1, 60 // self.moves_per_second)
        if self._frame_counter < frames_per_move:
            return
        self._frame_counter = 0

        self.snake.move()

        if self.snake.collides_with_wall(self.grid_width, self.grid_height):
            self._set_game_over()
            return

        if self.snake.collides_with_self():
            self._set_game_over()
            return

        if self.snake.head_rect().colliderect(self.food.rect()):
            self.snake.grow()
            self.score += 1
            if self.eat_sound is not None:
                self.eat_sound.play()
            self.food.respawn(self.snake.body)

    def render(self, screen):
        # Draw food
        pygame.draw.rect(screen, RED, self.food.rect())

        # Draw snake
        for rect in self.snake.segment_rects():
            pygame.draw.rect(screen, GREEN, rect)

        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        if self.game_over:
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 190))
            screen.blit(overlay, (0, 0))

            game_over_text = self.game_over_font.render("GAME OVER", True, WHITE)
            score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
            menu_lines = [
                "Play again:",
                "1 - Easy",
                "2 - Medium",
                "3 - Hard",
                "4 or ESC - Exit",
            ]

            screen.blit(
                game_over_text,
                game_over_text.get_rect(center=(self.width // 2, self.height // 2 - 70)),
            )
            screen.blit(
                score_text,
                score_text.get_rect(center=(self.width // 2, self.height // 2)),
            )
            for line_number, line in enumerate(menu_lines):
                menu_text = self.game_over_message_font.render(line, True, WHITE)
                menu_y = self.height // 2 + 55 + line_number * 34
                screen.blit(menu_text, menu_text.get_rect(center=(self.width // 2, menu_y)))
