import os
from pathlib import Path
import time
from dotenv import load_dotenv
from groq import Groq
import time

load_dotenv()
my_api_key= os.getenv("GROQ_API_KEY")

if not my_api_key :
    raise ValueError("GROK API KEY is not  set")

client = Groq(api_key=my_api_key)
 
model="openai/gpt-oss-120b"

JD="""
We are hiring a Backend Python Developer.

Requirements:
- Strong Python
- FastAPI or Django
- PostgreSQL
- Docker
- AWS
- REST APIs
- 2+ years of experience
"""

RESUME="""
Name: Rahul Sharma

Experience:
3 years as a Software Developer.

Skills:
Python, FastAPI, MySQL, Docker,
REST APIs, Git

Projects:
Built a food delivery backend using
FastAPI and MySQL.

Deployed applications using Docker.


"""

def ask_llm(system_prompt,user_prompt):
    sys_msg={
        "role": "system",
        "content": str(system_prompt)
    }
    user_msg={
        "role": "user",
        "content": str(user_prompt)
    }

    messages=[sys_msg,user_msg]

    # print("SYSTEM PROMPT:", system_prompt)
    # print("SYSTEM TYPE:", type(system_prompt))

    # print("USER PROMPT:", user_prompt)
    # print("USER TYPE:", type(user_prompt))
    response = client.chat.completions.create(model=model, messages=messages)

    answer=response.choices[0].message.content
    return answer;

def step1_res_extract( ):
    system_prompt =  """"You are a professional hr assistant that extracts skills from resumes only return the skill no other information. Do not invent any skills by your self ."""
    user_prompt = """"""
 
    return ask_llm(system_prompt, user_prompt)


def step2_JD_extract( ):
    system_prompt = "You are a professional hr assistant that extracts skills from JOB DESCRIPTIONS  only return the skill no other information. Do not invent any skills by your self ."
    user_prompt = f"Extract the skills from the following jd:\n{JD}"
    
    return ask_llm(system_prompt, user_prompt)

def step3_compare_skills(resume_skills, jd_skills):
    system_prompt="You are a professional hr assistant compare the skills of candidate and the required skills in jd and produce a final score between 1 to 100. also produce a short  verdict wheather the candidate is a good fit for job or not",
    user_prompt=f"Compare the following skills:\nResume Skills: {RESUME}\nJD Skills: {JD}"

    return ask_llm(system_prompt, user_prompt)

resume_skills=step1_res_extract()
time.sleep(2)
jd_skills=step2_JD_extract()
time.sleep(2)

score=step3_compare_skills(resume_skills, jd_skills)

print(score)