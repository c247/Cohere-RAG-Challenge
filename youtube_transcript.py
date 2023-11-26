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


pattern = r'(?<=v=)[\w-]+'

video_idx = {}
uid = 0

for youtube_url in urls:
    match = re.search(pattern, youtube_url)

    if match:
        video_id = match.group()
    else:
        print("Video ID not found.")

    # retrieve the available transcripts
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

    # using the srt variable with the list of dictionaries
    # obtained by the .get_transcript() function
    srt = YouTubeTranscriptApi.get_transcript(video_id)

    transcript = '\n'.join(i["text"] for i in srt)
    video_idx[uid] = (youtube_url, transcript)
    uid += 1

print(video_idx)
