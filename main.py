
import re
from pytube import Playlist
from youtube_transcript_api import YouTubeTranscriptApi
import cohere
co = cohere.Client('rGjz0KNIMSReCgEyzpEUDQpYzxSoXb85RjjdyAel')
from pytube import YouTube
import json
import webbrowser
from pytube import YouTube
import streamlit as st


# Global variables
transcriptSelected = 0
globalvideomap= {}
documents = []
urls = []
transcripts = []
global usermsg

def storeURLS(url):
    playlist = Playlist(url)
    for url in playlist:
        urls.append(url)

def Transcript(url):
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


        # using the srt variable with the list of dictionaries
        # obtained by the .get_transcript() function
        srt = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = '\n'.join(i["text"] for i in srt)
        transcripts.append(transcript)

def YoutubeParse(url):
    # Retrieve URLs of videos from playlist
    playlist = Playlist(url)
    print('Number Of Videos In playlist: %s' % len(playlist.video_urls))

    print(urls)


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
        print(transcript)
        response = co.summarize(
        text=transcript,
        )
        video_idx[uid] = (youtube_url, transcript, response.summary)
        globalvideomap[uid] = youtube_url
        document = {
            'title': str(uid),
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
    output_file = 'documents_auto.json'  
    with open(output_file, 'w') as file:
        file.write(json_data)



def process(response):
    citation_docs = response.citations
    print(citation_docs)
    indexes_array = [entry['document_ids'][0] for entry in citation_docs]
    print("INDEX OF VIDEO")
    numbers_after_underscore = [int(entry.split('_')[1].split(':')[0]) if '_' in entry else None for entry in indexes_array]
    print(numbers_after_underscore[0])
    global transcriptSelected 
    transcriptSelected = numbers_after_underscore[0]
    return urls[numbers_after_underscore[0]]

# def getdocindex(response):
#     citation_docs = response.citations
#     # print(citation_docs)
#     indexes_array = [entry['document_ids'][0] for entry in citation_docs]
#     print("INDEX OF VIDEO")
#     numbers_after_underscore = [int(entry.split('_')[1].split(':')[0]) if '_' in entry else None for entry in indexes_array]
#     print(numbers_after_underscore[0]-1)

    

def openVid():
    global usermsg
    msg = usermsg
    
    print("Finding relevant course video...")

    print("Opening Video")
    co = cohere.Client('rGjz0KNIMSReCgEyzpEUDQpYzxSoXb85RjjdyAel')
    with open('./documents_auto.json', 'r') as file:
        documents = json.load(file)
    response = co.chat(
    message= msg,
    documents=documents,
        prompt_truncation= "AUTO"
    )
    
    print(response.text)


    vidurl = process(response)
    return vidurl



def finalOpenTime(time, url):
    urltime = url + "&t=" + str(time)
    webbrowser.open(urltime)

def find_question_position_basic(transcript, question):
    """
    Find the percentage of the transcript where the question is answered without using NLP.

    Parameters:
    - transcript (str): The transcript of the lecture.
    - question (str): The question to search for in the transcript.

    Returns:
    - float: The percentage of the transcript where the question is answered.
    """
    # Convert both transcript and question to lowercase for case-insensitive comparison
    transcript_lower = transcript.lower()
    question_lower = question.lower()

    # Find the position of the question in the transcript
    question_start = transcript_lower.find(question_lower)

    # If the question is not found, return -1
    if question_start == -1:
        return -1

    # Calculate the percentage position based on the character offsets
    percentage_position = (question_start / len(transcript_lower))
    print("percent")
    print(percentage_position)
    return percentage_position



def action(url, msg):
    storeURLS(url)
    YoutubeParse(url)

    Transcript(url)

    print("Output added to documents.json")


    vidurl = openVid()

    print("*********************")
    print(usermsg)

    yt = YouTube(vidurl)  
    video_length = yt.length
    print(video_length)
    percentPos = find_question_position_basic(transcripts[transcriptSelected], usermsg)
    time = int(video_length * percentPos)
    print(time)
    finalOpenTime(time, vidurl)


def main():
    st.title("YouTube Transcript Analysis")
    global usermsg
    # Accept playlist URL and user message
    url = st.text_input("Enter YouTube playlist URL:")
    usermsg = st.text_input("What do you want to learn?")

    # Button to trigger the action
    if st.button("Generate Summary and Open Video"):
        action(url, usermsg)

# Run the Streamlit app
if __name__ == "__main__":
    main()





