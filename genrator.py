import os
import random
import time
import asyncio
import pandas as pd
from openai import AsyncOpenAI
from math import isnan
from bs4 import BeautifulSoup 
import markdown

from dotenv import load_dotenv, dotenv_values 
# loading variables from .env file

def load_environment():
    load_dotenv()
    print(os.getenv("OPEN_AI_KEY"))

def get_sheet(sheetID,tabID):
    None

def api_client(API_KEY):
    client = AsyncOpenAI(api_key=API_KEY)
    return client

async def writer(client, command) -> str:
    chat_completion = await client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": command
        }
    ],
    model="gpt-4o-2024-05-13",
    max_tokens=4096
    )
    gpt_return = dict(chat_completion)
    
    #This entire, humongous section is to get rid of some empty spaces, DO NOT TOUCH IT WORKS
    multiline_string = gpt_return['choices'][0].message.content
    num_of_lines = multiline_string.count("\n") + 1
    str_in_list = multiline_string.split("\n")[1:]
    new_str1 = ""
    for item in str_in_list:
        new_str1 += item
        new_str1 += '\n'
    num_of_lines = new_str1.count("\n") + 1
    str_in_list = new_str1.split("\n")[:num_of_lines-1]
    new_str2 = ""
    for item in str_in_list:
        new_str2 += item
        new_str2 += '\n'
 
    return new_str2

def main():
    print(os.environ.get("OPEN_AI_KEY"))
    client = api_client(os.environ.get("OPEN_AI_KEY"))
    command = "Write me a 2000 words blog post about gambling (in Markdown Format)"
    bp = asyncio.run(writer(client,command))
    # print(bp)
    command = "Summarize: " + bp
    summary = asyncio.run(writer(client,command))
    # print(summary)
    command = "Create 10 Frequently Asked Questions (in Markdown Format) for a blog about: " + summary
    faq = asyncio.run(writer(client,command))
    # print(faq)
    command = "Create a key takeaway table (in HTML Format) with 10 rows for a blog about: " + summary
    key_table = asyncio.run(writer(client,command))
    text = bp + "\n" + faq + "\n"
    tempHTML = markdown.markdown(text)

    with open("output.html", "w", encoding = 'utf-8') as file: 
        file.write(tempHTML + "\n\n\n" + key_table)


if __name__ == "__main__":
    main()