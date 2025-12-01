import os
import json
from dotenv import load_dotenv
from nlp_to_sql_engine.backend.agents.GenrateQueryAgent.GenrateQueryAgent import GenrateQueryAgent


load_dotenv()

def start_agent(frontend_prompt):
    print("Received prompt from frontend:", frontend_prompt)
    genrate_query_agent = GenrateQueryAgent(
        question=frontend_prompt,
        openai_api_key = os.getenv("gpt_4_o_mini_AZURE_OPENAI_KEY"),
        azure_endpoint = os.getenv("gpt_4_o_mini_AZURE_OPENAI_ENDPOINT"),
        deployment_name = os.getenv("gpt_4_o_mini_AZURE_OPENAI_DEPLOYMENT_NAME"),
        api_version = os.getenv("gpt_4_o_mini_AZURE_OPENAI_API_VERSION"),
        temperature = 0.7
    )
    response = genrate_query_agent.run()
    return response