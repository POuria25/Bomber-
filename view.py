import pygame
import math
from constants import *

class View:
    def __init__(self, dimensions):
        pygame.init()
        self.screen = pygame.display.set_mode(dimensions)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 16)
        self.dimensions = dimensions

        # Load the plane and cloud images
        try:
            self.plane_image = pygame.image.load("plane.png").convert_alpha()
            self.cloud_image = pygame.image.load("cloud.png").convert_alpha()
        except pygame.error as e:
            print(f"Error loading images: {e}")
            exit()

        self.ground_height = 20
        self.variometer_value = 0
        self.accelerometer_value = 0

    def draw(self):
        """
        Fill the screen with the LIGHTBLUE.
        """
        self.screen.fill(LIGHTBLUE)

    def draw_plane(self, altitude):
        """
        Draw the plane at the given altitude.

        Args:
            altitude (_type_): _description_
        """
        x = (self.dimensions[0] - self.plane_image.get_width()) // 2
        y = int(altitude) - self.plane_image.get_height() // 2
        self.screen.blit(self.plane_image, (x, y))

    def draw_bombs(self, position):
        """
        Draw bombs at the given position.

        Args:
            position (_type_): _description_
        """
        pygame.draw.circle(self.screen, ORANGE, list(map(int, position)), 10)


    def draw_clouds(self, clouds, current_time):
        """
        Drawing clouds at the given position.

        Args:
            clouds (_type_): _description_
            current_time (_type_): _description_
        """
        cloud_width = self.cloud_image.get_width()
        for cloud in clouds:
            x = (int(cloud[0] - current_time * 0.125) % (self.dimensions[0] + cloud_width) - cloud_width)
            y = cloud[1]
            self.screen.blit(self.cloud_image, (x, y))

    def draw_ground(self, current_time):
        """
        Drawing ground at the given position.

        Args:
            current_time (_type_): _description_
        """
        for x in range(self.dimensions[0]):
            alpha = ((-x - current_time * 0.125) * 2.0 * math.pi / (self.dimensions[0] + 200))
            y = self.ground_height * math.exp(math.cos(alpha)) / math.e
            pygame.draw.rect(self.screen, GREEN, ((x, self.dimensions[1] - y), (1, y)))

    def draw_flag(self, current_time):
        """
        Drawing flag at the given position

        Args:
            current_time (_type_): _description_
        """
        x = int(-current_time * 0.125) % self.dimensions[0]
        pygame.draw.polygon(self.screen, RED, [
            (x, self.dimensions[1] - 45),
            (x, self.dimensions[1] - 25),
            (x + 20, self.dimensions[1] - 35)
        ])
        pygame.draw.rect(self.screen, BLACK, ((x, self.dimensions[1] - 50), (3, 40)))

    def display_text(self, x, y, text, color):
        """
        Display text at the given position.

        Args:
            x (_type_): _description_
            y (_type_): _description_
            text (_type_): _description_
            color (_type_): _description_
        """
        text_image = self.font.render(text, True, color)
        self.screen.blit(text_image, (x, y))

    def draw_variometer(self, x, y, velocity):
        """
        Drawing variometer at the given position.

        Args:
            x (_type_): _description_
            y (_type_): _description_
            velocity (_type_): _description_
        """
        self.variometer_value = 0.8 * self.variometer_value + 0.2 * velocity
        height = 100
        width = 40
        thickness = 2

        indicator = int((self.variometer_value + 1.0) * height / 2.0)
        indicator = max(min(indicator, height - thickness), thickness)

        self.display_text(x + 10, y - 20, "Vy", BLACK)
        pygame.draw.rect(self.screen, BLACK, ((x, y), (width, height)))
        pygame.draw.rect(self.screen, GREEN, ((x, y + height - indicator - thickness), (width, thickness * 2)))

    def draw_accelerometer(self, x, y, acceleration):
        
        """
        Drawing accelerometer at the given position.
        
        Args:
            x (_type_): _description_
            y (_type_): _description_
            acceleration (_type_): _description_
        """
        GAIN = 200
        self.accelerometer_value = 0.8 * self.accelerometer_value + 0.2 * acceleration * GAIN
        height = 100
        width = 40
        thickness = 2

        indicator = int((self.accelerometer_value + 1.0) * height / 2.0)
        indicator = max(min(indicator, height - thickness), thickness)

        self.display_text(x + 10, y - 20, "Ay", BLACK)
        pygame.draw.rect(self.screen, BLACK, ((x, y), (width, height)))
        pygame.draw.rect(self.screen, RED, ((x, y + height - indicator - thickness), (width, thickness * 2)))

    def update_display(self):
        pygame.display.flip()
        self.clock.tick(25)
