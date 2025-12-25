import os
import json
from dotenv import load_dotenv
from nlp_to_sql_engine.backend.agents.OrchestratorAgent.OrchestratorAgent import OrchestratorAgent

load_dotenv()


def start_agent(frontend_prompt):
    orchestrator_agent = OrchestratorAgent(
        question=frontend_prompt,
        openai_api_key = os.getenv("gpt_4_o_mini_AZURE_OPENAI_KEY"),
        azure_endpoint = os.getenv("gpt_4_o_mini_AZURE_OPENAI_ENDPOINT"),
        deployment_name = os.getenv("gpt_4_o_mini_AZURE_OPENAI_DEPLOYMENT_NAME"),
        api_version = os.getenv("gpt_4_o_mini_AZURE_OPENAI_API_VERSION"),
        temperature = 0.7
    )
    response_run_query = orchestrator_agent.run()
    return response_run_query
        
    # print("Received prompt from frontend:", frontend_prompt)
    # genrate_query_agent = GenrateQueryAgent(
    #     question=frontend_prompt,
    #     openai_api_key = os.getenv("gpt_4_o_mini_AZURE_OPENAI_KEY"),
    #     azure_endpoint = os.getenv("gpt_4_o_mini_AZURE_OPENAI_ENDPOINT"),
    #     deployment_name = os.getenv("gpt_4_o_mini_AZURE_OPENAI_DEPLOYMENT_NAME"),
    #     api_version = os.getenv("gpt_4_o_mini_AZURE_OPENAI_API_VERSION"),
    #     temperature = 0.7
    # )
    # response_sql_query = genrate_query_agent.run()
    
    # print('<<------STEP 1------>>')
    # print("Generated SQL Query:", response_sql_query)
    # print('<<----------------->>')
    # run_query_agent = RunQueryAgent(
    #     query=response_sql_query,
    #     databricks_host=os.getenv("DATABRICKS_HOST"),
    #     databricks_token=os.getenv("DATABRICKS_TOKEN"),
    #     sql_http_path=os.getenv("DATABRICKS_SQL_HTTP_PATH"),
    #     catalog=os.getenv("CATALOG"),
    #     schema=os.getenv("SCHEMA")
    # )
    # response_run_query = run_query_agent.run()
    # return response_run_query
    # ------------------------------------------------
    