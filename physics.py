import math


class Physics:

    def compute_position(self, initial_position, elapsed_time, acceleration):
        """
        Computes the new vertical position based on the formula:
        y = y0 + 0.5 * a * t^2
        """
        return initial_position + 0.5 * acceleration * ((elapsed_time) ** 2)



    def compute_velocity(self, position, previous_position, current_time, previous_time):
        """
        Computes the velocity of an object, avoiding division by zero.
        """
        time_difference = current_time - previous_time
        if time_difference == 0:
            return 0  # If no time has elapsed, velocity is zero
        return (position - previous_position) / time_difference


    def calculate_velocity_acceleration(
        self,
        altitude,
        current_time,
        previous_position,
        previous_time,
        previous_velocity,
    ):
        """
        Calculate velocity and acceleration based on altitude and time.
        """
        velocity = -(altitude - previous_position) / (current_time - previous_time)
        acceleration = (velocity - previous_velocity) / (current_time - previous_time)

        return velocity, acceleration

    def calculate_acceleration(self, velocity, previous_velocity, current_time, previous_time):
        """
        Calculates acceleration, avoiding division by zero.
        """
        time_difference = current_time - previous_time
        if time_difference == 0:
            return 0  # Acceleration is zero if no time has passed
        return (velocity - previous_velocity) / time_difference


    def calculate_fire_time(self, start_height, target_height, acceleration, horizontal_speed, distance):
        
        if horizontal_speed == 0:
            return False, 0

        vertical_displacement = target_height - start_height
        if vertical_displacement >= 0:
            time_to_target_vertical = math.sqrt(2 * abs(vertical_displacement) / acceleration)
        else:
            return False, 0

        time_to_target_horizontal = abs(distance / horizontal_speed)
        print(f"Vertical time: {time_to_target_vertical}, Horizontal time: {time_to_target_horizontal}")
    
        if time_to_target_horizontal >= time_to_target_vertical:
            return True, time_to_target_horizontal
        return False, 0


    def calculate_distance(bomb_position, flag_position):
        """
        Calculate the Euclidean distance between a bomb and the flag.

        Args:
            bomb_position (tuple): (x, y) position of the bomb.
            flag_position (tuple): (x, y) position of the flag.

        Returns:
            float: Distance between the bomb and the flag.
        """
        dx = abs(bomb_position[0] - flag_position[0])
        dy = abs(bomb_position[1] - flag_position[1])
        return math.sqrt(dx**2 + dy**2)

    
    def mrua_1d(self, depart, depart_time, acceleration, actuel_time):
        """
        The mrua_1d function calculates the position of an object moving

        Args:
            depart (_type_): _description_
            temps_depart (_type_): _description_
            acceleration (_type_): _description_
            temps_maintenant (_type_): _description_

        Returns:
            computed position
        """
        p = depart + 1/2 * acceleration *((actuel_time-depart_time)** 2)

        return p



    def calculate_bomb_flag_distance(self, bomb, current_time, horizontal_speed, background_cycle_period, window_dimensions):
        """
        Calculates the distance between a bomb and the flag.

        Parameters:
        - bomb: dictionary containing the initial position and parameters of the bomb.
        - current_time: current time in milliseconds.
        - horizontal_speed: horizontal speed of the flag.
        - background_cycle_period: period of the background cycle.
        - window_dimensions: dimensions of the window (tuple (width, height)).

        Returns:
        - distance: Euclidean distance between the bomb and the flag.
        """
        # Current position of the bomb
        x_bomb = bomb['initial_position'][0]
        y_bomb = self.mrua_1d(bomb['initial_position'][1], bomb['initial_depart'], bomb['vertical_acceleration'], current_time)

        # Current position of the flag
        x_flag = int(-current_time * horizontal_speed) % background_cycle_period
        y_flag = window_dimensions[1]  # The flag is always at ground level

        # Calculate horizontal and vertical distances
        dx = abs(x_bomb - x_flag)
        dy = abs(y_bomb - y_flag)

        distance = math.sqrt(dx ** 2 + dy ** 2)
        
        return distance


            
        
