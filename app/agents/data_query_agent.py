from strands import tool, Agent
from app.models.LLM_model import ModelInstances
from app.tools.strands_agents_tool import (
    get_and_upload_app_rates,
    get_and_upload_firmware_rates,
    get_and_upload_firmware_speeds,
    get_and_upload_app_speeds
)
from app.servics.get_date import get_current_date
from datetime import datetime, timedelta, timezone
from app.prompt.data_query_prompt import data_query_prompt
start_time = int((datetime.now() - timedelta(days=7)).timestamp() * 1e9)
end_time = int(datetime.now(timezone.utc).timestamp() * 1e9)
env = "prod"

params = {
    "start_time": start_time,
    "end_time": end_time,
    "env": env,
    "date": get_current_date(),
}

prompt = data_query_prompt.format(**params)


@tool
def data_query_agent(query: str) -> str:
    """
    获取数据，具备本地数据读写能力

    Args:
        query: 用户的检查获取数据请求

    Returns:
        获取数据的结果
    """
    # 格式化查询，提供清晰的指令
    formatted_query = f"请处理以下检查获取数据，根据需要使用本地工具读取或写入数据: {query}"

    try:
        print("路由到获取数据专家")
        query_agent = Agent(
            system_prompt=data_query_prompt,
            model=ModelInstances.LEADER_MODEL,
            tools=[
                get_and_upload_app_rates,
                get_and_upload_firmware_rates,
                get_and_upload_firmware_speeds,
                get_and_upload_app_speeds
            ],
        )
        agent_response = query_agent(formatted_query)
        text_response = str(agent_response)

        if len(text_response) > 0:
            return text_response

        return "抱歉，无法处理您的获取数据请求。请尝试重新表述或提供更具体的需求详情。"
    except Exception as e:
        # 返回具体的错误信息
        return f"处理获取数据时出错: {str(e)}"