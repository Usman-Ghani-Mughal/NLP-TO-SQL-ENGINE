from ..BaseConfig.BaseConfig import BaseConfig
from langchain_openai import AzureChatOpenAI


class AzureOpenAIConfig(BaseConfig):
    def __init__(self, openai_api_key, azure_endpoint, deployment_name, api_version, temperature=0.7):
        self.api_type = "azure"
        self.openai_api_key = openai_api_key
        self.azure_endpoint = azure_endpoint
        self.deployment_name = deployment_name
        self.api_version = api_version
        self.temperature = temperature
        super().__init__()
    
    def validate(self) -> None:
        """Validate Azure OpenAI configuration."""
        print("Validating Azure OpenAI configuration...")
        
        if not self.openai_api_key:
            raise ValueError("API key is required")
        if not self.azure_endpoint:
            raise ValueError("Endpoint is required")
        if not self.deployment_name:
            raise ValueError("Deployment is required")
        if not self.api_version:
            raise ValueError("API Version is required")
        if not self.temperature:
            raise ValueError("Temperature is required")
        
        print("Azure OpenAI configuration is valid.")
    
    def get_ll_model(self):
        """Get the Azure OpenAI model """
        try:
            llm_model = AzureChatOpenAI(
                openai_api_key=self.openai_api_key,
                azure_endpoint=self.azure_endpoint,
                deployment_name=self.deployment_name,
                api_version=self.api_version,
                temperature=self.temperature)
            return llm_model
        except Exception as e:
            print(f"\033Got error file getting llm model: {e} \033[0m")
            return None
