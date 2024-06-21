import pygame
from random import random
import cv2
from fluid import *
from frame import *
import os
import shutil
from moviepy.editor import ImageSequenceClip, VideoFileClip, AudioFileClip

pygame.init()
clock = pygame.time.Clock()
time = 0

scale = float(input("Rebder scale : "))
cap = cv2.VideoCapture("badapple.mp4")
tmp = get_binary_image_at_time(cap, 0, scale)
nb_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

width, height = len(tmp[0]), len(tmp)
pixel_size = 1
diffusion = 0
viscosity = 0
dt = .000003
screen_width, screen_height = width * pixel_size, height * pixel_size

fluid = Fluid(width, height, diffusion, viscosity, dt)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Bad fluid")

frame_count = 0
output_folder = 'frames'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def render_badapple(t):
    img = get_binary_image_at_time(cap, t, scale)
    for i in range(height):
        for j in range(width):
            moy = (fluid.density[j, i] + img[i][j] * 255) / 2
            fluid.obstacles[j ,i] = bool(1-img[i][j])
            fluid.density[j, i] = moy
            # if img[i][j] > 0:
            #     a, b = random() * 2 -1, random() * 2 -1
            #     fluid.add_velocity(j, i, a, b)


print("Start rendering.")
running = True
while frame_count < nb_frame and running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    render_badapple(time)
    fluid.step()
    if frame_count % 30 == 0:
        print(f"Frame {frame_count}/{nb_frame}")

    screen.fill((0, 0, 0))
    for i in range(width):
        for j in range(height):
            fluid.add_velocity(i, j, 0, 9)
            fluid.fade_velocity(i, j)
            d = int(fluid.density[i, j])
            d = max(min(255, d), 0)
            r, g, b = vel2col(fluid.Vx[i, j], fluid.Vy[i, j])
            r *= d/255
            g = min(255, g*d/255 + r)
            b = min(255, b*d/255 + r)
            col = (r, g, b)
            pygame.draw.rect(screen, col, (i * pixel_size, j * pixel_size, pixel_size, pixel_size))

    frame_filename = os.path.join(output_folder, f'frame_{frame_count:04d}.png')
    pygame.image.save(screen, frame_filename)
    frame_count += 1
    pygame.display.flip()
    time += 1/30 
    # fluid.dt = clock.tick() /100

pygame.quit()


final = "badfluid.mp4"
fps = 30
image_files = [os.path.join(output_folder, f'frame_{i:04d}.png') for i in range(frame_count)]
clip = ImageSequenceClip(image_files, fps=fps)
clip.write_videofile(final, codec='libx264')

# clip_with_audio = VideoFileClip("badapple.mp4")
# clip_without_audio = VideoFileClip(final)
# audio_clip = clip_with_audio.audio
# video_with_audio = clip_without_audio.set_audio(audio_clip)
# video_with_audio.write_videofile(final, codec='libx264')

shutil.rmtree(output_folder)