# Import all libraries
import pygame
from pygame.locals import *
import sys
import time
import random

# contain all function


class Game:
    def __init__(self):
        """All variable and background image load and scale it."""
        self.w = 1200
        self.h = 700
        self.reset = True
        self.active = False
        self.input_text = ''
        self.word = ''
        self.time_start = 0
        self.total_time = 0
        self.accuracy = '0%'
        self.results = 'Time: 0 Accuracy: 0% Wpm: 0'
        self.wpm = 0
        self.end = False
        self.HEAD_C1 = (0, 100, 0)
        self.HEAD_C2 = (0, 255, 0)
        self.INBOX_C = (0, 128, 0)
        self.TEXT_C = (240, 240, 240)
        self.RESULT_C = (255, 70, 70)

        pygame.init()

        self.open_img = pygame.image.load('font.png')
        self.open_img = pygame.transform.scale(self.open_img, (self.w, self.h))

        self.bg = pygame.image.load('nasa.png')
        self.bg = pygame.transform.scale(self.bg, (1200, 700))

        self.screen = pygame.display.set_mode((self.w, self.h))

        pygame.display.set_caption('Typing Test Test')

    def draw_text(self, screen, msg, y, fsize, color):
        """It takes argument. Draw the text on the screen and pygame upload this text"""
        font = pygame.font.Font(None, fsize)
        text = font.render(msg, 1, color)
        text_rect = text.get_rect(center=(self.w/2, y))
        screen.blit(text, text_rect)
        pygame.display.update()

    def get_sentence(self):
        """Open the txt file. Split it and randomly select a sentence."""
        f = open('sentences.txt').read()
        sentences = f.split('\n')
        sentence = random.choice(sentences)
        return sentence

    def show_results(self, screen):
        """Calculate time, accuracy and speed"""
        if(not self.end):
            # Calculate time
            self.total_time = time.time() - self.time_start

            # Calculate accuracy
            count = 0
            for i, c in enumerate(self.word):
                try:
                    if self.input_text[i] == c:
                        count += 1
                except:
                    pass
            self.accuracy = count/len(self.word)*100

            # Calculate word per minute
            self.wpm = len(self.input_text)*60/(5*self.total_time)

            self.end = True
            print(self.total_time)

            self.results = 'Time: ' + str(round(self.total_time)) + " secs  Accuracy: " + str(round(self.accuracy)) \
                           + " % " + ' WPM ' + str(round(self.wpm))

            # Draw icon image
            self.time_img = pygame.image.load('reset.jpg')
            self.time_img = pygame.transform.scale(self.time_img, (120, 120))
            screen.blit(self.time_img, (1050, 520))
            # self.draw_text(screen, "Reset", 1050, 35, (0, 139, 139))
            print(self.results)
            pygame.display.update()

    def run(self):
        """This is the main function of the class. It looks for mouse position and keyboard event"""
        self.reset_game()

        self.running = True
        while(self.running):
            clock = pygame.time.Clock()
            self.screen.fill((0, 0, 0), (150, 500, 850, 60))
            pygame.draw.rect(self.screen, self.INBOX_C, (150, 500, 850, 60), 2)

            # Update the text of the user input
            self.draw_text(self.screen, self.input_text, 530, 35, (255, 0, 0))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    # position of the input box
                    if(x >= 150 and x <= 850 and y >= 500 and y <= 550):
                        self.active = True
                        self.input_text = ''
                        self.time_start = time.time()
                    # position of the reset box
                    if(x >= 1050 and x <= 1150 and y >= 520 and y <= 620):
                        self.reset_game()
                        x, y = pygame.mouse.get_pos()
                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.end:
                        if event.key == pygame.K_RETURN:
                            print(self.input_text)
                            self.show_results(self.screen)
                            print(self.results)
                            self.draw_text(self.screen, self.results, 640, 35, self.RESULT_C)
                            self.end = True
                        elif event.key == pygame.K_BACKSPACE:
                            self.input_text = self.input_text[:-1]
                        else:
                            try:
                                self.input_text += event.unicode
                            except:
                                pass
            pygame.display.update()

        Clock.tick(60)

    def reset_game(self):
        """Reset all variable"""
        self.screen.blit(self.open_img, (0, 0))
        pygame.display.update()
        time.sleep(3)
        self.reset = False
        self.end = False
        self.input_text = ''
        self.word = ''
        self.time_start = 0
        self.total_time = 0
        self.wpm = 0

        # Get random sentence
        self.word = self.get_sentence()
        if(not self.word): self.reset_game()
        # drawing heading
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.bg, (0, 0))
        msg1 = "Typing Test"
        msg2 = "Time Accuracy Speed"
        self.draw_text(self.screen, msg1, 60, 80, self.HEAD_C1)
        self.draw_text(self.screen, msg2, 120, 40, self.HEAD_C2)
        # Draw the rect for input box
        pygame.draw.rect(self.screen, (0, 128, 0), (315, 500, 600, 60))
        # Draw the sentence string
        self.draw_text(self.screen, self.word, 220, 45, (0, 128, 128))
        pygame.display.update()


Game().run()
















