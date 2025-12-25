import os
import json
from dotenv import load_dotenv
from langchain_core.tools import tool
from nlp_to_sql_engine.backend.agents.RunQueryAgent.RunQueryAgent import RunQueryAgent
from nlp_to_sql_engine.backend.agents.GenrateQueryAgent.GenrateQueryAgent import GenrateQueryAgent
from nlp_to_sql_engine.backend.agents.EnhancedQuestionAgent.EnhancedQuestionAgent import EnhancedQuestionAgent
from nlp_to_sql_engine.backend.agents.ValidateSQLQueryAgent.ValidateSQLQueryAgent import ValidateSQLQueryAgent
from nlp_to_sql_engine.backend.agents.ValidateResultsAgent.ValidateResultsAgent import ValidateResultsAgent

load_dotenv()


@tool
def enhance_user_prompt(original_prompt: str) -> str:
    """
    Enhance vague user questions to be more specific.
    
    Use this when the user's question is ambiguous or lacks details.
    
    Args:
        original_prompt: User's original question
        
    Returns:
        Enhanced question with more context
    """
    print("enhance_user_prompt started...")
    agent = EnhancedQuestionAgent(
        question=original_prompt,
        openai_api_key=os.getenv("gpt_4_o_mini_AZURE_OPENAI_KEY"),
        azure_endpoint=os.getenv("gpt_4_o_mini_AZURE_OPENAI_ENDPOINT"),
        deployment_name=os.getenv("gpt_4_o_mini_AZURE_OPENAI_DEPLOYMENT_NAME"),
        api_version=os.getenv("gpt_4_o_mini_AZURE_OPENAI_API_VERSION"),
        temperature=0.7
    )
    enhance_user_prompted_question = agent.run()
    print("Enhanced Question:", enhance_user_prompted_question)
    return enhance_user_prompted_question

@tool
def generate_sql_query(original_prompt: str, enhanced_prompt: str = None) -> str:
    """
    Generate a SQL query from natural language question.
    
    Use this tool when the user asks a question about data.
    This creates the SQL query needed to retrieve the information.
    
    Args:
        original_prompt: The user's question in natural language
        enhanced_prompt: Enhanced version of question (if enhancement was used)
        
    Returns:
        A valid SQL query string ready to execute
    """
    print("generate_sql_query started...")
    # Use your existing GenrateQueryAgent class
    question_context = enhanced_prompt if enhanced_prompt else original_prompt
    
    agent = GenrateQueryAgent(
        question=question_context,
        openai_api_key=os.getenv("gpt_4_o_mini_AZURE_OPENAI_KEY"),
        azure_endpoint=os.getenv("gpt_4_o_mini_AZURE_OPENAI_ENDPOINT"),
        deployment_name=os.getenv("gpt_4_o_mini_AZURE_OPENAI_DEPLOYMENT_NAME"),
        api_version=os.getenv("gpt_4_o_mini_AZURE_OPENAI_API_VERSION"),
        temperature=0.7
    )
    return agent.run()


# @tool
# def validate_sql_query(sql_query: str, original_prompt: str, enhanced_prompt: str = None) -> dict:
#     """
#     Validate SQL query for syntax and logic errors.
    
#     Use this before executing SQL to catch potential issues.
    
#     Args:
#         sql_query: The SQL query to validate
#         original_prompt: Original user question for context
#         enhanced_prompt: Enhanced version of question (if enhancement was used)
        
#     Returns:
#         Dictionary with validation results
#     """
#     print("validate_sql_query started...")
#     question_context = enhanced_prompt if enhanced_prompt else original_prompt
    
#     agent = ValidateSQLQueryAgent(
#         question=original_prompt,
#         enhanced_question=question_context,
#         sql_query=sql_query,
#         openai_api_key=os.getenv("gpt_4_o_mini_AZURE_OPENAI_KEY"),
#         azure_endpoint=os.getenv("gpt_4_o_mini_AZURE_OPENAI_ENDPOINT"),
#         deployment_name=os.getenv("gpt_4_o_mini_AZURE_OPENAI_DEPLOYMENT_NAME"),
#         api_version=os.getenv("gpt_4_o_mini_AZURE_OPENAI_API_VERSION"),
#         temperature=0.7
#     )
#     return agent.run()  


@tool
def execute_sql_query(sql_query: str) -> dict:
    """
    Execute a SQL query on Databricks and return results.
    
    Use this tool after generating SQL to get the actual data.
    
    Args:
        sql_query: The SQL query to execute
        
    Returns:
        Dictionary containing query results with data and metadata
    """
    print("execute_sql_query started...")
    # Use your existing RunQueryAgent class
    agent = RunQueryAgent(
        query=sql_query,
        databricks_host=os.getenv("DATABRICKS_HOST"),
        databricks_token=os.getenv("DATABRICKS_TOKEN"),
        sql_http_path=os.getenv("DATABRICKS_SQL_HTTP_PATH"),
        catalog=os.getenv("CATALOG"),
        schema=os.getenv("SCHEMA")
    )
    return agent.run()


# @tool
# def verify_query_results(results: dict, sql_query: str, original_prompt: str, enhanced_prompt: str = None) -> dict:
#     """
#     Verify if query results correctly answer the user's question.
    
#     Use this after executing SQL to ensure results are correct.
    
#     Args:
#         results: Query execution results
#         sql_query: The SQL query that was executed
#         original_prompt: Original user question
#         enhanced_prompt: Enhanced version of question (if enhancement was used)
        
#     Returns:
#         Dictionary with verification status and explanation
#     """
#     print("verify_query_results started...")
#     question_context = enhanced_prompt if enhanced_prompt else original_prompt
    
#     agent = ValidateResultsAgent(
#         question=original_prompt,
#         enhanced_question=question_context,
#         sql_query=sql_query,
#         query_results=results,
#         openai_api_key=os.getenv("gpt_4_o_mini_AZURE_OPENAI_KEY"),
#         azure_endpoint=os.getenv("gpt_4_o_mini_AZURE_OPENAI_ENDPOINT"),
#         deployment_name=os.getenv("gpt_4_o_mini_AZURE_OPENAI_DEPLOYMENT_NAME"),
#         api_version=os.getenv("gpt_4_o_mini_AZURE_OPENAI_API_VERSION"),
#         temperature=0.7
#     )
#     return agent.run()