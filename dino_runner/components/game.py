import pygame

from dino_runner.utils.constants import (
    BG,
    ICON,
    IMG_BACKGROUND,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TITLE,
    FPS,
    DEFAULT_TYPE,
)
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager

FONT_STYLE = "freesansbold.ttf"
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
BACKGROUND_COLOR = (153, 255, 204)
RED_COLOR = (255,0,0)

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.running = False
        self.game_speed = 20
        self.score = 0
        self.death_count = 0
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()

    def print_text(self, font_size, text_content, color, position):
        font = pygame.font.Font(FONT_STYLE, font_size)
        text = font.render(text_content, True, color)
        text_rect = text.get_rect()
        text_rect.center = position
        self.screen.blit(text, text_rect)

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()
        pygame.display.quit()
        pygame.quit()

    def run(self):
        self.playing = True
        pygame.mixer.music.play(-1)
        self.score = 0
        self.game_speed = 20
        self.obstacle_manager.reset_obstacles()
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        pass
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.power_up_manager.update(self)
        self.update_score()

    def update_score(self):
        self.score += 1
        if self.score % 100 == 0:
            self.game_speed += 2

    def draw(self):
        self.clock.tick(FPS)
        self.screen.blit(IMG_BACKGROUND, (0, 0))
        self.draw_background()
        self.player.draw(self.screen)
        self.draw_score()
        self.draw_power_up_time()
        self.obstacle_manager.draw(self.screen)
        self.power_up_manager.draw(self.screen)
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def draw_score(self):
        font = pygame.font.Font(FONT_STYLE, 22)
        text = font.render(f"Score: {self.score}", True, BLACK_COLOR)
        text_rect = text.get_rect()
        text_rect.center = (1020, 25)
        self.screen.blit(text, text_rect)

    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round(
                (self.player.power_up_time - pygame.time.get_ticks()) / 1000, 1
            )
            if time_to_show >= 0:
                self.print_text(
                    18,
                    f"{self.player.type.capitalize()} enabled for {time_to_show} seconds",
                    BLACK_COLOR,
                    (500, 40),
                )
            else:
                self.player.has_power_up = False
                self.player.type = DEFAULT_TYPE

    def show_menu(self):
        self.screen.fill(RED_COLOR)
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2

        if self.death_count == 0:
            self.print_text(
                22,
                "Press any key to start",
                BLACK_COLOR,
                (half_screen_width, half_screen_height),
            )

        else:
            self.screen.blit(ICON, (half_screen_width - 20, half_screen_height - 140))

            if self.death_count > 1:
                self.print_text(
                    22,
                    "You lost :( ",
                    BLACK_COLOR,
                    (half_screen_width, half_screen_height),
                )
                self.print_text(
                    20,
                    f"The number of times you dead is: {self.death_count} and score : {self.score}",
                    BLACK_COLOR,
                    (half_screen_width, half_screen_height + 30),
                )
                self.print_text(
                    20,
                    "Press to restart",
                    BLACK_COLOR,
                    (half_screen_width, half_screen_height + 60),
                )

            else:
                self.print_text(
                    22,
                    "You lost :( ",
                    BLACK_COLOR,
                    (half_screen_width, half_screen_height),
                )
                self.print_text(
                    20,
                    f"Your score is {self.score}",
                    BLACK_COLOR,
                    (half_screen_width, half_screen_height + 30),
                )
                self.print_text(
                    20,
                    "Press to restart",
                    BLACK_COLOR,
                    (half_screen_width, half_screen_height + 60),
                )

        pygame.display.update()
        self.handle_events_on_menu()

    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.run()
