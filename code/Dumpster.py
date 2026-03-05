from code.Entity import Entity

class Dumpster(Entity):

    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self.speed = 5

    def move(self):
        self.rect.x -= self.speed