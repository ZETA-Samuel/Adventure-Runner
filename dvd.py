import sys, pygame
pygame.init()
clock = pygame.time.Clock()

size = width, height = 900, 600
speed = [7, 3]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

dvd = pygame.image.load("dvd.png")
dvd = pygame.transform.scale(dvd, (150, 100))
dvdrect = dvd.get_rect()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    dvdrect = dvdrect.move(speed)
    if dvdrect.left < 0 or dvdrect.right > width:
        speed[0] = -speed[0]
    if dvdrect.top < 0 or dvdrect.bottom > height:
        speed[1] = -speed[1]

    screen.fill(black)
    screen.blit(dvd, dvdrect)
    pygame.display.flip()
    clock.tick(45)