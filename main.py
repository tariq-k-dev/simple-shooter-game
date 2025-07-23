import pygame
import sys
import random


# Collision detection function
def check_collision(rect1, rect2):
    return rect1.colliderect(rect2)


def main():
    # Initialize PyGame
    pygame.init()

    # Set up the game window
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Simple Shooter Game")
    bg_image = pygame.image.load('./assets/space-background.jpg')

    # Set the frame rate
    clock = pygame.time.Clock()

    # Player settings
    # player_width = 50
    # player_height = 60
    player_width = 82
    player_height = 76
    player_img = pygame.image.load("./assets/blue-space-ship-1.png")
    player_img = pygame.transform.scale(
        player_img, (player_width, player_height))
    # Center the player at the bottom of the screen
    player_x = screen_width // 2 - player_width // 2
    player_y = screen_height - player_height - 10
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    player_speed = 5
    player_lives = 3
    player_score = 0

    # Bullet settings
    bullet_width = 5
    bullet_height = 10
    bullet_speed = 7
    bullets = []

    # Enemy settings
    # enemy_width = 50
    # enemy_height = 60
    enemy_width = 93
    enemy_height = 77
    enemy_img = pygame.image.load("./assets/red-enemy-ship-1.png")
    enemy_img = pygame.transform.scale(enemy_img, (enemy_width, enemy_height))
    enemy_speed = 2
    enemies = []

    # Spawn an enemy every 2 seconds
    enemy_timer = 0
    enemy_spawn_time = 2000

    # Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Create a bullet at the current player position
                    bullet_x = player_x + player_width // 2 - bullet_width // 2
                    bullet_y = player_y
                    bullets.append(pygame.Rect(bullet_x, bullet_y,
                                               bullet_width, bullet_height))

        # Handle player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
            player_x += player_speed

        # Update bullet positions
        for bullet in bullets:
            bullet.y -= bullet_speed

        # Remove bullets that are off the screen
        bullets = [bullet for bullet in bullets if bullet.y > 0]

        # Update enemy positions and spawn new ones
        current_time = pygame.time.get_ticks()
        if current_time - enemy_timer > enemy_spawn_time:
            enemy_x = random.randint(0, screen_width - enemy_width)
            enemy_y = -enemy_height
            # enemies.append(pygame.Rect(
            #     enemy_x, enemy_y, enemy_width, enemy_height))
            enemies.append(enemy_img.get_rect(topleft=(enemy_x, enemy_y)))
            enemy_timer = current_time

        for enemy in enemies:
            enemy.y += enemy_speed

        # Check for collisions
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if check_collision(bullet, enemy):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    break

        # Remove enemies that are off the screen
        enemies = [enemy for enemy in enemies if enemy.y < screen_height]

        # Fill the screen with a color (black in this case)
        screen.fill((0, 0, 0))
        screen.blit(bg_image, (0, 0))

        # Draw the player
        # pygame.draw.rect(screen, (0, 128, 255), (player_x,
        #                                          player_y, player_width, player_height))
        screen.blit(player_img, (player_x, player_y))

        # Draw the bullets
        for bullet in bullets:
            pygame.draw.rect(screen, (255, 255, 255), bullet)

        # Draw the enemies
        for enemy in enemies:
            # pygame.draw.rect(screen, (255, 0, 0), enemy)
            screen.blit(enemy_img, enemy)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate at 60 frames per second
        clock.tick(60)


if __name__ == "__main__":
    main()
