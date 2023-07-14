from pydantic_settings import BaseSettings, SettingsConfigDict
import json

class Settings(BaseSettings):
    twitch_bot_username: str
    twitch_bot_client_id: str
    twitch_channel_name: str
    openai_api_key: str

    vote_delay: int = 20
    backend_port: int = 9511

    model_config = SettingsConfigDict(env_file='.env')

    def load_config(self):
        with open('config.json') as config_file:
            config = json.load(config_file)
        self.twitch_bot_username = config['twitch']['clientkey']
        self.twitch_bot_client_id = config['twitch']['clientkey']
        self.twitch_channel_name = config['twitch']['hostchannel']
        self.openai_api_key = config['openai']['api_key']

config = Settings()
config.load_config()
