import cv2
import numpy as np
import math
import colorsys

def process_frame(frame, scale):
    resized_frame = cv2.resize(frame, (0, 0), fx=scale, fy=scale)
    gray_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)

    # Appliquer un seuillage pour obtenir une image binaire
    _, binary_frame = cv2.threshold(gray_frame, 128, 255, cv2.THRESH_BINARY)

    # Convertir l'image binaire en tableau de 0 et 1
    binary_array = (binary_frame // 255).astype(np.uint8)

    return binary_array

def get_binary_image_at_time(cap, t, scale):
    # Définir la position de la vidéo à l'instant t (en secondes)
    cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)

    # Lire la frame à l'instant t
    ret, frame = cap.read()

    if not ret:
        print("Erreur lors de la lecture de la vidéo à l'instant t")
        return None

    # Traiter la frame
    binary_array = process_frame(frame, scale)

    return binary_array


def dir2col(x, y):
    length = math.sqrt(x*x + y*y)
    if length == 0:
        return (0, 0, 0)  # Handle zero length vector case

    nx = x / length
    ny = y / length

    angle = math.atan2(ny, nx)

    hue = angle * (180.0 / math.pi) + 90
    if hue < 0:
        hue += 360

    c = 1.0
    x_value = 1.0 - abs((hue / 60.0) % 2 - 1.0)
    m = 0

    if 0 <= hue < 60:
        r_prime = c
        g_prime = x_value
        b_prime = 0
    elif 60 <= hue < 120:
        r_prime = x_value
        g_prime = c
        b_prime = 0
    elif 120 <= hue < 180:
        r_prime = 0
        g_prime = c
        b_prime = x_value
    elif 180 <= hue < 240:
        r_prime = 0
        g_prime = x_value
        b_prime = c
    elif 240 <= hue < 300:
        r_prime = x_value
        g_prime = 0
        b_prime = c
    else:
        r_prime = c
        g_prime = 0
        b_prime = x_value

    r = int((r_prime + m) * 255)
    g = int((g_prime + m) * 255)
    b = int((b_prime + m) * 255)

    return (r, g, b)

def vel2col(x, y):
    magnitude = math.sqrt(x**2 + y**2)
    
    normalized_magnitude = min(magnitude / 30, 1)  
    
    hue = normalized_magnitude  # Full range from red (0) to green (1)
    saturation = 1.0
    value = 1.0
    
    # Convert HSV to RGB
    rgb = colorsys.hsv_to_rgb(hue, saturation, value)
    rgb = tuple(int(c * 255) for c in rgb)
    return rgb