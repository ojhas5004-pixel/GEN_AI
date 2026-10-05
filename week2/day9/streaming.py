import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
my_api_key= os.getenv("GROQ_API_KEY")

if not my_api_key :
    raise ValueError("GROK API KEY is not  set")

client = Groq(api_key=my_api_key)
 
model="openai/gpt-oss-120b"

prompt="Explain how internet works in simple word"

message={
    "role" : "user",
    "content" : prompt  
}

messages=[message]

# print response1

# response1= client.chat.completions.create(model=model, messages=messages)

 

# answer = response1.choices[0].message.content
# print(answer)

# print response2

response2= client.chat.completions.create(model=model, messages=messages,stream=True)

for chunk in response2:
    content = chunk.choices[0].delta.content
    if content:
        print(content,end="",flush=True)



