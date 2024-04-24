import toml

from app.config import BotConfig, Config, DbConfig


def load_config() -> Config:
    config_data = toml.load('config\config.template.toml')
    bot_config_data = config_data.get('bot', {})
    db_config_data = config_data.get('database', {})
    
    bot_config = BotConfig(token=bot_config_data.get('token', ''), admin_id=bot_config_data.get('admin_id', ''), token_yookassa=bot_config_data.get('token_yookassa', ''), channel_id=bot_config_data.get('channel_id', ''), channel_url=bot_config_data.get('channel_url', ''))
    db_config = DbConfig(type=db_config_data.get('type', ''), path=db_config_data.get('path', ''), echo=db_config_data.get('echo', False))

    return Config(bot=bot_config, db=db_config)


settings = load_config()