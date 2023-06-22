import pygame
import random
import time


pygame.init()
SIZE = 40
clock = pygame.time.Clock()


class Food():
    def __init__(self, screen):
        self.m_screen = screen
        self.food = pygame.image.load("resources/apple.jpg").convert()
        self.food_x = 120
        self.food_y = 120

    def draw_food(self):
        self.m_screen.blit(self.food, (self.food_x, self.food_y))

    def move_food(self):
        self.food_x = random.randint(1, 24)*SIZE
        self.food_y = random.randint(1, 19)*SIZE


class Snake:
    def __init__(self, screen):
        self.main_screen = screen
        self.length = 1
        self.snake = pygame.image.load("resources/block.jpg").convert()

        self.snake_x = [40] * self.length
        self.snake_y = [40] * self.length
        self.direction = 'down'

    def draw_snake(self):
        for i in range(self.length):
            self.main_screen.blit(self.snake, (self.snake_x[i], self.snake_y[i]))

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def move_right(self):
        self.direction = 'right'

    def move_left(self):
        self.direction = 'left'

    def increase_length(self):
        self.length += 1
        self.snake_x.append(-1)
        self.snake_y.append(-1)

    def walk(self):
        # this for loop handles rest of the body except head
        for i in range(self.length-1, 0, -1):
            self.snake_x[i] = self.snake_x[i-1]
            self.snake_y[i] = self.snake_y[i-1]

        # below this line we handle head of snake
        if self.direction == 'left':
            self.snake_x[0] -= SIZE
        elif self.direction == 'right':
            self.snake_x[0] += SIZE
        elif self.direction == 'up':
            self.snake_y[0] -= SIZE
        elif self.direction == 'down':
            self.snake_y[0] += SIZE
        self.draw_snake()


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.play_bg_music()
        self.screen_width = 1000
        self.screen_height = 800
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.snake = Snake(self.screen)
        self.snake.draw_snake()
        self.food = Food(self.screen)
        self.food.draw_food()

    def render_bg(self):
        bg = pygame.image.load("resources/background.jpg")
        self.screen.blit(bg, (0, 0))

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False
    
    def play_bg_music(self):
        pygame.mixer.music.load("resources/bg_music_1.mp3")
        pygame.mixer.music.play(-1, 0)

    def display_score(self):
        font = pygame.font.SysFont('comic sans', 30)
        score = font.render(f"Score: {self.snake.length-1}", True, (255,255,255))
        self.screen.blit(score, (850, 10))

    def show_game_over(self):
        self.render_bg()
        font = pygame.font.SysFont('comic sans', 30)
        line1 = font.render(f"Game is Over!! Your Score is: {self.snake.length - 1}", True, (255,255,255))
        self.screen.blit(line1, (200, 230))
        line2 = font.render(f"To Play again, Press Enter OR to Quit Press Escape", True, (255,255,255))
        self.screen.blit(line2, (200, 280))
        pygame.mixer.music.pause()

    def reset(self):
        self.snake = Snake(self.screen)
        self.food = Food(self.screen)

    def play(self):
        self.render_bg()
        self.snake.walk()
        self.food.draw_food()
        self.display_score()

        # snake colliding with apple
        if self.is_collision(self.snake.snake_x[0], self.snake.snake_y[0], self.food.food_x, self.food.food_y):
            sound = pygame.mixer.Sound("resources/ding.mp3")
            pygame.mixer.Sound.play(sound)
            self.snake.increase_length()
            self.food.move_food()

        # snake colliding with itself
        for i in range(2, self.snake.length):
            if self.is_collision(self.snake.snake_x[0], self.snake.snake_y[0], self.snake.snake_x[i],
                                 self.snake.snake_y[i]):
                crash_sound = pygame.mixer.Sound("resources/crash.mp3")
                pygame.mixer.Sound.play(crash_sound)
                raise "Game Over"

        # snake colliding with wall
        if not (0 <= self.snake.snake_x[0] <= 1000 and 0 <= self.snake.snake_y[0] <= 800):
            crash_sound = pygame.mixer.Sound("resources/crash.mp3")
            pygame.mixer.Sound.play(crash_sound)
            raise "Hit the boundary error"

    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_RETURN:
                        pause = False
                        pygame.mixer.music.unpause()
                    if not pause:
                        if event.key == pygame.K_UP:
                            self.snake.move_up()
                        if event.key == pygame.K_DOWN:
                            self.snake.move_down()
                        if event.key == pygame.K_RIGHT:
                            self.snake.move_right()
                        if event.key == pygame.K_LEFT:
                            self.snake.move_left()

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()
            time.sleep(0.13)
            pygame.display.update()
            clock.tick(50)


if __name__ == '__main__':
    game = Game()
    game.run()
