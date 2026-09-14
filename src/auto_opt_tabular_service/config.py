from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
	# app settings
	APP_NAME: str = "auto-opt-tabular-service"
	ENVIRONMENT: str = "development"
	DEBUG: bool = True
	API_V1_STR: str = "/api/v1"
	PORT: int = 8000
	# adding service name variable
	service_name: str = "auto-opt-tabular-service"
	# creating model_config
	model_config = SettingsConfigDict(
		env_file=".env",
		env_file_encoding="utf-8",
		extra="ignore"
	)

@lru_cache
def get_settings() -> Settings:
	return Settings()
