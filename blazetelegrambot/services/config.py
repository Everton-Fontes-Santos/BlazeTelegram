from pydantic_settings import BaseSettings, SettingsConfigDict

class APIConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    PORT:int
    
class TelegramConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    SESSION_NAME:str
    BOT_TOKEN:str
    API_ID:str
    API_HASH:str
    WHITE_PAID_GROUP:int
    COLOR_PAID_GROUP:int
    WHITE_FREE_GROUP:str
    COLOR_FREE_GROUP:str
    PORT:int