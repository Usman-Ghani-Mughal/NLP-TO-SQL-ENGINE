from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
    
from nlp_to_sql_engine.metadata.MetaDataManager import MetaDataManager
from nlp_to_sql_engine.backend.configs.AzureOpenAI.AzureOpenAI import AzureOpenAIConfig
from nlp_to_sql_engine.backend.agents.EnhancedQuestionAgent.prompts import enhance_prompt_system, enhance_prompt_human

class EnhancedQuestionAgent:
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
        self.metadata_manager = MetaDataManager()
        self.unity_catalog_metadata = self.metadata_manager.get_metadata()
    
    def run(self):
        try:
            print("EnhancedQuestionAgent started...")
            enhance_prompt = ChatPromptTemplate.from_messages([
                ("system", enhance_prompt_system),
                ("human", enhance_prompt_human),
                ])
            enhance_chain = enhance_prompt | self.llm_model | StrOutputParser()
            inputs = {
                "catalog": "ecom",
                "schema": "brazilian_ecom_olist",
                "metadata": self.unity_catalog_metadata,
                "original_prompt": self.question,
                }
            enhance_question = enhance_chain.invoke(inputs)
            return enhance_question
        except Exception as e:
            raise
            #raise(f"Error in EnhancedQuestionAgent run method: {e}")