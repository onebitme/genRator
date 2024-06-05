import os
import random
import asyncio
import pandas as pd
import datetime
from openai import AsyncOpenAI
from math import isnan

#date = datetime.datetime.now()
#folder_suffix = "output" + date.strftime('_%d%b%g_%H%M%S')

#current_directory = os.getcwd()
#output_directory = os.path.join(current_directory, folder_suffix)

# os.makedirs(output_directory)

#Read google sheets,
#TODO: hide sheet id

spreadsheet_id = os.environ.get("SHEET_ID")
tab_id = os.environ.get("TAB_ID")
input_csv = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv")

imagelink_csv = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?gid={tab_id}&format=csv")


concat = input_csv['Concat']
title = input_csv['Title']
category = input_csv['Category']
keywords = input_csv['Keywords']

imagelink_csv = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?gid={tab_id}&format=csv")
image_categories = imagelink_csv.columns

image_dict = {}

for i in range(len(image_categories)):
    image_dict[image_categories[i]] =  [x for x in imagelink_csv[image_categories[i]] if str(x) !="nan"]

def image_match(image_dict, category):
    try:
        list = image_dict[category]
        image_link = random.choice(list)   
        return image_link
    except:
        print("Category - image database mismatch")
        image_link = []
        return image_link

## All lists for writing the final sheet

def write_to_sheet(title, content, category, image_list, keywords):
    dict_write = {
                    'Post Title': title,
                    'Post Content': content,
                    'Categories': category,
                    'Image': image_list,
                    'Keywords': keywords
                }
    #try: 
    towrite= pd.DataFrame.from_dict(dict_write, orient='index')
    towrite = towrite.transpose()
    towrite.to_excel('out.xlsx', index=False)
    #except:
    #    print("Delete 'out.csv' and try again")


# GPT Client and Main Function

client = AsyncOpenAI(
    # This is the default and can be omitted
    api_key = os.environ.get("OPEN_AI_KEY")
)

async def main(title,command) -> None:
    chat_completion = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": command
            }
        ],
        model="gpt-4o-2024-05-13",
        max_tokens=1600
    )
    gpt_return = dict(chat_completion)

    multiline_string = gpt_return['choices'][0].message.content
    
    num_of_lines = multiline_string.count("\n") + 1
    print("number of lines in string : " + str(num_of_lines))
    
    #Split the str at newline and use list slicing to drop 1st line
    str_in_list = multiline_string.split("\n")[1:]
    
    #after removal, change list to string
    new_str1 = ""
    for item in str_in_list:
        new_str1 += item
        new_str1 += '\n'
    
    num_of_lines = new_str1.count("\n") + 1
    #Split the str at newline and use list slicing to drop last line
    str_in_list = new_str1.split("\n")[:num_of_lines-1]
    
    #after removal, change list to string
    new_str2 = ""
    for item in str_in_list:
        new_str2 += item
        new_str2 += '\n'
 
    return new_str2


#Pre Write, Create content

content = []
image_list = []
# Still cant believe I am doing like this
title_toExcel = []
category_toExcel = []
keywords_toExcel = []

for i in range(len(concat)):
    title_toExcel.append(title[i])
    category_toExcel.append(category[i])
    keywords_toExcel.append(keywords[i])
    content.append(asyncio.run(main(title[i],concat[i])))
    image_list.append(image_match(image_dict,category[i]))



write_to_sheet(title_toExcel,content,category_toExcel,image_list, keywords_toExcel)

