from strands import Agent, tool
from app.tools.strands_agents_tool import read_local_file, get_local_file_metadata, write_local_file_html
from app.models.LLM_model import ModelInstances
from app.prompt.web_engieer_prompt import web_engineer_prompt



@tool
def web_engineer_agent(query: str) -> str:
    """
    将json转换为html报告，具备本地数据读写能力

    Args:
        query: 用户的将json转换为html报告请求

    Returns:
        将json转换为html报告的结果
    """
    # 格式化查询，提供清晰的指令
    formatted_query = f"请处理以下将json转换为html报告请求，根据需要使用本地工具读取或写入数据: {query}"

    try:
        print("路由到将json转换为html报告专家")
        query_agent = Agent(
            system_prompt=web_engineer_prompt,
            model=ModelInstances.LEADER_MODEL,
            tools=[
                read_local_file,
                get_local_file_metadata,
                write_local_file_html
            ],
        )
        agent_response = query_agent(formatted_query)
        text_response = str(agent_response)

        if len(text_response) > 0:
            return text_response

        return "抱歉，无法处理您的将json转换为html请求。请尝试重新表述或提供更具体的需求详情。"
    except Exception as e:
        # 返回具体的错误信息
        return f"处理将json转换为html报告时出错: {str(e)}"