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


class ThirdPartyProperties(BaseModel):
    deepseek_api_key: Optional[str] = ""
    deepseek_base_url: Optional[str] = ""
    deepseek_model_id: Optional[str] = ""

    bedrock_region_name: str
    bedrock_pro_model_id: str
    bedrock_aws_access_key_id: str
    bedrock_aws_secret_access_key: str


class Setting(BaseSettings):
    port: int
    profile: str
    version: str

    app_id: Optional[str] = None
    app_key: Optional[str] = None

    third_party: Optional[ThirdPartyProperties] = None
    mysql: Optional[MysqlProperties] = None

    sign_name: Optional[str] = None
    third_party_name: Optional[str] = None

    feature_code: str = "-intelligence"



    prompt: dict = {
        "orchestrator": {
            "prompt_code": ""
        },
        "data_query_agent": {
            "prompt_code": ""
        },
        "data_analyst_agent": {
            "prompt_code": ""
        },
        "web_engineer_agent": {
            "prompt_code": ""
        },
        "html_report_review_agent": {
            "prompt_code": ""
        },
        "lead_agent": {
            "prompt_code": ""
        },
    }

    description: dict = {
        "supervisor_agent": "你是一个数据分析主管, 你能够协调Team Agent完成客户P2P分析需求并生成报告.",
        "lead_agent": "你是P2P报告团队的负责人, 你需要协调多名专家回答用户问题或完成任务.",
        "data_query_agent": "你是一名数据获取工程师，你擅长根据用户提供的设备型号、日期等信息，从数据库或统计服务中获取连接率、连接速度、版本发布等原始数据，并保存到指定的s3路径中",
        "data_analyst_agent": "你是一个数据分析专家, 你能够识别异常并提供深度见解和可能的原因分析.",
        "web_engineer_agent": "你是一位Web开发工程师, 你需要将给定的内容转换为HTML文档.",
        "html_report_review_agent": "你是一位HTML报告审核专家, 你需要审核给定的HTML内容, 并给出审核意见.",
    }


# 获取命令行参数
print(f"Command args: {sys.argv[1:]}")
profile = sys.argv[1]
# 获取项目根目录
project_dir = Path(__file__).parents[2]
# 读取配置文件
config_file = f"config_{profile}.yml"
with open(f"{project_dir}/{config_file}", "r") as file:
    data = safe_load(file)
# 将数据设置到 Setting 类属性
settings = Setting(**data)
print(f"Load project {config_file}")
