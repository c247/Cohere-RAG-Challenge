import cohere
import webbrowser


video_urls = {
    0: "https://www.youtube.com/watch?v=WDAnJpOuhI8&list=PLEoM_i-3sen_w5IYh0d5xtnpLHJeeO8l5&index=1&t=2834s&ab_channel=LesleytalksCS%2CGraphicsandFilm",
    1: "https://www.youtube.com/watch?v=63lbnckNkZ4&list=PLEoM_i-3sen_w5IYh0d5xtnpLHJeeO8l5&index=2&ab_channel=LesleytalksCS%2CGraphicsandFilm",
    2: "https://www.youtube.com/watch?v=Qid5OMJJ3x4&list=PLEoM_i-3sen_w5IYh0d5xtnpLHJeeO8l5&index=3&ab_channel=LesleytalksCS%2CGraphicsandFilm",
}

def process(response, video_urls):
    citation_docs = response.citations
    # print(citation_docs)
    indexes_array = [entry['document_ids'][0] for entry in citation_docs]
    val_array = [int(entry[-1]) for entry in indexes_array]
    youtube_video_url = video_urls[0]

    webbrowser.open(youtube_video_url)




co = cohere.Client('rGjz0KNIMSReCgEyzpEUDQpYzxSoXb85RjjdyAel')
response = co.chat(
  message= "Where do the tallest penguins live?",
  documents= [
    {
      "title": "Tall penguins",
      "snippet": "Emperor penguins are the tallest."
    },
    {
      "title": "Penguin habitats",
      "snippet": "Emperor penguins only live in Antarctica."
    },
    {
      "title": "What are animals?",
      "snippet": "Animals are different from plants."
    }
  ],
    prompt_truncation= "AUTO"
)
# print(response)

citation_docs = response.citations

# print("The response is ")

# print(citation_docs)
# indexes_array = [entry['document_ids'][0] for entry in citation_docs]
# val_array = [int(entry[-1]) for entry in indexes_array]
# print(val_array)

process(response, video_urls)
