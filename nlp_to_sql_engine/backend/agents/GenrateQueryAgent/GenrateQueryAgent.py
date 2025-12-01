# from langchain.chains import LLMChain
# from langchain.prompts import ChatPromptTemplate

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
    
from nlp_to_sql_engine.metadata.MetaDataManager import MetaDataManager
from nlp_to_sql_engine.backend.configs.AzureOpenAI.AzureOpenAI import AzureOpenAIConfig
from nlp_to_sql_engine.backend.agents.GenrateQueryAgent.prompts import nlp_to_sql_prompt_system, nlp_to_sql_prompt_human

class GenrateQueryAgent:
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
            # --------------OLD CODE----------------
            # sql_prompt = ChatPromptTemplate.from_messages([
            #     ("system", nlp_to_sql_prompt_system),
            #     ("human", nlp_to_sql_prompt_human)
            # ])
            
            # sql_chain = LLMChain(llm=self.llm_model, prompt=sql_prompt)
            # sql_query = sql_chain.run({
            #     "catalog": catalog,
            #     "schema": schema,
            #     "metadata": metadata_str,
            #     "question": question
            # })
            # ---------------------------------
            
            sql_prompt = ChatPromptTemplate.from_messages([
                ("system", nlp_to_sql_prompt_system),
                ("human", nlp_to_sql_prompt_human),
                ])
            sql_chain = sql_prompt | self.llm_model | StrOutputParser()
            inputs = {
                "catalog": "ecom",
                "schema": "brazilian_ecom_olist",
                "metadata": self.unity_catalog_metadata,
                "question": self.question,
                }
            sql_query = sql_chain.invoke(inputs)
            return sql_query
        except Exception as e:
            raise(f"Error in GenrateQueryAgent run method: {e}")
        