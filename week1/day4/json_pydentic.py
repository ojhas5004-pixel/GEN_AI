import os
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("GROQ API KEY is not set")

client = Groq(api_key=my_api_key)

model = "openai/gpt-oss-120b"
role = "user"


# Define the structure
class Ticket(BaseModel):
    issue: str
    name: str
    email: str
    contact_no: int
    address: str
 


# Generate JSON schema AFTER the class is created
Schema = Ticket.model_json_schema()

response_format = {
    "type": "json_object"
}


system_prompt = f"""
Extract the information from the customer complaint
and return the data in JSON format strictly based on this schema:

{Schema}
"""


text = """Hello, my name is Saurabh. I have an iPhone which is
not working at all. My address is Bhopal.
My email address is abc@gmail.com.
My contact number is 8763329873."""


prompt = f"""
This is a customer complaint. Please extract the information from it.

Customer complaint:
{text}
"""


message_system = {
    "role": "system",
    "content": system_prompt
}

message = {
    "role": role,
    "content": prompt
}

messages = [message_system, message]


response = client.chat.completions.create(
    model=model,
    messages=messages,
    response_format=response_format,
    temperature=0
)

answer = response.choices[0].message.content

print(answer)

# isko padhte kaise hai 
# ham isko bhi paas kr sakte hai taki padhne me aasani ho
import json 
raw_json=answer
parsed_json = json.loads(raw_json)

ticket=Ticket(**parsed_json)

print(ticket)


# homework => take a resume which is in pdf or word and extract the information from it and return it in JSON fomat , where hr will give you a list of fields like skills,experiance, projects,extract these and match against hr requirements and return the percentage of matching or not
