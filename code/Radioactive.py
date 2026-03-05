from code.Entity import Entity

class Radioactive(Entity):

    def __init__(self, position):
        super().__init__('/radioactive', position)
        self.speed = 5

    def move(self):
        self.rect.x -= self.speed