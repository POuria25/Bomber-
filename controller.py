import pygame
from state import State
from view import View
from physics import Physics
from constants import *


class Controller:

    def __init__(self):
        self.state = State()
        self.view = View((800, 600))
        self.physics = Physics()
        self.clouds = [(800, 100), (600, 150), (400, 200)]
        print("[INIT] Controller initialized")

    def run(self):
        """Main game loop."""
        print("[RUN] Game loop started")
        while True:
            self.handle_event()
            self.update_game()
            self.render_game()

    def handle_event(self):
        """Handle user inputs and events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEMOTION:
                self.state.plane_altitude = max(
                    min(event.pos[1], self.view.dimensions[1] - 70), 50
                )
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    print("[KEYDOWN] B pressed: Adding bomb")
                    self.add_bomb()
                elif event.key == pygame.K_a:
                    self.state.autoBomb = True
                    print("[KEYDOWN] A pressed: Attempting auto-fire")

    def add_bomb(self, position=None):
        """Add a bomb to the state."""
        if position is None:
            position = (self.view.dimensions[0] // 2, self.state.plane_altitude + 20)

        current_time = pygame.time.get_ticks()  # Capture the current time

        bomb_data = {
            "initial_position": position,
            "vertical_acceleration": GRAVITY,
            "initial_depart": current_time,  # Add the time the bomb was dropped
        }
        self.state.add_bomb(bomb_data)
        print(f"[ADD BOMB] Bomb added at position: {position}, time: {current_time}")

    def update_flag_position(self):
        """Update the flag's position based on its speed."""

        flag_x = self.state.flag_position[0]
        flag_x -= FLAG_SPEED  # Move the flag to the left
        
        if flag_x < 0:
            flag_x = self.view.dimensions[0]

        self.state.flag_position = (flag_x, self.view.dimensions[1] - 50)
        flag_y = self.view.dimensions[1] - 50  # Position the flag above the ground
        self.state.flag_position = (flag_x, flag_y)
        if(flag_x == 0):
            print(f"[UPDATE FLAG] Flag position updated to: {flag_x}")
            exit()

    def attempt_automatic_fire(self):
        """Automatically add a bomb if the distance between the plane and the flag is below the threshold."""

        current_time = pygame.time.get_ticks()

        if current_time < self.state.autoBomb_time:
            return

        if self.state.autoBomb == True:
            print("waiting to drop")
            plane_x = self.view.dimensions[0] // 2
            plane_y = self.state.plane_altitude
            flag_x, flag_y = self.state.flag_position

            # Calculate the time and position to drop the bomb
            time_to_fall, drop_position = self.physics.calculate_drop_time_and_position(
                plane_altitude=plane_y,
                flag_position=flag_x,
                plane_speed=FLAG_SPEED,
                gravity=GRAVITY,
            )

            # Calculate horizontal and vertical distances
            horizontal_distance = abs(plane_x - flag_x)
            vertical_distance = abs(plane_y - flag_y)
        print(plane_x, "---", flag_x, "----", plane_x - flag_x)
        if abs(plane_x - flag_x) <= 100:  # Allow small error margin
            print(f"[AUTO-FIRE] Dropping bomb at position: {plane_x}")
            self.add_bomb()
            # Reset cooldown timer
            self.state.autoBomb_time = current_time + AUTO_BOMB_INTERVAL

    def update_game(self):
        """Update the game state."""
        current_time = pygame.time.get_ticks()
        bombs_to_remove = []

        # Update bombs' positions
        for bomb in self.state.bombs:
            try:
                # Calculate new vertical position
                elapsed_time = (
                    current_time - bomb["initial_depart"]
                )  # Convert to seconds
                new_y_position = self.physics.compute_position(
                    bomb["initial_position"][1],
                    elapsed_time,
                    bomb["vertical_acceleration"],
                )

                # Update the bomb's position
                bomb["initial_position"] = (bomb["initial_position"][0], new_y_position)

                # Remove bombs that hit the ground
                if new_y_position >= self.view.dimensions[1]:
                    bombs_to_remove.append(bomb)
                    print(
                        f"[UPDATE GAME] Bomb hit the ground at: {bomb['initial_position']}"
                    )
            except Exception as e:
                print(f"[ERROR] Unexpected error updating bomb: {e}")

        # Remove bombs that have hit the ground
        for bomb in bombs_to_remove:
            self.state.bombs.remove(bomb)

        # Check automatic bomb-dropping conditions
        if self.state.autoBomb:
            self.attempt_automatic_fire()

        # Update the flag's position
        self.update_flag_position()

        # Placeholder for updating the plane's motion
        self.update_plane_motion()

    def update_plane_motion(self):
        """Update the plane's velocity and acceleration."""
        # Placeholder: Update plane velocity and acceleration if needed
        # print("[PLANE MOTION] Updated plane dynamics")

    def render_game(self):
        """Render the game."""
        self.view.draw()
        self.view.draw_plane(self.state.plane_altitude)
        self.view.draw_clouds(self.clouds, pygame.time.get_ticks())
        self.view.draw_ground(pygame.time.get_ticks())
        self.view.draw_flag(pygame.time.get_ticks())  # Pass the correct current time

        for bomb in self.state.bombs:
            self.view.draw_bombs(bomb["initial_position"])

        self.view.update_display()
