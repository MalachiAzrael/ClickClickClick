import pygame
import os
import math
#import time
#import random

pygame.font.init()

# Window
WIDTH = 750
HEIGHT = 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Click Click Click")

# Load Images
COOKIE_IMG = pygame.image.load(os.path.join("assets", "cookie.png"))
SIMPLE_CLICK_IMG = pygame.image.load(os.path.join("assets", "ok.png"))
GRAY_BUTTON_IMG = pygame.image.load(os.path.join("assets", "gray.png"))
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "spacebg.jpg")), (WIDTH, HEIGHT))

# Set Icon
pygame.display.set_icon(COOKIE_IMG)
cookie_count = 0

# Simple Clicker Variables
SIMPLE_BASE_PROD = 0.1
SIMPLE_BASE_COST = 15
SIMPLE_COST_RATE = 1.15

simple_clickers_owned = 0
simple_clicker_level = 1
simple_clicker_cps = 0
simple_clicker_cost = 0


class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.subimage = pygame.transform.scale(GRAY_BUTTON_IMG, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.rect.topleft = (x, y)
        self.clicked = False
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, window):
        pos = pygame.mouse.get_pos()
        action = False

        if self.rect.collidepoint(pos):
            #print("hover")
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        window.blit(self.image, (self.rect.x, self.rect.y))

        return action


def main():
    global cookie_count
    global simple_clickers_owned
    global simple_clicker_cps
    run = True
    frames = 60
    main_font = pygame.font.SysFont("Calibri", 50)
    button_font = pygame.font.SysFont("Calibri", 25)
    small_button_font = pygame.font.SysFont("Calibri", 15)
    clock = pygame.time.Clock()

    big_cookie = Button(((WIDTH / 2) - ((int(COOKIE_IMG.get_width()) * 0.25) / 2)), 100, COOKIE_IMG, 0.25)

    #buy_simple_clicker = Button(15, (HEIGHT - (int(SIMPLE_CLICK_IMG.get_height()) * 0.5) - 15), SIMPLE_CLICK_IMG, 0.5)

    #simple_clicker_cost = int(math.ceil(SIMPLE_BASE_COST * SIMPLE_COST_RATE ** simple_clickers_owned))

    def redraw_window():
        global cookie_count
        global simple_clicker_cost

        # Draw Background
        WIN.blit(BG, (0, 0))

        # Draw Cookie Count Label
        cookie_count_label = main_font.render(f"Count: {int(cookie_count)}", True, (255, 255, 255))
        WIN.blit(cookie_count_label, ((WIDTH / 2) - (cookie_count_label.get_width() / 2), 10))

        #Update Window Title
        pygame.display.set_caption(str(cookie_count))

        # Calc Simple Clicker Cost
        simple_clicker_cost = int(math.ceil(SIMPLE_BASE_COST * SIMPLE_COST_RATE ** simple_clickers_owned))

        # Draw Big Cookie and Check if Clicked
        if big_cookie.draw(WIN):
            big_cookie_click()

        #Geneate Simple Clicker Button
        buy_simple_clicker = Button(15, (HEIGHT - (int(SIMPLE_CLICK_IMG.get_height()) * 0.5) - 15), SIMPLE_CLICK_IMG if cookie_count >= simple_clicker_cost else GRAY_BUTTON_IMG, 0.5)

        # Draw Buy Simple Clicker and Check if Clicked
        if buy_simple_clicker.draw(WIN):
            buy_simple_click()


        # Draw Simple Clicker Label
        buy_simple_label = button_font.render("Simple Clicker", True, (255, 255, 255))
        WIN.blit(buy_simple_label, (buy_simple_clicker.rect.center[0] - ((buy_simple_label.get_width() // 2) + 35), buy_simple_clicker.rect.center[1] - (buy_simple_label.get_height() // 2) - 10))

        # Draw Simple Clicker Price
        simple_price_label = small_button_font.render(f"Cost: {str(simple_clicker_cost)}", True, (255, 255, 255))
        WIN.blit(simple_price_label, (buy_simple_clicker.rect.center[0] - ((simple_price_label.get_width() // 2) + 35), buy_simple_clicker.rect.center[1] - (simple_price_label.get_height() // 2) + 13))

        # Draw Simple Clicker Count
        number_font = pygame.font.SysFont("Calibri", 50 if simple_clickers_owned < 100 else 25)
        simple_count_label = number_font.render(str(simple_clickers_owned), True, (255, 255, 255))
        WIN.blit(simple_count_label, (buy_simple_clicker.rect.center[0] - ((simple_count_label.get_width() // 2) - 85), buy_simple_clicker.rect.center[1] - (simple_count_label.get_height() // 2)))

        # Update Screen
        pygame.display.update()

    #On Big Cookie Click
    def big_cookie_click():
        global cookie_count
        cookie_count += 1

    #On Buy Simple Clicker Click
    def buy_simple_click():
        #Globals
        global simple_clickers_owned
        global simple_clicker_cps
        global simple_clicker_cost
        global cookie_count

        # Increment Simple Clicker Owned
        if cookie_count >= simple_clicker_cost:
            cookie_count -= simple_clicker_cost
            simple_clickers_owned += 1
        else:
            print("You cant afford that")
            print(simple_clicker_cost)

        # Calculate Simple Clicker CPS
        simple_clicker_cps = (SIMPLE_BASE_PROD * simple_clickers_owned) * simple_clicker_level

    # Main Game Loop
    while run:
        # Update Clock (Limit to #frames)
        clock.tick(frames)

        # Add cookies for simple clickers
        cookie_count += simple_clicker_cps / frames

        # Check for any in game events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Redraw screen per frame
        redraw_window()


if __name__ == '__main__':
    main()
