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
    

    def ship(self):
        
        # load ship image
        beforescale_ship = pygame.image.load("ship.png")
        ship = pygame.transform.scale(beforescale_ship, (140, 120))
        shiprect = ship.get_rect()

        shiprect.x = 560
        shiprect.y = 545

        return ship, shiprect
    
    def shoot_laser(self, x, y):

        # load laser image
        beforescale_laser = pygame.image.load("laser.png")
        laser = pygame.transform.scale(beforescale_laser, (30, 50))
        laser_rect = laser.get_rect()

        laser_rect.x = x
        laser_rect. y = y

        return laser, laser_rect

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

    if start() == False:
        sys.exit()

    pygame.init()

    clock = pygame.time.Clock()
    running = True
    dt = 0

    speed = [4, 0]
    nspeed = [0, -7]
    espeed = [0, 7]
    
    game = Game(1280, 720)
    screen = game.screen()
    background = game.background()
    ship, ship_rect = game.ship()

    enemy_cls = Enemy("enemy.png")

    enemies, enemies_rect = enemy_cls.enemy()

    score = 0
    lives = 5

    laser = None
    elaser = None


    while running:
        
        # quit pygame if user clicked X to close window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill screen with color 
        screen.fill("black")
        screen.blit(background[0], background[1])
        screen.blit(ship, ship_rect)
        screen.blit(enemies, enemies_rect)

        # move enemy ship
        move_enemy1(enemies_rect, speed)

        # move player ship by calling function
        move_ship(dt, ship_rect)

        # check when key pressed
        keys = pygame.key.get_pressed()

        # Check if space is pressed
        if keys[pygame.K_SPACE]:
                
            # Calculate initial laser position near the ship
            x = ship_rect.x + 54  # Adjust x-coordinate relative to ship position
            y = ship_rect.y - 50

            # Shoot laser if it's not already on the screen
            if  y > 0:  # Only shoot if enemy is above the bottom of the screen
                laser, laser_rect = game.shoot_laser(x, y)

        # Move and render laser if it exists
        if laser:
            laser_rect.y += nspeed[1]  # Move laser upwards
            screen.blit(laser, laser_rect)  # Render laser on screen 

            if laser_rect.colliderect(enemies_rect):
                score += 10
                laser = None


        # Update and render enemy laser
        # Create new enemy laser if none or previous one is off-screen
        if elaser is None or elaser_rect.y >= 720:
            ex = enemies_rect.x + 36
            ey = enemies_rect.y + 80
            elaser, elaser_rect = enemy_cls.enemy_original_laser(ex, ey)

        elaser_rect.y += espeed[1]  # Move enemy laser downwards

         # Render enemy laser if within screen bounds
        if elaser_rect.y < 720:
            screen.blit(elaser, elaser_rect)


            if elaser_rect.colliderect(ship_rect):
                lives -= 1
                elaser=None

        

        font = pygame.font.Font(None, 36)

        # Render and position the score text
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))


        # Render and position the lives text
        live_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
        live_rect = live_text.get_rect(right=screen.get_width() - 30, top=30)
        screen.blit(live_text, live_rect)

        if lives <= 0:
            font_size = pygame.font.Font(None, 72)
            lose = font_size.render("YOU LOSE!", True, (255, 0, 0))
            lose_rect = lose.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            screen.blit(lose, lose_rect)

            final_score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
            final_score_rect = final_score_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 100))
            screen.blit(final_score_text, final_score_rect)

            pygame.display.flip()
            pygame.time.wait(5000)
            pygame.quit()

        dt = clock.tick(60) / 1000
        pygame.display.flip()
    

def start():

    prompt = input("Are you ready to begin? Press Y/N")

    if prompt == "Y":
        return True
    else:
        return False
    

def move_ship(dt, ship_rect):
        
    # move left or right when user moves
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        ship_rect.x -= 250 * dt
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        ship_rect.x += 250 * dt

    return ship_rect.x

def move_enemy1(enemy_rect1, speed):

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