class Entity:
    def __init__(self, config, x, y, width, height, surface, shape):
        # Game Config 
        self.config  = config 
        # Position
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        # Surface + Shape
        self.surface = surface
        self.shape = shape
        
    @property
    def cx(self):
        return self.x + self.width / 2

    @property
    def cy(self):
        return self.y + self.height / 2

    @property
    def rect(self):
        return self.shape 
    
        
    def process(self):
        # Process entity in 1 game tick 
        pass 
    
    def draw(self):
        # Draw entity on screen
        pass 

    def collide(self, other):
        # Return true if entity collides with other entity
        pass 
