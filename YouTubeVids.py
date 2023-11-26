from pytube import Playlist

URL_PLAYLIST = "https://www.youtube.com/playlist?list=PLEoM_i-3sen_w5IYh0d5xtnpLHJeeO8l5"

# Retrieve URLs of videos from playlist
playlist = Playlist(URL_PLAYLIST)
print('Number Of Videos In playlist: %s' % len(playlist.video_urls))

urls = []
for url in playlist:
    urls.append(url)

print(urls)