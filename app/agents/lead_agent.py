import sys
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_DIR))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from strands import Agent
from app.agents.data_query_agent import data_query_agent
from app.agents.data_analyst_agent import data_analyst_agent
from app.agents.web_engineer_agent import web_engineer_agent
from app.agents.summary_html_agent import summary_html_agent
from app.agents.html_report_review_agent import html_report_agent
from app.agents.zip_file_agent import zip_file_agent
from app.models.LLM_model import ModelInstances
from app.prompt.lead_prompt import lead_prompt
from app.agents.send_email_agent import send_email_agent


lead_agent = Agent(
            system_prompt=lead_prompt,
            model=ModelInstances.LEADER_MODEL,
            tools=[
                data_query_agent,
                data_analyst_agent,
                web_engineer_agent,
                summary_html_agent,
                html_report_agent,
                zip_file_agent,
                send_email_agent
            ],
        )