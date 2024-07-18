import os
import random
import asyncio
import pandas as pd
from openai import AsyncOpenAI
from math import isnan

from dotenv import load_dotenv, dotenv_values 
# loading variables from .env file
load_dotenv()

print(os.getenv("OPEN_AI_KEY"))