import pygame
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import time 


pygame.init()
size = width, height = 1280, 720
white = (255, 255, 255)
screen = pygame.display.set_mode(size)
# Initialize the clock
fps = 60
clock = pygame.time.Clock()

# capture the camera
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# hand detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Load Image
imgBG = pygame.image.load("/home/fateme/Documents/game/Resources/background.png").convert()
imgSoundOff = pygame.image.load("/home/fateme/Documents/game/Resources/sound-off.png").convert_alpha()
imgSoundOff = pygame.transform.rotozoom(imgSoundOff, 0, 0.1)
soundRect = imgSoundOff.get_rect()
soundRect.x, soundRect.y = 5, 200


imgBalloon = pygame.image.load("/home/fateme/Documents/game/Resources/balloonBlue.png").convert_alpha()
imgBalloon = pygame.transform.rotozoom(imgBalloon, 0, 0.15)
balloonRect = imgBalloon.get_rect()
balloonRect.x, balloonRect.y = 500, 600

imgBalloonPink = pygame.image.load("/home/fateme/Documents/game/Resources/balloonPink.png").convert_alpha()
imgBalloonPink = pygame.transform.rotozoom(imgBalloonPink, 0, 0.13)
balloonRectPink = imgBalloonPink.get_rect()
balloonRectPink.x, balloonRectPink.y = 200, 530

imgBalloonGr = pygame.image.load("/home/fateme/Documents/game/Resources/balloonGreen.png").convert_alpha()
imgBalloonGr = pygame.transform.rotozoom(imgBalloonGr, 0, 0.15)
balloonRectGr = imgBalloonGr.get_rect()
balloonRectGr.x, balloonRectGr.y = 400, 530

# Load music
pygame.mixer.music.load("/home/fateme/Documents/game/Resources/Fluffing-a-Duck.mp3")

# Variables
speed = 5
score = 0
totalTime = 10
startTime = time.time()

def resetballoon(ballon):
    ballon.x, ballon.y = np.random.randint(100, 1180), 700

pygame.mixer.init()
pygame.mixer.music.play()
# Main Loop
start = True
while start:
    # Get events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
            pygame.quit()

    # Apply Logic
    remainTime = int(totalTime - (time.time() - startTime))

    if remainTime > 0:
        # move balloon up
        for rect in balloonRect, balloonRectPink, balloonRectGr:
            rect.y -= speed

        if balloonRect.y < 0:
            resetballoon(balloonRect)
            speed += 3
        if balloonRectPink.y < 0:
            resetballoon(balloonRectPink)
            speed += 2
        if balloonRectGr.y < 0:
            resetballoon(balloonRectGr)
            speed += 4

        success, frame = cap.read()
        frame = cv2.flip(frame, 1)
        # Find the hand and its landmarks
        # hands, frame = detector.findHands(frame)  # with draw
        hands = detector.findHands(frame, draw=False)  # without draw

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        surface_frame = pygame.surfarray.make_surface(frame)
        surface_frame = pygame.transform.flip(surface_frame, True, False)

        if hands:
            # Hand 1
            hand1 = hands[0]
            lmList1 = hand1["lmList"]  # List of 21 Landmark points
            index_finger_x, index_finger_y = lmList1[8][0], lmList1[8][1]
            if soundRect.collidepoint(index_finger_x, index_finger_y):
                pygame.mixer.music.stop()
                
            if balloonRect.collidepoint(index_finger_x, index_finger_y):
                resetballoon(balloonRect)
                speed += 1
                score += 10
            if balloonRectPink.collidepoint(index_finger_x, index_finger_y):
                resetballoon(balloonRectPink)
                speed += 2
                score += 15
            if balloonRectGr.collidepoint(index_finger_x, index_finger_y):
                resetballoon(balloonRectGr)
                speed += 0
                score += 5

        
        screen.blit(surface_frame, (0, 0))
        screen.blit(imgSoundOff, soundRect)
        pygame.Surface.blit(screen, imgBalloon, balloonRect)
        pygame.Surface.blit(screen, imgBalloonGr, balloonRectGr)
        pygame.Surface.blit(screen, imgBalloonPink, balloonRectPink)

        font = pygame.font.Font("Resources/Marcellus-Regular.ttf", 30)
        txt_renderer = font.render(f'Score: {score}', True, (100, 50, 200))
        screen.blit(txt_renderer, (50, 50))
        txt_renderer = font.render(f'Time: {remainTime}', True, (200, 50, 20))
        screen.blit(txt_renderer, (1050, 50))
        pygame.display.update()
    else:
        screen.blit(imgBG, (0,0))
        font = pygame.font.Font("Resources/Marcellus-Regular.ttf", 60)
        txt_renderer = font.render(f'Score: {score}', True, (100, 50, 200))
        screen.blit(txt_renderer, (440, 350))
        txt_renderer = font.render(f'Time is UP!', True, (200, 50, 20))
        screen.blit(txt_renderer, (440, 250))

    # Update display
    pygame.display.update()

    # Set FPS
    clock.tick(fps)