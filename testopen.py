
from openai import OpenAI

client = OpenAI(api_key="",)
global usermsg
response = client.chat.completions.create(
model="gpt-3.5-turbo",
messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": f" what is the square root of 225."}
]
)
print(response)
print(response.choices[0].message.content)
