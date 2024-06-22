import pygame
import cv2
from fluid import *
from utils import *
from badpoly import *
from badsketch import *
import os
import shutil
from moviepy.editor import ImageSequenceClip

# Global params
name = "sketch"
scale = 1


pygame.init()
clock = pygame.time.Clock()
time = 0

cap = cv2.VideoCapture("badapple.mp4")
tmp = get_binary_image_at_time(cap, 0, scale)
nb_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

width, height = len(tmp[0]), len(tmp)
pixel_size = 1
screen_width, screen_height = width * pixel_size, height * pixel_size


screen = pygame.display.set_mode((screen_width/scale, screen_height/scale))
pygame.display.set_caption(f"Bad {name}")

###
remix = BadSketch(cap, scale, screen)
###

output_folder = "frames"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)


print("Start rendering.")
running = True
while remix.frame < nb_frame and running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    screen.fill((0, 0, 0))
    remix.render()

    frame_filename = os.path.join(output_folder, f"frame_{remix.frame:04d}.png")
    pygame.image.save(screen, frame_filename)
    pygame.display.flip()
    pygame.display.set_caption(f"Bad {name} - {100*remix.frame/nb_frame}%")

pygame.quit()


final = f"bad{name}.mp4"
fps = 30
image_files = [os.path.join(output_folder, f"frame_{i:04d}.png") for i in range(remix.frame)]
clip = ImageSequenceClip(image_files, fps=fps)
clip.write_videofile(final, codec='libx264')

shutil.rmtree(output_folder)