import os
import time
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel, Field

load_dotenv()
my_api_key=os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key kaha hai bhai")

client=Groq(api_key=my_api_key)
model = "openai/gpt-oss-120b"

def llm_ans(prompt):
    message={
        "role":"user",
        "content":prompt
    }

    messages=[message]
    response=client.chat.completions.create(
        model=model,messages=messages)

    answer=response.choices[0].message.content
    return answer

   # bad prompt

bad_prompt="""
                 #Role:
                 You are a support assistant at a laptop compny 
                 #Contraints
                    - You should classify the user complaint into one of the three  categories namely:Billing, technical,return
                #Output Format:
                    - You should only return the category name in your response
                #Example 
                For instance if a user complaint says he wants refund ten the categories should be return

                # Fallback 
                If the issue is unrealated to any of the categories then answer should be other

                
                 THis is a user complaint: 
                 My Girlfriend left me
"""

print (llm_ans(bad_prompt))