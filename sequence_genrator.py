import os
import random
import time
import asyncio
import pandas as pd
import openai
from math import isnan
from bs4 import BeautifulSoup 
import markdown

from dotenv import load_dotenv, dotenv_values 

def load_environment():
    load_dotenv()
    print(os.getenv("OPEN_AI_KEY"))

api_key = os.getenv("OPEN_AI_KEY")

spreadsheet_id = "1_RlqjuGBPPi4gVAdWgVFpyPVu9QeqKC4jgZSkwPcTgw"
tab_id = "1919817288"

excel_commands = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?gid={tab_id}&format=csv")

## Messages

messages = [
    {"role": "system", "content": excel_commands['Commands'][0]}
]

client = openai.OpenAI(api_key=api_key)

response = client.chat.completions.create(
        model="gpt-4",  # Model adını belirleyin
        messages=messages,
        max_tokens=800,  # Blog postun uzunluğunu ayarlamak için kullanılır
        n=1,
        stop=None,
        temperature=0.7,  # Cevabın yaratıcılık seviyesi
    )
response = dict(response)
assistant_reply = response['choices'][0].message.content

messages.append({"role" : "assistant", "content" : assistant_reply})

for i in range(13):
    messages.append({"role" : "user", "content" : excel_commands['Commands'][i+1]})
    response = client.chat.completions.create(
        model="gpt-4",  # Model adını belirleyin
        messages=messages,
        max_tokens=4096,  # Blog postun uzunluğunu ayarlamak için kullanılır
        n=1,
        stop=None,
        temperature=0.7,  # Cevabın yaratıcılık seviyesi
    )
    response = dict(response)
    assistant_reply = response['choices'][0].message.content

    messages.append({"role" : "assistant", "content" : assistant_reply})

print(response)