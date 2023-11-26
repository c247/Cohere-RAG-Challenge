import re
from pytube import Playlist
from youtube_transcript_api import YouTubeTranscriptApi


# URL of the YouTube playlist
URL_PLAYLIST = "https://www.youtube.com/playlist?list=PLEoM_i-3sen_w5IYh0d5xtnpLHJeeO8l5"

# Retrieve URLs of videos from playlist
playlist = Playlist(URL_PLAYLIST)
print('Number Of Videos In playlist: %s' % len(playlist.video_urls))

urls = []
for url in playlist:
    urls.append(url)

# print(urls)

video_ids = []

pattern = r'(?<=v=)[\w-]+'

for youtube_url in urls:
    # Find the video ID using regex
    match = re.search(pattern, youtube_url)

    if match:
        video_id = match.group()
        video_ids.append(video_id)
        # print("Video ID:", video_id)
    else:
        print("Video ID not found.")

# print(video_ids)

for id in video_ids:
    # retrieve the available transcripts
    transcript_list = YouTubeTranscriptApi.list_transcripts(id)

    # using the srt variable with the list of dictionaries
    # obtained by the .get_transcript() function
    srt = YouTubeTranscriptApi.get_transcript(id)

    transcripts = {}
    transcript = '\n'.join(i["text"] for i in srt)
    transcripts[id] = transcript

# print(transcripts)
