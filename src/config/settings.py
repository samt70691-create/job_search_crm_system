from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    gemini_api_key: str = os.getenv('GEMINI_API_KEY', '')
    email_sender: str = os.getenv('EMAIL_SENDER', '')
    email_recipient: str = os.getenv('EMAIL_RECIPIENT', '')


settings = Settings()
