import os
import json
from dotenv import load_dotenv
from Configs import AzureOpenAIConfig
from Configs import DatabricksConfig

load_dotenv()

def start_agent(frontend_prompt):
    print("Received prompt from frontend:", frontend_prompt)
    return f"Processed your prompt: '{frontend_prompt}'. (Backend integration pending)"