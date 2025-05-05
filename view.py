import pygame
import math
from constants import *

class View:
    def __init__(self, dimensions):
        """Initialize the view with given window dimensions."""
        pygame.init()
        pygame.display.set_caption("B2 - Bomber")
        
        self.screen = pygame.display.set_mode(dimensions)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 16)
        self.dimensions = dimensions
        self.text_size = 16

        # Load images
        try:
            self.plane_image = pygame.image.load("plane.png").convert_alpha()
            self.cloud_image = pygame.image.load("cloud.png").convert_alpha()
            self.bomb_image = pygame.image.load("bomb.png").convert_alpha()
            self.explosion_image = pygame.image.load("explosion.png").convert_alpha()
        except pygame.error as e:
            print(f"Error loading images: {e}")
            exit()

        # View properties
        self.ground_height = 20
        self.variometer_value = 0.0
        self.accelerometer_value = 0.0

    def draw(self):
        """Fill the screen with the background color."""
        self.screen.fill(LIGHTBLUE)

    def draw_plane(self, altitude):
        """
        Draw the plane at the given altitude.
        
        Args:
            altitude: Vertical position of the plane
        """
        x = (self.dimensions[0] - self.plane_image.get_width()) // 2
        y = int(altitude) - self.plane_image.get_height() // 2
        self.screen.blit(self.plane_image, (x, y))

    def draw_bombs(self, position):
        """
        Draw a bomb at the given position.
        
        Args:
            position: (x, y) coordinates for the bomb
        """
        #pygame.draw.circle(self.screen, ORANGE, list(map(int, position)), 10)
        self.screen.blit(self.bomb_image, (position[0], position[1]))

    def draw_explosion(self, position):
        """
        Draw an explosion at the given position.
        
        Args:
            position: (x, y) coordinates for the explosion
        """
        self.screen.blit(self.explosion_image, (position[0], position[1]))

    def draw_clouds(self, clouds, current_time):
        """
        Draw clouds with horizontal movement based on time.
        
        Args:
            clouds: List of cloud positions (x, y)
            current_time: Current time in milliseconds
        """
        cloud_width = self.cloud_image.get_width()
        background_period = self.dimensions[0] + cloud_width
        
        for cloud in clouds:
            x = (int(cloud[0] - current_time * HORIZONTAL_SPEED) 
                 % background_period - cloud_width)
            y = cloud[1]
            self.screen.blit(self.cloud_image, (x, y))

    def draw_ground(self, current_time):
        """
        Draw the undulating ground.
        
        Args:
            current_time: Current time in milliseconds
        """
        background_period = self.dimensions[0] + 200  # Match the original
        
        for x in range(self.dimensions[0]):
            alpha = ((-x - current_time * HORIZONTAL_SPEED) 
                    * 2.0 * math.pi / background_period)
            y = self.ground_height * math.exp(math.cos(alpha)) / math.e
            pygame.draw.rect(self.screen, GREEN, 
                            ((x, self.dimensions[1] - y), (1, y)))

    def draw_flag(self, current_time):
        """
        Draw a flag with horizontal movement based on time.
        
        """
        x = int(-current_time * HORIZONTAL_SPEED) % self.dimensions[0]  # Incorrect

        background_period = self.dimensions[0] + self.cloud_image.get_width()
        x = int(-current_time * HORIZONTAL_SPEED) % background_period
    
        # Draw flag pole
        pygame.draw.rect(self.screen, BLACK, 
                        ((x, self.dimensions[1] - 50), (3, 40)))

        # Draw flag triangle
        pygame.draw.polygon(self.screen, RED, [
            (x, self.dimensions[1] - 45),
            (x, self.dimensions[1] - 25),
            (x + 20, self.dimensions[1] - 35)
        ])

    def display_text(self, x, y, text, color):
        """
        Display text at the given position.
        
        Args:
            x: Horizontal position
            y: Vertical position
            text: Text to display
            color: RGB color tuple
        """
        text_image = self.font.render(text, True, color)
        self.screen.blit(text_image, (x, y))

    def draw_variometer(self, x, y, velocity):
        """
        Draw the vertical velocity indicator.
        
        Args:
            x: Horizontal position
            y: Vertical position
            velocity: Current vertical velocity
        """
        # Smooth the value for display
        self.variometer_value = 0.8 * self.variometer_value + 0.2 * velocity
        
        height = 100
        width = 40
        thickness = 2
        
        # Calculate indicator position
        indicator = int((self.variometer_value + 1.0) * height / 2.0)
        
        # Clamp indicator position
        if indicator < thickness:
            indicator = thickness
        elif indicator >= height - thickness:
            indicator = height - thickness
        
        # Draw labels
        self.display_text(x + 10, y - 20, "Vy", BLACK)
        self.display_text(x - 20, y + (height - self.text_size) // 2, "0-", BLACK)
        
        # Draw variometer background
        pygame.draw.rect(self.screen, BLACK, ((x, y), (width, height)))
        
        # Draw indicator bar
        pygame.draw.rect(self.screen, GREEN, 
                        ((x, y + height - indicator - thickness), 
                         (width, 2 * thickness)))

    def draw_accelerometer(self, x, y, acceleration):
        """
        Draw the vertical acceleration indicator.
        
        Args:
            x: Horizontal position
            y: Vertical position
            acceleration: Current vertical acceleration
        """
        # Apply gain and smoothing for display
        GAIN = 200
        self.accelerometer_value = 0.8 * self.accelerometer_value + 0.2 * acceleration * GAIN
        
        height = 100
        width = 40
        thickness = 2
        
        # Calculate indicator position
        indicator = int((self.accelerometer_value + 1.0) * height / 2.0)
        
        # Clamp indicator position
        if indicator < thickness:
            indicator = thickness
        elif indicator >= height - thickness:
            indicator = height - thickness
        
        # Draw labels
        self.display_text(x + 10, y - 20, "Ay", BLACK)
        self.display_text(x - 20, y + (height - self.text_size) // 2, "0-", BLACK)
        
        # Draw accelerometer background
        pygame.draw.rect(self.screen, BLACK, ((x, y), (width, height)))
        
        # Draw indicator bar
        pygame.draw.rect(self.screen, RED, 
                        ((x, y + height - indicator - thickness), 
                         (width, 2 * thickness)))

    def update_display(self):
        """Update the screen and control frame rate."""
        pygame.display.flip()
        self.clock.tick(FPS)
        
    def draw_explosion(self, position):
        """
        Draw an explosion at the given position.
    
        Args:
            position: (x, y) coordinates for the explosion
        """
        # Center the explosion image at the given position
        x = int(position[0] - self.explosion_image.get_width() // 2)
        y = int(position[1] - self.explosion_image.get_height()) + 20
        self.screen.blit(self.explosion_image, (x, y))