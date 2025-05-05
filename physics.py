import math

class Physics:
    def calculate_velocity_acceleration(self, altitude, current_time, previous_position, previous_time, previous_velocity):
        """
        Calculate velocity and acceleration based on altitude and time.
        Matches the original implementation.
        
        Args:
            altitude: Current altitude of the plane
            current_time: Current time in milliseconds
            previous_position: Previous altitude
            previous_time: Previous time in milliseconds
            previous_velocity: Previous velocity
            
        Returns:
            tuple: (velocity, acceleration)
        """
        # Avoid division by zero
        if current_time == previous_time:
            return 0, 0
            
        # Calculate vertical velocity (negative because up is decreasing y)
        velocity = -(altitude - previous_position) / (current_time - previous_time)
        
        # Calculate acceleration
        acceleration = (velocity - previous_velocity) / (current_time - previous_time)
        
        return velocity, acceleration

    def mrua_1d(self, depart, depart_time, acceleration, current_time):
        """
        Calculate the position of an object under constant acceleration.
        p = p0 + 0.5 * a * t²
        
        Args:
            depart: Initial position
            depart_time: Initial time in milliseconds
            acceleration: Constant acceleration
            current_time: Current time in milliseconds
            
        Returns:
            float: Current position
        """
        elapsed_time = current_time - depart_time
        position = depart + 0.5 * acceleration * (elapsed_time ** 2)
        
        return position

    def calculate_fire(self, altitude_release, altitude_target, acceleration, next_target_time, current_time):
        """
        Calculate if a shot is possible and when to fire.
        
        Args:
            altitude_release: Altitude where the bomb is released
            altitude_target: Target altitude (ground level)
            acceleration: Gravitational acceleration
            next_target_time: Time when the target will be in position
            current_time: Current time in milliseconds
            
        Returns:
            tuple: (is_possible, time_to_fire)
        """
        # Calculate time of flight for the bomb
        flight_time = math.sqrt(2 * (altitude_target - altitude_release) / acceleration)
        
        # Calculate when to release the bomb
        fire_time = next_target_time - flight_time
        
        # Determine if the shot is possible (fire time is in the future)
        if fire_time > current_time:
            return True, fire_time
        
        # Shot not possible with current parameters
        return False, 0

    def calculate_impact_point(self, initial_position, initial_velocity, acceleration, time):
        """
        Calculate the impact point of a projectile.
        
        Args:
            initial_position: Initial position (x, y)
            initial_velocity: Initial velocity (vx, vy)
            acceleration: Acceleration vector (ax, ay)
            time: Time of flight
            
        Returns:
            tuple: Impact position (x, y)
        """
        x = initial_position[0] + initial_velocity[0] * time
        y = initial_position[1] + initial_velocity[1] * time + 0.5 * acceleration[1] * (time ** 2)
        
        return (x, y)