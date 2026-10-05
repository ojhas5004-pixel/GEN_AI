import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
my_api_key= os.getenv("GROK_API_KEY")

if not my_api_key :
    raise ValueError("GROK API KEY is not  set")

client = Groq(api_key=my_api_key)
 
model="openai/gpt-oss-120b"
role ="user"
prompt="Suggest a name for my milk shop"

#this is a system message which will be used to set the context for the model

# message_system={
#     "role":"system",
#     "content":"You are a cricket expert and you have to answer the question in 2 lines"
# }

message_system={
    "role":"system",
    "content":"You are a  brand manager who suggeset name for my company , name should be in one word , suggest only one name"
}

#this is a user message which will be used to ask the question to the model
message={
    "role":role,
    "content":prompt
}

#first we will pass the system message to the model and then we will pass the user message to the model

messages=[message_system, message]

response = client.chat.completions.create(model=model, messages=messages,temperature=2 )
print(response)

print("##############################")
    
answer = response.choices[0].message.content

print(answer)