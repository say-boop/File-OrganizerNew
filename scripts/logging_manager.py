import logging
import logging.config
import yaml
from pathlib import Path

class LoggingManager:
  _initialized = False
  _config = None
  
  @classmethod
  def initialize(cls, config_file="logging_config.yml"):
    if cls._initialized:
      return
    
    config_path = Path(__file__).parent.parent / "config" / config_file
    if config_path.exists():
      with open(config_path, "r", encoding="utf-8") as f:
        cls._config = yaml.safe_load(f)
      logging.config.dictConfig(cls._config)
      cls._initialized = True
    else:
      logging.basicConfig(level=logging.INFO)
      cls._initialized = True
  
  @classmethod
  def get_logger(cls, name):
    cls.initialize()
    return logging.getLogger(name)