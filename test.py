import sys, pygame


class Game:

    def __init__(self, width, height):

        self.width = width
        self.height = height

    
    def screen(self):
        
        return pygame.display.set_mode((self.width, self.height))

    
    def background(self):

        # load image background and scale to
        background = pygame.image.load("background.jpg")
        background = pygame.transform.scale(background, (self.width, self.height))
        backgroundrect = background.get_rect()

        return background, backgroundrect
    

class Player:


    def __init__(self, image):
        
        self.image = image

    def ship(self):
        
        # load ship image
        beforescale_ship = pygame.image.load(self.image)
        ship = pygame.transform.scale(beforescale_ship, (140, 120))
        shiprect = ship.get_rect()

        shiprect.x = 560
        shiprect.y = 545

        return ship, shiprect
        

class Enemy():
    
    def __init__(self, image):
        self.image = image
        
    def enemy(self):
        beforescale_enemy = pygame.image.load(f"{self.image}")
        enemy = pygame.transform.scale(beforescale_enemy, (110, 90))
        enemy_rect = enemy.get_rect()

        enemy_rect.x = 40
        enemy_rect.y = 120

        return enemy, enemy_rect
    
    def enemy_original_laser(self, x, y):

        # load laser image
        beforescale_laser = pygame.image.load("laser.png")
        laser = pygame.transform.scale(beforescale_laser, (30, 50))
        laser_rect = laser.get_rect()

        laser_rect.x = x
        laser_rect.y = y

        return laser, laser_rect


def main():

    pygame.init()

    clock = pygame.time.Clock()
    running = True
    dt = 0

    speed = [4, 0]
    
    game = Game(1280, 720)
    screen = game.screen()
    background = game.background()

    player = Player('ship.png')

    enemy = Enemy('enemy.png')

    while running:
        
        # quit pygame if user clicked X to close window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill screen with color 
        screen.fill("black")

        # check when key pressed
        keys = pygame.key.get_pressed()

        player.ship()[1].x = move_ship(dt, keys, player.ship()[1])

        # background
        screen.blit(background[0], background[1])

        # player ship
        screen.blit(player.ship()[0], player.ship()[1])

        # create enemy
        screen.blit(enemy.enemy()[0], enemy.enemy()[1])

        dt = clock.tick(60) / 1000
        pygame.display.flip()
    


def move_ship(dt, keys, shiprect):
    
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            shiprect.x -= 250 * dt
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            shiprect.x += 250 * dt

        return shiprect.x

def move_enemy(enemy_rect1, speed):

    # Move the enemy rectangle by the current speed
    enemy_rect1.x += speed[0]

    # Check if the enemy hits the left or right boundary of the screen
    if enemy_rect1.left < 0 or enemy_rect1.right > 1280:
        # Reverse the horizontal speed to change direction
        speed[0] = -speed[0]

    # Update the enemy's rectangle position
    return enemy_rect1


if __name__ == "__main__":
    main()