import logging
import time
from app.db.mysql.live_connection_log import TbLiveConnectionLog
from app.db.mysql.live_connection_statistic_rate_5m import TbLiveConnectionStatisticsRate
from app.db.mysql.live_connection_statistics_speed_5m import TbLiveConnectionStatisticsSpeed
from fastapi import APIRouter, FastAPI
from typing import Dict, List

app = APIRouter()


@app.get("/api/get-live-connection-logs")
async def get_live_connection_log_list(
        device_model: str,
        device_id: str,
        env: str,
        start_time: int,
        end_time: str
):
    live_connection_log: List[Dict] = TbLiveConnectionLog(
        device_model=device_model,
        device_id=device_id,
        env=env,
        start_time=start_time,
        end_time=end_time
    )

    return live_connection_log


@app.get("/api/get-live-connection-statistics-rates")
async def get_live_connection_statistics_rates(
        device_model: str,
        device_id: str,
        env: str,
        start_time: int,
        end_time: str
):
    live_connection_statistics_rates: List[Dict] = TbLiveConnectionStatisticsRate(
        device_model=device_model,
        device_id=device_id,
        env=env,
        start_time=start_time,
        end_time=end_time
    )

    return live_connection_statistics_rates


@app.get("/api/get-live-connection-statistics-speeds")
async def get_live_connection_statistics_speeds(
        device_model: str,
        device_id: str,
        env: str,
        start_time: int,
        end_time: str
):
    live_connection_statistics_speeds: List[Dict] = TbLiveConnectionStatisticsSpeed(
        device_model=device_model,
        device_id=device_id,
        env=env,
        start_time=start_time,
        end_time=end_time
    )

    return live_connection_statistics_speeds


@app.get("/api/strands-agents/")
async def strands_agents():
    from app.agents.lead_agent import lead_agent
    from app.servics.get_date import get_current_date

    device_models = [
        "",
    ]

    current_date = get_current_date()

    for device_model in device_models:
        logging.info(f"Processing  device model: {device_model} with Strands Agents...")

        response = await lead_agent.invoke_async(
            f"current report type is , current device model is {device_model}"
            f"current date is {current_date}"
        )

        logging.info(f"Strands Agents Response for {device_model}: {response}")



