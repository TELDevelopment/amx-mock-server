import os
from enum import Enum, auto
from dotenv import load_dotenv

load_dotenv()

gemini_model_id = "gemini-1.5-flash"
claude_model_id = 'anthropic.claude-3-5-sonnet-20240620-v1:0'

class LLMProvider(Enum):
    ANTHROPIC = auto()
    GEMINI =  auto()

class LLMClient:
    def __init__(self, provider):
        self.provider = provider
        self.model_id = ""
        self.client = None
        
        if provider == LLMProvider.GEMINI:
            import google.generativeai as genai
            self.model_id = gemini_model_id
            
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            self.client = genai.GenerativeModel(self.model_id)
            
        
        elif provider == LLMProvider.ANTHROPIC:
            from anthropic import AnthropicBedrock
            
            self.model_id = claude_model_id
                
            aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
            aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
            aws_session_token = os.getenv("AWS_SESSION_TOKEN")
            region_name = os.getenv("AWS_REGION_NAME")

            self.client = AnthropicBedrock(
                aws_access_key=aws_access_key_id,
                aws_secret_key=aws_secret_access_key,
                aws_session_token=aws_session_token,
                aws_region=region_name,
            )
           
        
    def generate_content(self, prompt):
            
        if self.provider == LLMProvider.GEMINI:  
            return self.client.generate_content(prompt).text.strip()
        elif self.provider == LLMProvider.ANTHROPIC:
            message = self.client.messages.create(
            model=self.model_id,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )

            return message.content[0].text.strip()
            
                        
                
        
        
        