
import re
from pytube import Playlist
from youtube_transcript_api import YouTubeTranscriptApi
import cohere
import concurrent.futures
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
# co = cohere.Client(os.getenv("COHERE_KEY"))

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



def YoutubeParse(url):
    # Retrieve URLs of videos from playlist

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
 

def openVid():
    global usermsg
    msg = usermsg
    
    # print("Finding relevant course video...")

    # print("Opening Video")
    co = cohere.Client(st.secrets["coherekey"])
    # co = cohere.Client(os.getenv("COHERE_KEY"))

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



def find_question_position_basic(transcript, question, video_length):

    client = OpenAI(api_key=st.secrets["openaikey"],)
    # client = OpenAI(api_key=os.getenv("API_KEY"),)


    global usermsg

    
    response = client.chat.completions.create(
    model="gpt-4-1106-preview",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Look at this transcript(between the ~ signs) of a class lecture:\n\n ~{transcript}~ \n\n The video corresponding to the above transcript is {video_length} seconds long. What approximate percent way through the video should I open the video such that the question/prompt: \n\n  ~{usermsg}~ \n\n answered/talked about in that point in the video .\n Just give me a single integer without the percent sign in the output/response no explanation or extra text needed."}
    ],
    )
    print("openai")
    print(response)
    
    val = int(response.choices[0].message.content)
    print(val)
    return val/100


def action(url, msg):
    storeURLS(url)
    YoutubeParse(url)

    # print("Output added to documents.json")


    vidurl = openVid()

    # print("*********************")
    # print(usermsg)

    yt = YouTube(vidurl)  
    video_length = yt.length
    # print(video_length)
    percentPos = find_question_position_basic(transcripts[transcriptSelected], usermsg, video_length)
    time = int(video_length * percentPos)
    # print(time)
    finalOpenTime(time, vidurl)

global user_authenticated
user_authenticated = True
def main():
    st.set_page_config(
        page_title="GoHere",
        page_icon="📚", 
    )

    if user_authenticated:
        st.title("GoHere")
        st.subheader("Youtube Playlist AI Assistant")
        hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            .made-by {
                position: fixed;
                bottom: 10px;
                left: 10px;
                font-size: 18px;
                color: #777;
                display: flex;
                align-items: center;
                text-decoration: underline;
            }
            .github-logo {
                height: 30px;
                width: 30px;
                margin-right: 5px;
            }
            .made-by a {
                text-decoration: none;  /* Remove blue hyperlink styling */
                color: #777;  /* Set the color to a desired value */
                margin-right: 10px;  /* Add space between the names */
            }
            </style>
            """
        st.markdown(hide_st_style, unsafe_allow_html=True)

        st.markdown('<div class="made-by">'
                    '<img class="github-logo" src="https://github.githubassets.com/assets/GitHub-Mark-ea2971cee799.png" alt="GitHub Logo">'
                    '<a href="https://github.com/c247">Vijay </a> '
                    '<a href="https://github.com/katarinamak">Katarina </a> '
                    '<a href="https://github.com/mary1afshar">Maryam</a>'
                    '</div>', unsafe_allow_html=True)

        global usermsg
           # Create the expander for "How to"
        with st.expander("?"):
            st.markdown("<h4 style='color: #0066cc; '>GoHere uses Cohere's RAG (Retrieval Augmented Generation) capabilities to assist you with your study search</h3>", unsafe_allow_html=True)
            st.write("1. Enter the YouTube playlist URL of lecture content")
            st.write("2. Enter what you want to learn")
            st.write("3. Click the 'Submit' button")
            st.write("4. Wait...for a while")
            st.write("5. GoHere will locate the specific video and timestamp where the content is covered and also provide its best explanation")
        url = st.text_input("Enter YouTube playlist URL:")
        usermsg = st.text_input("What do you want to learn?")
        client = OpenAI(api_key=st.secrets["openaikey"],)
        # client = OpenAI(api_key=os.getenv("API_KEY"),)
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"{usermsg}"}
            ],
        )

        
        # Button to trigger the action
        if st.button("Submit"):
            with st.spinner("Searching..."):
                global finalURL
                finalURL = ""
                
                action(url, usermsg)
                
                if finalURL:
                    st.success(f"Final URL: {finalURL}")
                    st.success(f"Query Answer: {response.choices[0].message.content}")

     

        footer_container = st.container()

        
# Run the Streamlit app
if __name__ == "__main__":
    main()





