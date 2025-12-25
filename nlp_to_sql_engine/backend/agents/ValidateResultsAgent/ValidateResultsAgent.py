from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
    
from nlp_to_sql_engine.metadata.MetaDataManager import MetaDataManager
from nlp_to_sql_engine.backend.configs.AzureOpenAI.AzureOpenAI import AzureOpenAIConfig
from nlp_to_sql_engine.backend.agents.ValidateResultsAgent.prompts import verify_results_prompt_system, verify_results_prompt_human

class ValidateResultsAgent:
    def __init__(self, 
                 question,
                 enhanced_question,
                 sql_query,
                 query_results,
                 openai_api_key, 
                 azure_endpoint, 
                 deployment_name, 
                 api_version, 
                 temperature=0.7):
        
        self.original_question = question
        self.enhanced_question = enhanced_question
        self.sql_query = sql_query,
        self.query_results = query_results
        
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
            print("ValidateResultsAgent started...")
            validate_prompt = ChatPromptTemplate.from_messages([
                ("system", verify_results_prompt_system),
                ("human", verify_results_prompt_human),
                ])
            validate_chain = validate_prompt | self.llm_model | StrOutputParser()
            inputs = {
                "metadata": self.unity_catalog_metadata,
                "catalog": "ecom",
                "schema": "brazilian_ecom_olist",
                "original_question": self.original_question,
                "enhanced_question": self.enhanced_question,
                "sql_query": self.sql_query,
                "query_results": self.query_results
                }
            validate_query = validate_chain.invoke(inputs)
            return validate_query
        except Exception as e:
            raise
            #raise(f"Error in ValidateResultsAgent run method: {e}")