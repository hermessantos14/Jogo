import pygame

print('Setup start')
pygame.init()
window = pygame.display.set_mode(size=(800, 600))

print('Setup end')

print('Loop start')
while True:
    #check for all events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() #fecha a janela do jogo
            quit() #encerra o pygame