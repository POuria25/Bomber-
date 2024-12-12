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
        self.next_autoBomb_time = 0  # Initialize next auto-bomb time
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
                    print("[KEYDOWN] A pressed: Attempting auto-fire")
                    self.attempt_automatic_fire()

    def add_bomb(self, position=None):
        """Add a bomb to the state."""
        if position is None:
            position = (self.view.dimensions[0] // 2, self.state.plane_altitude + 20)
        bomb_data = {
            "initial_position": position,
            "initial_depart": pygame.time.get_ticks(),
            "vertical_acceleration": GRAVITY,
        }
        self.state.add_bomb(bomb_data)
        print(f"[ADD BOMB] Bomb added at position: {position}")

    def update_flag_position(self, current_time):
        """Update the flag's position."""
        flag_x = int(-current_time * FLAG_SPEED) % self.view.dimensions[0]
        self.state.flag_position = (flag_x, self.view.dimensions[1])
        print(f"[UPDATE FLAG] Flag position updated to: {self.state.flag_position}")

    def update_game(self):
        """Update the game state."""
        current_time = pygame.time.get_ticks()
        bombs_to_remove = []

        # Check if it's time for an automatic bomb
        if self.state.autoBomb and self.state.autoBomb_time and current_time >= self.state.autoBomb_time:
            position = (self.view.dimensions[0] // 2, self.state.plane_altitude + 20)
            self.add_bomb(position)
            self.next_auto_bomb_time = 0  # Reset the auto-fire timer

            print(
                f"[AUTO-BOMB] Auto-bomb triggered at: {current_time}, Scheduled time: {self.state.autoBomb_time}"
            )
            # Reset the auto-bomb time after the bomb is added
            self.state.autoBomb_time = None

        for bomb in self.state.bombs:
            try:
                # Calculate elapsed time in seconds
                elapsed_time = current_time - bomb["initial_depart"]
                print(f"[UPDATE GAME] Elapsed time for bomb: {elapsed_time:.2f}s")

                # Update the bomb's vertical position
                new_y_position = self.physics.compute_position(
                    bomb["initial_position"][1],
                    elapsed_time,
                    bomb["vertical_acceleration"],
                )
                bomb["initial_position"] = (bomb["initial_position"][0], new_y_position)
                print(
                    f"[UPDATE GAME] Bomb position updated to: {bomb['initial_position']}"
                )

                # Check if the bomb has hit the ground
                if new_y_position >= self.view.dimensions[1]:
                    bombs_to_remove.append(bomb)

                    print(
                        f"[UPDATE GAME] Bomb hit the ground: {bomb['initial_position']}"
                    )

            except Exception as e:
                print(f"[ERROR] Unexpected error during bomb processing: {e}")

        # Remove bombs that have hit the ground
        for bomb in bombs_to_remove:
            self.state.bombs.remove(bomb)
            print(f"[REMOVE BOMB] Bomb removed: {bomb}")

        # print(f"[DEBUG] Number of bombs: {len(self.state.bombs)}")

        # Update the flag's position
        self.update_flag_position(current_time)

        # Update clouds
        for i in range(len(self.clouds)):
            self.clouds[i] = (self.clouds[i][0] - 1, self.clouds[i][1])
            if self.clouds[i][0] < -50:
                self.clouds[i] = (self.view.dimensions[0], self.clouds[i][1])
            # print(f"[UPDATE CLOUDS] Cloud {i} position: {self.clouds[i]}")

        # Update plane velocity and acceleration
        velocity = self.physics.compute_velocity(
            self.state.plane_altitude,
            self.state.previous_altitude,
            current_time,
            self.state.previous_time,
        )
        acceleration = self.physics.calculate_acceleration(
            velocity,
            self.state.previous_velocity,
            current_time,
            self.state.previous_time,
        )

        self.state.previous_altitude = self.state.plane_altitude
        self.state.previous_velocity = velocity
        self.state.previous_time = current_time
        self.state.velocity = velocity
        self.state.acceleration = acceleration
        # print(f"[DEBUG] Plane velocity: {velocity}, acceleration: {acceleration}")

    def render_game(self):
        """Render the game."""
        self.view.draw()
        self.view.draw_plane(self.state.plane_altitude)
        self.view.draw_clouds(self.clouds, pygame.time.get_ticks())
        self.view.draw_variometer(20, 50, self.state.velocity)
        self.view.draw_accelerometer(70, 50, self.state.acceleration)
        self.view.draw_ground(pygame.time.get_ticks())
        self.view.draw_flag(pygame.time.get_ticks())

        # Draw each bomb at its current position
        for bomb in self.state.bombs:
            self.view.draw_bombs(bomb["initial_position"])
            print(f"[RENDER GAME] Bomb drawn at: {bomb['initial_position']}")

        self.view.update_display()
        # print("[RENDER GAME] Display updated")

    def attempt_automatic_fire(self):
        """Automatically add a bomb based on calculations."""
        current_time = pygame.time.get_ticks()

        # Check if the automatic bomb is already armed and time has passed
        if self.state.autoBomb and self.state.autoBomb_time is not None and current_time < self.state.autoBomb_time:

            return  # Wait until the scheduled time for the next bomb

            # Check if the automatic bomb is already armed and time has passed

        # Example parameters for firing
        start_height = self.state.plane_altitude
        target_height = self.view.dimensions[1]
        acceleration = GRAVITY
        horizontal_speed = 0.2
        distance = self.view.dimensions[0]

        # Calculate if automatic fire is possible
        fire_possible, time_to_target = self.physics.calculate_fire_time(
            start_height=start_height,
            target_height=target_height,
            acceleration=acceleration,
            horizontal_speed=horizontal_speed,
            distance=distance,
        )

        if fire_possible:
            print(f"[AUTO-FIRE] Automatic fire scheduled in {time_to_target:.2f}s")
            self.state.arm_automatic_fire(current_time + int(time_to_target))
            self.state.autoBomb = True
        else:
            print("[AUTO-FIRE] Automatic fire not possible")
            
