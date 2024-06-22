import cv2
import numpy as np
import pygame
from random import randrange
from bad import Bad

class BadSketch(Bad):
    def processFrame(self):
        self.cap.set(cv2.CAP_PROP_POS_MSEC, self.time * 1000)
        ret, frame = self.cap.read()

        if not ret:
            print("Erreur lors de la lecture de la vidéo à l'instant t")
            return None

        frame = cv2.resize(frame, (0, 0), fx=self.scale, fy=self.scale)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, frame = cv2.threshold(frame, 128, 255, cv2.THRESH_BINARY)
        edges = cv2.Canny(frame, 50, 150)
        
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return calculate_tangents(contours) + fill(frame, 0.1)

    def render(self):
        f = self.processFrame()
        for i in range(0, len(f), 5):
            l = randrange(10, 30)
            col = randrange(100, 255)
            t = f[i]
            a = t[0] - l * t[1]
            b = t[0] + l * t[1]
            pygame.draw.line(self.screen, (col, col, col), a, b)
        self.next()

def calculate_tangents(contours):
    tangents = []
    for contour in contours:
        for i in range(len(contour)):
            p1 = contour[i][0]
            p0 = contour[i - 1][0]
            p2 = contour[(i + 1) % len(contour)][0]

            tangent_direction = np.array([p2[0] - p0[0], p2[1] - p0[1]])
            tangent_direction = tangent_direction / np.linalg.norm(tangent_direction)

            tangents.append((p1, tangent_direction))
    return tangents

def fill(mask, density):
    points_with_directions = []
    height, width = mask.shape
    num_points = int(density * np.sum(mask != 0))  # Nombre de points en fonction de la densité

    while len(points_with_directions) < num_points:
        x = np.random.randint(0, width)
        y = np.random.randint(0, height)
        if mask[y, x] != 0:
            angle = np.random.uniform(0, 2 * np.pi)
            direction = np.array([np.cos(angle), np.sin(angle)])
            points_with_directions.append(((x, y), direction))
    
    return points_with_directions