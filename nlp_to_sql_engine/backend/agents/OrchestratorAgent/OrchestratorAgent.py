# from langchain.chains import LLMChain
# from langchain.prompts import ChatPromptTemplate
import os
from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from nlp_to_sql_engine.backend.configs.AzureOpenAI.AzureOpenAI import AzureOpenAIConfig
from nlp_to_sql_engine.backend.agents.OrchestratorAgent.prompts import orchestrator_system_message
from nlp_to_sql_engine.backend.agents.Tools.Tools import (
    enhance_user_prompt,
    generate_sql_query,
    execute_sql_query
)

class OrchestratorAgent:
    def __init__(self, question, openai_api_key, azure_endpoint, deployment_name, api_version, temperature=0.7):
        self.question = question
        self.llm_config = AzureOpenAIConfig(
            openai_api_key=openai_api_key,
            azure_endpoint=azure_endpoint,
            deployment_name=deployment_name,
            api_version=api_version,
            temperature=temperature
        )
        self.llm_model = self.llm_config.get_ll_model()
    
    def run(self):
        try:
            print("OrchestratorAgent started...")
            tools = [
                enhance_user_prompt,
                generate_sql_query,
                execute_sql_query,
            ]
            
            agent = create_react_agent(self.llm_model, tools)
            
            result = agent.invoke({
                "messages": [
                    {"role": "system", "content": orchestrator_system_message},
                    {"role": "user", "content": self.question}
                ]
            })
            
            final_response = result["messages"][-1].content
            
            print('--------------------------------------------------------------------------')
            print("Orchestrator Agent Result:", final_response)
            print('--------------------------------------------------------------------------')
            
            return final_response
        except Exception as e:
            raise
            #raise(f"Error in OrchestratorAgent run method: {e}")
        