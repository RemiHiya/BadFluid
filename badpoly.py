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
    
    def processHeight(self):
        bin = self.processFrame()
    
    def render(self):
        bin = self.processFrame()
        for i in range(len(bin[0])):
            for j in range(len(bin)):
                col = bin[i][j] * 255
                pygame.draw.rect(self.screen, (col, col, col), (i, j, 1, 1))
     
