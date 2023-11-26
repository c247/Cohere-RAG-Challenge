# importing the module
from youtube_transcript_api import YouTubeTranscriptApi

# retrieve the available transcripts
transcript_list = YouTubeTranscriptApi.list_transcripts('WDAnJpOuhI8&')

# using the srt variable with the list of dictionaries
# obtained by the .get_transcript() function
srt = YouTubeTranscriptApi.get_transcript("WDAnJpOuhI8&")

# creating or overwriting a file "subtitles.txt" with
# the info inside the context manager
with open("subtitles.txt", "w") as f:

        # iterating through each element of list srt
    for i in srt:
        # writing each element of srt on a new line
        f.write("{}\n".format(i["text"]))