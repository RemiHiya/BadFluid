from moviepy.editor import VideoFileClip

def addAudio(name):
    clip_with_audio = VideoFileClip("badapple.mp4")
    clip_without_audio = VideoFileClip(f"bad{name}.mp4")
    audio_clip = clip_with_audio.audio
    video_with_audio = clip_without_audio.set_audio(audio_clip)
    video_with_audio.write_videofile(f"bad{name}_audio.mp4", codec='libx264')