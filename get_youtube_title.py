from pytube import YouTube

# YouTube video URL
url = 'https://www.youtube.com/watch?v=WDAnJpOuhI8'

# Create a YouTube object
yt = YouTube(url)

# Get the title of the video
video_title = yt.title

# Print the title of the video
print("Title of the video:", video_title)