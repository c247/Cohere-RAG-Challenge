
import re
from pytube import Playlist
from youtube_transcript_api import YouTubeTranscriptApi
import cohere
co = cohere.Client('rGjz0KNIMSReCgEyzpEUDQpYzxSoXb85RjjdyAel')
from pytube import YouTube
import json
import webbrowser


globalvideomap= {}
documents = []
urls = []

def storeURLS(url):
    playlist = Playlist(url)
    for url in playlist:
        urls.append(url)


def YoutubeParse(url):
    # Retrieve URLs of videos from playlist
    playlist = Playlist(url)
    print('Number Of Videos In playlist: %s' % len(playlist.video_urls))

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
        response = co.summarize(
        text=transcript,
        )
        video_idx[uid] = (youtube_url, transcript, response.summary)
        globalvideomap[uid] = youtube_url
        document = {
            'title: ': uid,
            'snippet': response.summary,
        }
        uid += 1

        documents.append(document)

    # print(video_idx)

    # Convert documents list to JSON format
    json_data = json.dumps(documents, indent=2)  # Convert list of dictionaries to JSON string

    # Print the JSON-formatted data
    print(json_data)

    # Write JSON data to a file
    output_file = 'documents.json'  
    with open(output_file, 'w') as file:
        file.write(json_data)



def process(response):
    citation_docs = response.citations
    # print(citation_docs)
    indexes_array = [entry['document_ids'][0] for entry in citation_docs]
    print("INDEX OF VIDEO")
    numbers_after_underscore = [int(entry.split('_')[1].split(':')[0]) if '_' in entry else None for entry in indexes_array]
    print(numbers_after_underscore[0] - 1)
    webbrowser.open(urls[numbers_after_underscore[0]])

def openVid():
    co = cohere.Client('rGjz0KNIMSReCgEyzpEUDQpYzxSoXb85RjjdyAel')
    with open('./documents_auto.json', 'r') as file:
        documents = json.load(file)
    response = co.chat(
    message= "what is a deadlock",
    documents=documents,
        prompt_truncation= "AUTO"
    )
    
    print(response.text)

    # print(citation_docs)
    # indexes_array = [entry['document_ids'][0] for entry in citation_docs]
    # val_array = [int(entry[-1]) for entry in indexes_array]
    # print(val_array)

    process(response)

url = input("Enter Youtube playlist URL: ")

# YoutubeParse(url)
storeURLS(url)

print("Output added to documents.json")

print("Generating Response...")

openVid()





