from strands import Agent, tool
from app.tools.strands_agents_tool import read_local_file, write_local_file
from app.models.LLM_model import ModelInstances
from app.prompt.data_analyst_prompt import data_analyst_prompt

@tool
def data_analyst_agent(query: str) -> str:
    """
    分析JSON数据，为每个设备型号生成详细的分析报告

    Args:
        query: 用户的分析JSON数据请求

    Returns:
        分析JSON数据的结果
    """
    results = []
    formatted_query = f"请分析数据信息，根据需要使用本地工具读取或写入数据：{query}"

    try:
        query_agent = Agent(
            system_prompt=data_analyst_prompt,
            model=ModelInstances.LEADER_MODEL,
            tools=[
                read_local_file,
                write_local_file

            ],
        )
        agent_response = query_agent(formatted_query)
        text_response = str(agent_response)

        if len(text_response) > 0:
            results.append(f" {text_response}")
        else:
            results.append(f" 分析完成，已生成分析报告")

    except Exception as e:
        error_msg = f"处理设备 时出错: {str(e)}"
        print(error_msg)
        results.append(error_msg)

# 返回所有设备的处理结果
    return "\n\n".join(results) if results else "处理数据分析时出错: 未能处理任何设备型号"