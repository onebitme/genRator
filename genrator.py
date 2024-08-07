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

class Input_Commands():
    def __init__(self,concat,title, category, keywords) -> None:
        self.concat = concat
        self.title = title
        self.category = category
        self.keywords = keywords

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




def commands_list(spreadsheet_id):
    input_csv = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv")
    command = Input_Commands(input_csv['Concat'],input_csv['Title: '],input_csv['Category'],input_csv[' Keywords: '])
    return command


def image_list():
    imagelink_csv = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?gid={tab_id}&format=csv")
    image_categories = imagelink_csv.columns
    image_dict = {}


def main():
    print("Here we go:")
    command = commands_list(spreadsheet_id = os.environ.get("SHEET_ID"))
    client = api_client(os.environ.get("OPEN_AI_KEY"))

    content = []
    image_list = []
    # Still cant believe I am doing like this
    title_toExcel = []
    category_toExcel = []
    keywords_toExcel = []
    
    titles = command.title.tolist()
    categories = command.category.tolist()
    keywords = command.keywords.tolist()
    concats = command.concat.tolist()


    for i in range(len(titles)):
        print("Loop: " + str(i))
        print(titles[i])
        category_toExcel.append(categories[i])
        keywords_toExcel.append(keywords[i])
        bp = asyncio.run(writer(client,concats[i]))
        ### TODO : Take Header 2s and for each, run writer with a short command!!
        print(bp)
        command_sum = "Summarize: " + bp
        summary = asyncio.run(writer(client,command_sum))
        print(summary)
        command = "Create 10 Frequently Asked Questions in same HTML format a blog about: " + summary
        faq = asyncio.run(writer(client,command))
        # print(faq)
        command = "Create a key takeaway table with 10 rows in same HTML format for a blog about: " + summary
        key_table = asyncio.run(writer(client,command))
        text = bp + "\n" + faq + "\n" + key_table
        with open("output" + str(i) + ".html", "w", encoding = 'utf-8') as file: 
            file.write(text)




if __name__ == "__main__":
    main()