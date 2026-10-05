import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

my_api_key = os.getenv("GROK_API_KEY")

if not my_api_key:
    raise ValueError("GROK API KEY is not set")

client = Groq(api_key=my_api_key)

model = "openai/gpt-oss-120b"
role = "user"

# 3 prompts to test the model
prompt1 = "Hi"
prompt2 = "Explain time travel in simple words"
prompt3 = "Write an essay on how to sharpen your mind in 100 words"

prompts = [prompt1, prompt2, prompt3]

for prompt in prompts:

    message = {
        "role": role,
        "content": prompt
    }

    messages = [message]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=600,
    )

    usage = response.usage


 # calculating tokens used for each prompt and printing the result

    print(f"\nPrompt: {prompt}")
    print(f"Your tokens: {usage.prompt_tokens}")
    print(f"Completion tokens: {usage.completion_tokens}")
    print(f"Total tokens: {usage.total_tokens}")

    # printing the finish reason for each prompt
    print(f"Finish reason: {response.choices[0].finish_reason}")

    # answer = response.choices[0].message.content
    # print(f"Answer: {answer}")
