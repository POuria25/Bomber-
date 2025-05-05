class State:
    def __init__(self):
        """Initialize the game state with default values."""
        # Plane properties
        self.plane_altitude = 300
        self.previous_altitude = 300
        self.previous_velocity = 0.0
        self.previous_time = 0
        self.velocity = 0.0
        self.acceleration = 0.0
        
        # Bombs
        self.bombs = []
        
        # Auto-bombing
        self.autoBomb = False
        self.autoBomb_time = 0
        self.explosions = [] 

    def add_bomb(self, bomb):
        """
        Add a bomb to the list of bombs.
        
        Args:
            bomb: Dictionary containing bomb properties
        """
        # Add a current_position field to track position during flight
        bomb["current_position"] = bomb["initial_position"]
        self.bombs.append(bomb)

    def remove_bombs(self, current_time):
        """
        Remove bombs that have been in the air for more than 3 seconds
        or have hit the ground.
        
        Args:
            current_time: Current time in milliseconds
        """
        self.bombs = [bomb for bomb in self.bombs if 
                     bomb['initial_depart'] > current_time - 3000 and
                     'hit_ground' not in bomb]

    def remove_bomb(self, bomb):
        """
        Remove a specific bomb from the list.
        
        Args:
            bomb: The bomb to remove
        """
        if bomb in self.bombs:
            self.bombs.remove(bomb)

    def arm_automatic_fire(self, fire_time):
        """
        Arms the automatic bomb-dropping mechanism.
        
        Args:
            fire_time: Time when the bomb should be dropped
        """
        if not self.autoBomb:
            self.autoBomb = True
            self.autoBomb_time = fire_time
            
    def add_explosion(self, position, time):
        """
        Add an explosion at the specified position.
        
        Args:
            position: (x, y) coordinates of the explosion
            time: Current time in milliseconds
        """
        explosion = {
            'position': position,
            'time_created': time
        }
        self.explosions.append(explosion)
        print(f"Explosion added at {position}")
    
    def remove_explosions(self, current_time):
        """
        Remove explosions that have been displayed for more than 500ms.
        
        Args:
            current_time: Current time in milliseconds
        """
        old_count = len(self.explosions)
        self.explosions = [exp for exp in self.explosions if exp['time_created'] > current_time - 500]
        