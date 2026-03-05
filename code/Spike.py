from code.Entity import Entity

class Spike(Entity):

    def __init__(self, position):
        super().__init__('/spikes', position)
        self.speed = 5

    def move(self):
        self.rect.x -= self.speed