from pydantic_settings import BaseSettings, SettingsConfigDict



class TelegramConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    SESSION_NAME:str
    BOT_TOKEN:str
    API_ID:str
    API_HASH:str