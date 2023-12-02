
import re
from pytube import Playlist
from youtube_transcript_api import YouTubeTranscriptApi
import cohere

from pytube import YouTube
import json
import webbrowser
from pytube import YouTube
import streamlit as st
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
co = cohere.Client(st.secrets["coherekey"])

# Global variables
transcriptSelected = 0
globalvideomap= {}
documents = []
urls = []
transcripts = []
global usermsg
global finalURL
finalURL = ""

def storeURLS(url):
    playlist = Playlist(url)
    for url in playlist:
        urls.append(url)

def Transcript(url):
    # Retrieve URLs of videos from playlist
    playlist = Playlist(url)
    # print('Number Of Videos In playlist: %s' % len(playlist.video_urls))

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
    # print('Number Of Videos In playlist: %s' % len(playlist.video_urls))

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
        # print(transcript)
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
    # print(json_data)

    # Write JSON data to a file
    output_file = 'documents_auto.json'  
    with open(output_file, 'w') as file:
        file.write(json_data)



def process(response):
    citation_docs = response.citations
    # print(citation_docs)
    indexes_array = [entry['document_ids'][0] for entry in citation_docs]
    # print("INDEX OF VIDEO")
    numbers_after_underscore = [int(entry.split('_')[1].split(':')[0]) if '_' in entry else None for entry in indexes_array]
    # print(numbers_after_underscore[0])
    global transcriptSelected 
    transcriptSelected = numbers_after_underscore[0]
    return urls[numbers_after_underscore[0]]

def processToGetDocIndex(response):
    citation_docs = response.citations
    # print(citation_docs)
    indexes_array = [entry['document_ids'][0] for entry in citation_docs]
    # print("INDEX OF VIDEO")
    numbers_after_underscore = [int(entry.split('_')[1].split(':')[0]) if '_' in entry else None for entry in indexes_array]
    # print(numbers_after_underscore[0])
    return numbers_after_underscore[0]

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
    
    # print("Finding relevant course video...")

    # print("Opening Video")
    co = cohere.Client(st.secrets["coherekey"])
    with open('./documents_auto.json', 'r') as file:
        documents = json.load(file)
    response = co.chat(
    message= msg,
    documents=documents,
        prompt_truncation= "AUTO"
    )
    
    # print(response.text)


    vidurl = process(response)
    return vidurl



def finalOpenTime(time, url):
    urltime = url + "&t=" + str(time)
    global finalURL
    finalURL = urltime
    # webbrowser.open(urltime)


def split_transcript(transcript, max_words=300):
    print(transcript)
    words = transcript.split()
    grouped_transcripts = []

    current_group = []
    current_word_count = 0

    for word in words:
        current_group.append(word)
        current_word_count += 1

        if current_word_count >= max_words:
            grouped_transcripts.append(" ".join(current_group))
            current_group = []
            current_word_count = 0

    if current_group:
        grouped_transcripts.append(" ".join(current_group))

    return grouped_transcripts


def create_json_array(grouped_transcripts):
    json_array = []

    for idx, group in enumerate(grouped_transcripts):
        # You can replace this with your actual logic to generate summaries
        response_summary = f"Summary for part {idx + 1}"

        json_object = {
            "title": str(idx),
            "snippet": response_summary,
        }

        json_array.append(json_object)

    return json_array


def find_question_position_basic(transcript, question):
    """
    Find the percentage of the transcript where the question is answered without using NLP.

    Parameters:
    - transcript (str): The transcript of the lecture.
    - question (str): The question to search for in the transcript.

    Returns:
    - float: The percentage of the transcript where the question is answered.
    """
    # grouped = split_transcript(question)
    # totalDocuments = len(grouped)
    # jsonDocuments = create_json_array(grouped)
    # global usermsg
    # response = co.chat(
    #     message=usermsg ,
    #     documents=jsonDocuments,
    #     prompt_truncation= "AUTO"
    # )

    # indexOfDocument = processToGetDocIndex(response)
    # return indexOfDocument/totalDocuments
    
    # print(transcript)
    # # Convert both transcript and question to lowercase for case-insensitive comparison
    # transcript_lower = transcript.lower()
    # question_lower = question.lower()

    # # Find the position of the question in the transcript
    # question_start = transcript_lower.find(question_lower)

    # # If the question is not found, return -1
    # if question_start == -1:
    #     return -1

    # # Calculate the percentage position based on the character offsets
    # percentage_position = (question_start / len(transcript_lower))
    # print("percent")
    # print(percentage_position)
    # return percentage_position

    client = OpenAI(api_key=st.secrets["openaikey"],)
    global usermsg
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"{transcript} \n What percent way through what percent way through the text is: \n  ~ {usermsg} ~\n talked about\n Just give me a single integer without the percent sign in the output no explanation or extra text needed."}
    ]
    )
    print(response)
    val = int(response.choices[0].message.content)
    return val/100


def action(url, msg):
    storeURLS(url)
    YoutubeParse(url)

    Transcript(url)

    # print("Output added to documents.json")


    vidurl = openVid()

    # print("*********************")
    # print(usermsg)

    yt = YouTube(vidurl)  
    video_length = yt.length
    # print(video_length)
    percentPos = find_question_position_basic(transcripts[transcriptSelected], usermsg)
    time = int(video_length * percentPos)
    # print(time)
    finalOpenTime(time, vidurl)


def main():
    st.title("GoHere Youtube Playlist AI Search")
   

    global usermsg
    # Accept playlist URL and user message
    url = st.text_input("Enter YouTube playlist URL:")
    usermsg = st.text_input("What do you want to learn?")

    # Button to trigger the action
    if st.button("Submit"):
        global finalURL
        finalURL = ""
        action(url, usermsg)
        if finalURL:
            st.success(f"Final URL: {finalURL}")
        # st.write("Made by: [Vijay](link-to-vijay-github), [Katarina](link-to-katarina-github), [Maryam](link-to-maryam-github)")

    footer_container = st.container()

    # st.write("Made by: [Vijay](link-to-vijay-github), [Katarina](link-to-katarina-github), [Maryam](link-to-maryam-github)")
    hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_st_style, unsafe_allow_html=True)
# Run the Streamlit app
if __name__ == "__main__":
    main()





