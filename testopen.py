
from openai import OpenAI

client = OpenAI(api_key="",)
global usermsg
response = client.chat.completions.create(
model="gpt-4-1106-preview",
messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": f" what is the square root of 225 - answer in json with a field called answer and value being an number"}
],
response_format={"type": "json_object"},
)
# print(response)
print(int(eval(response.choices[0].message.content)["answer"]))
