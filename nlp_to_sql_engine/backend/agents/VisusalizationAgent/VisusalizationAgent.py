# from langchain.chains import LLMChain
# from langchain.prompts import ChatPromptTemplate

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
    
from nlp_to_sql_engine.metadata.MetaDataManager import MetaDataManager
from nlp_to_sql_engine.backend.configs.AzureOpenAI.AzureOpenAI import AzureOpenAIConfig
from nlp_to_sql_engine.backend.agents.VisusalizationAgent.prompts import system_prompt, human_prompt

class VisusalizationAgent:
    def __init__(self, 
                 question,
                 sql_query,
                 df_preview, 
                 openai_api_key, azure_endpoint, deployment_name, api_version, temperature=0.7):
        
        self.question = question
        self.sql_query = sql_query
        self.df_preview = df_preview
        self.llm_config = AzureOpenAIConfig(
            openai_api_key=openai_api_key,
            azure_endpoint=azure_endpoint,
            deployment_name=deployment_name,
            api_version=api_version,
            temperature=temperature
        )
        self.llm_model = self.llm_config.get_ll_model()
        self.metadata_manager = MetaDataManager()
        self.unity_catalog_metadata = self.metadata_manager.get_metadata()
    
    def run(self):
        try:
            vis_prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                ("human", human_prompt),
                ])
            vis_chain = vis_prompt | self.llm_model | StrOutputParser()
            inputs = {
                "question": self.question,
                "sql_query": self.sql_query,
                "df_preview": self.df_preview,
                "metadata": self.unity_catalog_metadata,
                }
            vis_code = vis_chain.invoke(inputs)
            return vis_code
        except Exception as e:
            raise(f"Error in VisusalizationAgent run method: {e}")
        