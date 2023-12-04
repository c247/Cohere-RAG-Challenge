
from openai import OpenAI

client = OpenAI(api_key="",)
global usermsg
response = client.chat.completions.create(
    model="gpt-4-1106-preview",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"The cross-product is a binary operation between two vectors in three-dimensional space. If two vectors, let's say a and b, are angled at theta to each other, their cross-product is equal to the magnitude of a times b times the sine of theta. The direction of the cross product is perpendicular to the plane made by the two original vectors and can be determined using Fleming's left-hand and right-hand rules. Conventionally, the cross-product is positive when the vectors are in a specific order and negative in the reverse order. Understanding this convention is essential as it will be used in later chapters to determine the direction of cross products. \n What percent way through what percent way through the question/prompt inside the ~ signs: \n  ~binary operations~\n talked about/answered.\n Answer single integer without the percent sign in the output/response no explanation or extra text needed"}
    ],
)
# print(response)
print(response.choices[0].message.content)
