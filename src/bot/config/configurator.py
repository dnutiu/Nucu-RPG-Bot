import functools
import os

import yaml
from pathlib import Path
from typing import Type, Tuple, Any, Dict

from pydantic import Field, BaseModel
from pydantic.fields import FieldInfo
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource

config_file_default_location = "config.yaml"


class YamlConfigSettingsSource(PydanticBaseSettingsSource):
    """
    A simple settings source class that loads variables from a YAML file
    at the project's root.

    Here we happen to choose to use the `env_file_encoding` from Config
    when reading `config.yaml`
    """

    @functools.lru_cache
    def read_file_content(self):
        encoding = self.config.get("env_file_encoding")
        return yaml.safe_load(
            Path(
                os.getenv("NUCUBOT_CONFIG", default=config_file_default_location)
            ).read_text(encoding)
        )

    def get_field_value(
        self, field: FieldInfo, field_name: str
    ) -> Tuple[Any, str, bool]:
        file_content_json = self.read_file_content()
        field_value = file_content_json.get(field_name)
        return field_value, field_name, False

    def prepare_field_value(
        self, field_name: str, field: FieldInfo, value: Any, value_is_complex: bool
    ) -> Any:
        return value

    def __call__(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {}

        for field_name, field in self.settings_cls.model_fields.items():
            field_value, field_key, value_is_complex = self.get_field_value(
                field, field_name
            )
            field_value = self.prepare_field_value(
                field_name, field, field_value, value_is_complex
            )
            if field_value is not None:
                d[field_key] = field_value

        return d


class DiscordSettings(BaseModel):
    """
    Holds all the settings needed to configure the bot for Discord usage.
    """

    game_name: str = Field(default="RPG")
    token: str = Field()
    command_prefix: str = Field(default=".")
    test_guilds: list[int] = Field(default=[])


class Settings(BaseSettings):
    """
    Settings class for the bot
    """

    discord: DiscordSettings

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            YamlConfigSettingsSource(settings_cls),
            env_settings,
            file_secret_settings,
        )
