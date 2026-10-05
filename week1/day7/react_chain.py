import os
import re
import time

from dotenv import load_dotenv
from groq import Groq


# -----------------------------
# Load API key
# -----------------------------

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("GROQ_API_KEY kaha hai bhai")


# -----------------------------
# Groq client
# -----------------------------

client = Groq(api_key=my_api_key)

model = "openai/gpt-oss-120b"


# -----------------------------
# Tools
# -----------------------------

def get_price(product):
    product = product.lower().strip()

    # Handle both "iphone" and "i phone"
    product = product.replace("i phone", "iphone")

    if product == "iphone 17":
        return 1000

    elif product == "iphone 15":
        return 500

    else:
        return "Product not found"


def calculator(expression):
    try:
        return eval(expression)
    except Exception:
        return "Calculation error"


tools = {
    "get_product_price": get_price,
    "calculator": calculator
}


# -----------------------------
# System prompt
# -----------------------------

system_prompt = """
You are a shopping assistant.

You have these tools:

get_product_price(product)
calculator(expression)

Important:

Call tools exactly like these examples:

Action:get_product_price("iphone 17")
Action:calculator("5000-1000")

Never write:

calculator(expression="5000-1000")

Never write:

get_product_price(product="iphone 17")

Follow these rules:

1. Decide what you need to do next.
2. Call only one tool at a time.
3. After writing an Action, stop immediately.
4. Never guess or invent a tool result.
5. Wait until you receive an Observation.
6. Then decide your next action.
7. When the task is complete, give the Final Answer.

Format:

Thought: What you need to do
Action: tool_name(argument)

When finished:

Final Answer: your answer
"""


# -----------------------------
# ReAct Agent
# -----------------------------

def run_agent(question):

    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": question
        }
    ]

    for step in range(5):

        print("\n-----------")
        print("Step", step + 1)
        print("-----------\n")

        # -----------------------------
        # Ask LLM
        # -----------------------------

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0
        )

        answer = response.choices[0].message.content

        print(answer)

        # -----------------------------
        # Check if agent finished
        # -----------------------------

        if "Final Answer:" in answer:
            break

        # -----------------------------
        # Find Action
        # -----------------------------

        match = re.search(
            r'Action:\s*(\w+)\("(.*?)"\)',
            answer
        )

        if not match:
            print("No valid action found.")
            break

        # Extract tool name and input
        tool_name = match.group(1)
        tool_input = match.group(2).strip()

        print("Tool:", tool_name)
        print("Input:", tool_input)

        # -----------------------------
        # Run tool
        # -----------------------------

        if tool_name in tools:

            tool = tools[tool_name]

            observation = tool(tool_input)

        else:

            observation = "Tool not found"

        print("Observation:", observation)

        # -----------------------------
        # Add assistant response
        # -----------------------------

        messages.append({
            "role": "assistant",
            "content": answer
        })

        # -----------------------------
        # Give tool result to LLM
        # -----------------------------

        messages.append({
            "role": "user",
            "content": "Observation: " + str(observation)
        })

        time.sleep(1)


# -----------------------------
# User question
# -----------------------------

prompt = """
I have 5000 rupees. What is the price of an i phone 17?
And how much money will I have left after buying it?
"""

run_agent(prompt)