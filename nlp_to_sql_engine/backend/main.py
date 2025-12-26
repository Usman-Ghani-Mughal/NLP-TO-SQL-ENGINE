import os
import json
from dotenv import load_dotenv
from nlp_to_sql_engine.backend.agents.GenrateQueryAgent.GenrateQueryAgent import GenrateQueryAgent
from nlp_to_sql_engine.backend.agents.RunQueryAgent.RunQueryAgent import RunQueryAgent
from nlp_to_sql_engine.backend.agents.VisusalizationAgent.VisusalizationAgent import VisusalizationAgent
from nlp_to_sql_engine.backend.agents.EnhancedQuestionAgent.EnhancedQuestionAgent import EnhancedQuestionAgent


load_dotenv()

def start_agent(frontend_prompt):
    
    enhanced_question_agent = EnhancedQuestionAgent(
        question=frontend_prompt,
        openai_api_key = os.getenv("gpt_4_o_mini_AZURE_OPENAI_KEY"),
        azure_endpoint = os.getenv("gpt_4_o_mini_AZURE_OPENAI_ENDPOINT"),
        deployment_name = os.getenv("gpt_4_o_mini_AZURE_OPENAI_DEPLOYMENT_NAME"),
        api_version = os.getenv("gpt_4_o_mini_AZURE_OPENAI_API_VERSION"),
        temperature = 0.7
    )
    enhanced_question = enhanced_question_agent.run()
    print("Received prompt from frontend:", frontend_prompt)
    print("Enhanced question:", enhanced_question)
    
    genrate_query_agent = GenrateQueryAgent(
        question=enhanced_question,
        openai_api_key = os.getenv("gpt_4_o_mini_AZURE_OPENAI_KEY"),
        azure_endpoint = os.getenv("gpt_4_o_mini_AZURE_OPENAI_ENDPOINT"),
        deployment_name = os.getenv("gpt_4_o_mini_AZURE_OPENAI_DEPLOYMENT_NAME"),
        api_version = os.getenv("gpt_4_o_mini_AZURE_OPENAI_API_VERSION"),
        temperature = 0.7
    )
    response_sql_query = genrate_query_agent.run()
    
    run_query_agent = RunQueryAgent(
        query=response_sql_query,
        databricks_host=os.getenv("DATABRICKS_HOST"),
        databricks_token=os.getenv("DATABRICKS_TOKEN"),
        sql_http_path=os.getenv("DATABRICKS_SQL_HTTP_PATH"),
        catalog=os.getenv("CATALOG"),
        schema=os.getenv("SCHEMA")
    )
    response_run_query = run_query_agent.run()
    
    viz_code_agent = VisusalizationAgent(
        question=enhanced_question,
        sql_query=response_run_query['query'],
        df_preview=response_run_query['response'],
        openai_api_key = os.getenv("gpt_4_o_mini_AZURE_OPENAI_KEY"),
        azure_endpoint = os.getenv("gpt_4_o_mini_AZURE_OPENAI_ENDPOINT"),
        deployment_name = os.getenv("gpt_4_o_mini_AZURE_OPENAI_DEPLOYMENT_NAME"),
        api_version = os.getenv("gpt_4_o_mini_AZURE_OPENAI_API_VERSION"),
        temperature = 0.7
    )
    viz_code = viz_code_agent.run()
    
    response_run_query['visualization_code'] = viz_code
    return response_run_query