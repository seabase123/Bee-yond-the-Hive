import pygame, math, random

pygame.init()

WIDTH, HEIGHT = 1024, 576
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Honeybee Game")

background = pygame.image.load("Images/background.png").convert_alpha()
hive = pygame.image.load("Images/hive.png").convert_alpha()

clock = pygame.time.Clock()

flowers = []
flower_count = 10
state = "menu"
day_length = 1000
start_time = 0
honey = 0
day = 1
max_days = 10


class Honeybee:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

        self.original_image = pygame.image.load("Images/bee.png").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (64, 64))

        self.angle = 0

    def rotate_left(self):
        self.angle += 5

    def rotate_right(self):
        self.angle -= 5

    def move_forward(self):
        rad = math.radians(self.angle + 90)
        self.x += math.cos(rad) * self.speed
        self.y -= math.sin(rad) * self.speed

    def constrain(self):
        w, h = self.original_image.get_size()
        half_w, half_h = w // 2, h // 2

        self.x = max(half_w, min(self.x, WIDTH - half_w))
        self.y = max(half_h, min(self.y, HEIGHT - half_h))

    def draw(self):
        rotated = pygame.transform.rotate(self.original_image, self.angle)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(rotated, rect)

    def get_rect(self):
        rotated = pygame.transform.rotate(self.original_image, self.angle)
        return rotated.get_rect(center=(int(self.x), int(self.y)))


class Flower:
    def __init__(self):
        self.image = pygame.image.load("Images/flower.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 64))

        w, h = self.image.get_size()
        self.x = random.randint(w // 2, WIDTH - w // 2)
        self.y = random.randint(h // 2, HEIGHT - h // 2)

        self.active = True

    def draw(self):
        rect = self.image.get_rect(center=(self.x, self.y))

        if self.active:
            screen.blit(self.image, rect)
        else:
            faded = self.image.copy()
            faded.set_alpha(80)
            screen.blit(faded, rect)

def draw_text(text, size, color, x, y):
    font = pygame.font.SysFont(None, size)
    render = font.render(text, True, color)
    rect = render.get_rect(center=(x, y))
    screen.blit(render, rect)


bee = Honeybee(500, 300, 2)

running = True
while running:
    screen.fill((25, 74, 42))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if state == "menu":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                state = "playing"
                start_time = pygame.time.get_ticks()

                flowers = []
                for _ in range(flower_count):
                    flowers.append(Flower())

        elif state == "hive":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                day += 1

                for _ in range(int(honey // 5)):
                    if random.random() < 0.2:
                        flower_count += 1

                if day > max_days:
                    state = "game_over"
                else:
                    state = "playing"
                    start_time = pygame.time.get_ticks()

                    bee = Honeybee(500, 300, 2)

                    flowers = []
                    for _ in range(flower_count):
                        flowers.append(Flower())

        elif state == "game_over":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bee = Honeybee(500, 300, 2)
                honey = 0
                day = 1
                state = "menu"

    if state == "menu":
        screen.blit(background, (0, 0))
        draw_text("Press SPACE to Start", 40, (255, 255, 255), WIDTH // 2, 500)

    elif state == "playing":
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            bee.rotate_left()
        if keys[pygame.K_RIGHT]:
            bee.rotate_right()
        if keys[pygame.K_UP]:
            bee.move_forward()

        bee.constrain()

        for flower in flowers:
            flower.draw()

        bee.draw()
        bee_rect = bee.get_rect()

        for flower in flowers:
            if flower.active:
                flower_rect = flower.image.get_rect(center=(flower.x, flower.y))

                if bee_rect.colliderect(flower_rect):
                    honey += random.randint(1, 3)
                    flower.active = False


        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time
        timer_time = (max(0, day_length - elapsed_time)+1)

        progress = min(elapsed_time / day_length, 1)
        darkness = int(progress * 180)

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(darkness)
        overlay.fill((0, 0, 5))
        screen.blit(overlay, (0, 0))

        if elapsed_time >= day_length:
            state = "hive"

        draw_text(f"Honey: {int(honey)}", 30, (255, 255, 255), 60, 30)
        draw_text(f"Time: {timer_time//1000}", 30, (255, 255, 255), 55, 60)

    elif state == "hive":
        screen.blit(hive, (0, 0))

        draw_text(f"Day {day} Complete", 100, (255, 255, 255), WIDTH // 2, 150)
        draw_text(f"Total Honey: {int(honey)}", 60, (255, 255, 255), WIDTH // 2, 240)
        draw_text(f"Yesterday Flower Count: {flower_count}", 60, (255, 255, 255), WIDTH // 2, 290)
        draw_text(f"Days Left: {max_days - day}", 60, (255, 255, 255), WIDTH // 2, 340)

        draw_text("Press SPACE to continue", 40, (255, 255, 255), WIDTH // 2, 460)

    elif state == "game_over":
        screen.fill((0, 0, 0))

        draw_text("Winter Has Come...", 60, (255, 255, 255), WIDTH // 2, 100)
        draw_text(f"Total Honey: {int(honey)}", 40, (200, 200, 200), WIDTH // 2, 150)

        draw_text(f"Bees might be small, but they do a huge job for us!", 30, (150, 150, 150), WIDTH // 2, 230)
        draw_text(f"Without bees, we wouldn't have many of the fruits and vegetables we love.", 30, (150, 150, 150), WIDTH // 2, 270)
        draw_text(f"Let's do our part to protect bees and their habitats!", 30, (150, 150, 150), WIDTH // 2, 310)
        draw_text(f"Planting flowers, reducing pesticide use, and supporting local beekeepers can all help!", 30, (150, 150, 150), WIDTH // 2, 350)
        draw_text(f"Together, we can make a difference for our buzzing friends!", 30, (150, 150, 150), WIDTH // 2, 390)

        draw_text("Press SPACE to Restart", 30, (150, 150, 150), WIDTH // 2, 500)

        flower_count = 10

    pygame.display.update()
    clock.tick(60)


pygame.quit()