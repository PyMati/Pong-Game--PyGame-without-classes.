"""Game Module"""
import sys
import pygame
import random

# Variables that help keep state of the game and need's of the game.
start_game = False
start = False
win = False
winner_player = ""
WIN_SCORE = 5
# Setting start players score.
left_score = 0
right_score = 0


# Main function.
def main():
    global start_game, win

    def create_rectangle(left, top, width, heigth):
        """
        This function creates rectangle objects.
        """
        return pygame.Rect(left, top, width, heigth)

    # Initialization of the pygame library and window size as constant.
    pygame.init()
    WINDOW_SIZE = (750, 750)

    # Colours constants.
    white = (255, 255, 255)
    black = (0, 0, 0)

    # Creation of gamescreen in provided WINDOW_SIZE constant.
    game_screen = pygame.display.set_mode(WINDOW_SIZE)

    # Getting gamescreen as rectangular object.
    gamescreen_rect = game_screen.get_rect()

    # Players, ball, middle line creation.
    left_player = create_rectangle(0, 0, 5, 65)
    ball = create_rectangle(0, 0, 25, 25)
    right_player = create_rectangle(0, 0, 5, 65)
    middle_line = create_rectangle(0, 0, 5, 10)

    # Initialization of their native position to the screen center.
    left_player.midleft = gamescreen_rect.midleft
    right_player.midright = gamescreen_rect.midright
    ball.center = gamescreen_rect.center
    middle_line.midtop = gamescreen_rect.midtop
    paddles = [left_player, right_player]

    # Creating midlane.
    line_objects = []
    for _ in range(46):
        line_objects.append(middle_line)
        middle_line = middle_line.move(0, 20)

    # Setting speed for game objects.
    PADDLE_SPEED = 7.5
    ESCAPE_SPEED = 17.5
    ball_velocity = [5, 5]

    # Limiting frames per second.
    fps = pygame.time.Clock()
    MAX_FPS = 60

    # Setting maximum key repetition.
    pygame.key.set_repeat(25, 25)

    # Font and text rendering
    font = pygame.font.Font("freesansbold.ttf", 25)
    right_player_score_text = font.render(f"Score:{right_score}",
                                          True,
                                          white)
    left_player_score_text = font.render(f"Score:{left_score}",
                                         True,
                                         white)
    welcome_message = font.render("Welcome! Press space to start!",
                                  True,
                                  black)
    author = font.render("M. Cieslinski - Pong Game",
                         True,
                         black)
    AUTHOR_POS = (200, 405)
    WELCOME_POS = (200, 375)
    LEFT_SCORE_POS = gamescreen_rect.topleft
    RIGHT_SCORE_POS = (620, 0)

    # Detect player screen border colission.
    def player_border_collision(player, player_side):
        """
        This function controls player space in which the paddles can move.
        """
        if player_side == "left":
            if player.right > gamescreen_rect.centerx - 5:
                player = player.move(-PADDLE_SPEED, 0)
            if player.left < gamescreen_rect.left:
                player = player.move(PADDLE_SPEED, 0)
        elif player_side == "right":
            if player.left < gamescreen_rect.centerx + 5:
                player = player.move(PADDLE_SPEED, 0)
            if player.right > gamescreen_rect.right:
                player = player.move(-PADDLE_SPEED, 0)
        else:
            "Player not found"

        if player.top > gamescreen_rect.top:
            player = player.move(0, -PADDLE_SPEED)

        if player.bottom < gamescreen_rect.bottom:
            player = player.move(0, PADDLE_SPEED)

        return player

    # Creation of ball physics.
    def ball_behaviour(ball_object, paddle_list):
        """
        This function controls ball behaviour in game.
        """
        global start, left_score, right_score, need_random_direction
        if start:
            if ball_object.collidelist(paddle_list) == -1:
                pass
            else:
                ball_velocity[0] = -ball_velocity[0]
                ball_velocity[1] = 5
                if ball_object.colliderect(paddle_list[0]):
                    direct = direction()
                    ball_velocity[1] = ball_velocity[1] * direct
                    if ball_velocity[1] < 0:
                        escape_vertical = -ESCAPE_SPEED
                    else:
                        escape_vertical = ESCAPE_SPEED
                    ball = ball_object.move(ESCAPE_SPEED, escape_vertical)
                    return ball
                elif ball_object.colliderect(paddle_list[1]):
                    direct = direction()
                    ball_velocity[1] = ball_velocity[1] * direct
                    if ball_velocity[1] < 0:
                        escape_vertical = -ESCAPE_SPEED
                    else:
                        escape_vertical = ESCAPE_SPEED
                    ball = ball_object.move(-ESCAPE_SPEED, 0)
                    return ball

            if (ball_object.top < gamescreen_rect.top or
                    ball_object.bottom > gamescreen_rect.bottom):
                ball_velocity[1] = -ball_velocity[1]
            elif ball_object.left > gamescreen_rect.right:
                left_score += 1
                score_left()
                reset_ball(ball_object)
                start = False
            elif ball_object.right < gamescreen_rect.left:
                right_score += 1
                score_right()
                reset_ball(ball_object)
                start = False
            ball_object = ball_object.move(ball_velocity[0], ball_velocity[1])
        else:
            if (ball_object.top < gamescreen_rect.top or
                    ball_object.bottom > gamescreen_rect.bottom):
                start = True
                direct = direction()
                ball_velocity[1] = -ball_velocity[1]
                ball_velocity[0] = ball_velocity[0] * direct
                ball_object = ball_object.move(ball_velocity[0],
                                               ball_velocity[1])
            else:
                ball_object = ball_object.move(0, ball_velocity[1])
        return ball_object

    # Draw game objects.
    def draw(game_object):
        """
        This function draws object on the screen.
        """
        return pygame.draw.rect(game_screen, white, game_object)

    def draw_text(text, position):
        """
        This function draws text objects on the screen.
        """
        return game_screen.blit(text, position)

    # Update scores of players.
    def score_right():
        """
        This function updates score for right player.
        """
        global right_score, winner_player
        if right_score == WIN_SCORE:
            reset_score()
            winner_player = "Right player won!"
        right_player_score_text = font.render(f"Score:{right_score}",
                                              True,
                                              white)
        return right_player_score_text

    def score_left():
        """
        This function updates score for left player.
        """
        global left_score, winner_player
        if left_score == WIN_SCORE:
            reset_score()
            winner_player = "Left player won!"
        right_player_score_text = font.render(f"Score:{left_score}",
                                              True,
                                              white)
        return right_player_score_text

    def winner_text():
        """
        Displays information which player have won.
        """
        msg = font.render(f"{winner_player} Click R to restart.", True, white)
        return msg

    # Refresh screen/ ball object/ Game state.
    def reset_score():
        """
        Reset winner game state and score of each player.
        """
        global left_score, right_score, win
        win = True
        left_score = 0
        right_score = 0

    def reset_ball(ball_object):
        """
        This function resets ball to center position,
        after scoring a point and paddles to their native position.
        """
        left_player.midleft = gamescreen_rect.midleft
        right_player.midright = gamescreen_rect.midright
        ball_object.center = gamescreen_rect.center
        return ball_object

    def refresh_screen():
        """
        This function refreshes screen.
        More understandable for me :D.
        """
        return pygame.display.flip()

    def fill_screen_with_colour(colour):
        """
        This function fills screen with a given colour.
        """
        return game_screen.fill(colour)

    # Randomity
    def direction():
        """
        Generates positive or negative number what influnce the direction
        in which the ball is moving.
        """
        return random.randrange(-1, 2, 2)

    # Main loop
    while True:
        # Controls and events
        if start_game:
            fill_screen_with_colour(black)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                keys = pygame.key.get_pressed()
                if not win:
                    # Left player controls
                    if keys[pygame.K_w]:
                        left_player = left_player.move(0, -PADDLE_SPEED)
                    if keys[pygame.K_s]:
                        left_player = left_player.move(0, PADDLE_SPEED)
                    if keys[pygame.K_d]:
                        left_player = left_player.move(PADDLE_SPEED, 0)
                    if keys[pygame.K_a]:
                        left_player = left_player.move(-PADDLE_SPEED, 0)

                    # Right player controls
                    if keys[pygame.K_UP]:
                        right_player = right_player.move(0, -PADDLE_SPEED)
                    if keys[pygame.K_DOWN]:
                        right_player = right_player.move(0, PADDLE_SPEED)
                    if keys[pygame.K_RIGHT]:
                        right_player = right_player.move(PADDLE_SPEED, 0)
                    if keys[pygame.K_LEFT]:
                        right_player = right_player.move(-PADDLE_SPEED, 0)
                else:
                    if keys[pygame.K_r]:
                        win = False

            # Objects drawing
            if not win:
                # Players and ball
                left_player = player_border_collision(left_player, "left")
                right_player = player_border_collision(right_player, "right")
                paddles[0] = left_player
                paddles[1] = right_player
                ball = ball_behaviour(ball, paddles)
                draw(left_player)
                draw(right_player)
                draw(ball)
                for line in line_objects:
                    draw(line)
                # Text
                left_player_score_text = score_left()
                right_player_score_text = score_right()
                draw_text(left_player_score_text, LEFT_SCORE_POS)
                draw_text(right_player_score_text, RIGHT_SCORE_POS)
            else:
                draw_text(winner_text(), WELCOME_POS)

            refresh_screen()
            # Fps settings
            fps.tick(MAX_FPS)
        else:

            fill_screen_with_colour(white)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    start_game = True

            draw_text(welcome_message, WELCOME_POS)
            draw_text(author, AUTHOR_POS)
            refresh_screen()


if __name__ == "__main__":
    main()
