class State:
    def __init__(self):
        self.plane_altitude = 300
        self.previous_altitude = 300
        self.previous_velocity = 0
        self.previous_time = 0
        self.velocity = 0
        self.acceleration = 0
        self.bombs = []
        self.autoBomb = False
        self.autoBomb_time = 0
        self.flag_position = (800, 600)  # Initialize flag position Default starting position (x, y)

    def add_bomb(self, bomb):
        """
        Add a bomb to the list of bombs.

        Args:
            bomb
        
        """
        self.bombs.append(bomb)
        print(f"Added bomb at {bomb['initial_position']}")

    def remove_bombs(self, current_time):
        """
        Remove bombs that have been in the air for more than 3 seconds.

        Args:
            current_time
            
        """
        self.bombs = [bomb for bomb in self.bombs if bomb['initial_depart'] > current_time - 3000]
        print(f"Number of bombs: {len(self.bombs)}")

    def arm_automatic_fire(self, fire_time):
        """
        Arms the automatic bomb-dropping mechanism.
        """
        if not self.autoBomb:
            self.autoBomb = True
            self.autoBomb_time = fire_time
            print(f"Auto-bomb armed for: {fire_time}")
