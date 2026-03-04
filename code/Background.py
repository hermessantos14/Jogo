from code.Entity import Entity

class Background(Entity):

    def __init__(self, name: str, position: tuple, speed: int):
        super().__init__(name, position)
        self.speed = speed

    def move(self):
        self.rect.x -= self.speed
