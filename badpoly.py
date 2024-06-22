import cv2
import numpy as np
import pygame
from bad import Bad

class BadPoly(Bad):
    def processFrame(self):
        self.cap.set(cv2.CAP_PROP_POS_MSEC, self.time * 1000)
        ret, frame = self.cap.read()

        if not ret:
            print("Erreur lors de la lecture de la vidéo à l'instant t")
            return None

        resized_frame = cv2.resize(frame, (0, 0), fx=self.scale, fy=self.scale)
        gray_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)

        _, binary_frame = cv2.threshold(gray_frame, 128, 255, cv2.THRESH_BINARY)
        binary_frame = cv2.Canny(binary_frame, 100, 200)

        binary_array = (binary_frame // 255).astype(np.uint8)

        return binary_array
    
    def processHeight(self, x: int) -> tuple[int, int]:
        bin = self.processFrame()
        height = len(bin)
        a = 0
        b = height-1
        while a < height//2 and bin[a][x] == 0:
            a+=1
        while b >= height//2 and bin[b][x] == 0:
            b-=1
        return (a, b)

    def processHeight(self, x: int) -> tuple[int, int]:
        bin = self.processFrame()
        height = bin.shape[0]
    
        column = bin[:, x]
    
        a = np.argmax(column[:height // 2] != 0)
        b = height - 1 - np.argmax(column[::-1][:height // 2] != 0)
    
        return (a, b)
    
    def render(self):
        bin = self.processFrame()
        for i in range(len(bin[0])):
            a, b = self.processHeight(i)
            col = (255, 255, 255)
            pygame.draw.rect(self.screen, col, (i/self.scale, a/self.scale, 1/self.scale,1))
            pygame.draw.rect(self.screen, col, (i/self.scale, b/self.scale, 1/self.scale,1))
        self.frame += 1
        self.time += self.rate