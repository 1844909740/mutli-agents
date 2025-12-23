import sys
from pathlib import Path
from typing import Optional

from pydantic import BaseModel
from pydantic_settings import BaseSettings
from yaml import safe_load


class MysqlProperties(BaseModel):
    host: str
    port: int
    database: str
    user: str
    password: str


class Setting(BaseSettings):
    port: int
    profile: str
    version: str

    sign_name: Optional[str] = None
    sign_rds: Optional[str] = None
    sign_greptime: Optional[str] = None

    mysql: Optional[MysqlProperties] = None


print(f"Command args: {sys.argv[1:]}")
profile = sys.argv[1]
project_dir = Path(__file__).parents[2]
config_file = f"config_{profile}.yml"
with open(f"{project_dir}/{config_file}", "r") as file:
    data = safe_load(file)
settings = Setting(**data)
print(f"Load project {config_file}")