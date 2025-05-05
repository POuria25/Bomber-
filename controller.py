import pygame
import math
from state import State
from view import View
from physics import Physics
from constants import *


class Controller:

    def __init__(self):
        self.state = State()
        self.view = View((800, 600))
        self.physics = Physics()
        self.clouds = [(0, 100), (600, 300), (200, 350)]
        self.background_period = self.view.dimensions[0] + self.view.cloud_image.get_width()

    def run(self):
        """B52 - Bomber."""
        # Initialize previous values for physics calculations
        current_time = pygame.time.get_ticks()
        self.state.previous_time = current_time
        self.state.previous_altitude = self.state.plane_altitude
        
        while True:
            self.handle_event()
            self.update_game()
            self.render_game()

    def handle_event(self):
        """Handle user inputs and events."""
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEMOTION:
                # Apply smoothing to plane altitude
                target_altitude = event.pos[1]
                max_altitude = self.view.dimensions[1] - 50 - self.view.plane_image.get_height() // 2
                if target_altitude > max_altitude:
                    target_altitude = max_altitude
                
                self.state.plane_altitude = (self.state.plane_altitude * 5.0 + target_altitude) / 6.0
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    self.add_bomb()
                elif event.key == pygame.K_a:
                    self.try_automatic_fire()

    def add_bomb(self):
        """Add a bomb to the state."""
        current_time = pygame.time.get_ticks()
        
        # Calculate offset from the plane's center for bomb dropping
        offset = self.view.plane_image.get_height() // 2 - 10
        
        position = (self.view.dimensions[0] // 2, self.state.plane_altitude + offset)

        bomb_data = {
            "initial_position": position,
            "vertical_acceleration": GRAVITY,
            "initial_depart": current_time,
        }
        self.state.add_bomb(bomb_data)

    def try_automatic_fire(self):
        """Try to arm automatic fire based on timing calculations."""
        current_time = pygame.time.get_ticks()
        
        # Calculate when the flag will next be at a position where a bomb can hit it
        period = self.background_period / HORIZONTAL_SPEED
        next_target_time = -self.view.dimensions[0] / (2.0 * HORIZONTAL_SPEED)
        
        while next_target_time < current_time:
            next_target_time += period
        
        # Calculate bomb drop offset
        offset = self.view.plane_image.get_height() // 2 - 10
        
        # Check if a hit is possible and calculate the fire time
        can_hit, fire_time = self.physics.calculate_fire(
            self.state.plane_altitude + offset,
            self.view.dimensions[1],
            GRAVITY,
            next_target_time,
            current_time
        )
        
        if can_hit:
            self.state.arm_automatic_fire(fire_time)

    def update_game(self):
        """Update the game state."""
        current_time = pygame.time.get_ticks()
        
        # Calculate velocity and acceleration
        velocity, acceleration = self.physics.calculate_velocity_acceleration(
            self.state.plane_altitude,
            current_time,
            self.state.previous_altitude,
            self.state.previous_time,
            self.state.previous_velocity
        )
        
        # Update state with new values
        self.state.velocity = velocity
        self.state.acceleration = acceleration
        self.state.previous_altitude = self.state.plane_altitude
        self.state.previous_velocity = velocity
        self.state.previous_time = current_time
        
        # Check if it's time for automatic fire
        if self.state.autoBomb and self.state.autoBomb_time <= current_time:
            self.add_bomb()
            self.state.autoBomb = False
        
        # Update bombs position and remove old ones
        self.update_bombs(current_time)
        self.state.remove_bombs(current_time)
        self.state.remove_explosions(current_time)

    def update_bombs(self, current_time):
        """Update the positions of all bombs and check for ground contact."""
        ground_level = self.view.dimensions[1] - self.view.ground_height  # More accurate ground level
    
        for bomb in self.state.bombs:
            # Calculate new position using MRUA physics
            new_y = self.physics.mrua_1d(
                bomb["initial_position"][1],
                bomb["initial_depart"],
                bomb["vertical_acceleration"],
                current_time
            )
        
            # Check if bomb hit the ground
            if new_y >= ground_level:
                # Create explosion at ground level with the same x-coordinate
                explosion_pos = (bomb["initial_position"][0], ground_level)
                self.state.add_explosion(explosion_pos, current_time)
            
                # Mark bomb as hit ground so it can be removed
                bomb["hit_ground"] = True
            else:
                # Update bomb position (x position stays constant)
                bomb["current_position"] = (bomb["initial_position"][0], new_y)

    def render_game(self):
        """Render the game."""
        current_time = pygame.time.get_ticks()
        
        self.view.draw()
        self.view.draw_clouds(self.clouds, current_time)
        
        # Draw all bombs with their current positions
        for bomb in self.state.bombs:
            position = bomb.get("current_position", bomb["initial_position"])
            self.view.draw_bombs(position)
        
        # Draw ground and flag
        self.view.draw_ground(current_time)
        self.view.draw_flag(current_time)
        
        # Draw all explosions
        for explosion in self.state.explosions:
            self.view.draw_explosion(explosion["position"])
        
        # Draw plane and instruments
        self.view.draw_plane(self.state.plane_altitude)
        
        # Draw instruments
        self.view.draw_variometer(self.view.dimensions[0] // 20, 
                                  self.view.dimensions[1] // 10, 
                                  self.state.velocity)
        
        self.view.draw_accelerometer(self.view.dimensions[0] * 3 // 20, 
                                     self.view.dimensions[1] // 10, 
                                     self.state.acceleration)
        
        # Display auto-fire status if armed
        if self.state.autoBomb:
            self.view.display_text(self.view.dimensions[0] // 20,
                                  3 * self.view.dimensions[1] // 10,
                                  "Auto Bombing", BLACK)
        
        # Update the display
        self.view.update_display()