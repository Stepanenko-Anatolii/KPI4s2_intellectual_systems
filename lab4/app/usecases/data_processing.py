from app.entities.agent_data import AgentData
from app.entities.processed_agent_data import ProcessedAgentData

import logging

def process_agent_data(
    agent_data: AgentData,
) -> ProcessedAgentData:
    """
    Process agent data and classify the state of the road surface.
    Parameters:
        agent_data (AgentData): Agent data that containing accelerometer, GPS, and timestamp.
    Returns:
        processed_data_batch (ProcessedAgentData): Processed data containing the classified state of the road surface and agent data.
    """
    quality: str = "medium"
    value = abs(agent_data.accelerometer.y)
    timestamp = agent_data.timestamp
    user_id = 2

    if value <= 75:
        quality = "Good"
    elif 75 < value <= 160:
        quality = "Average"
    else:
        quality = "Bad"

    return ProcessedAgentData(road_state=quality, agent_data=agent_data, user_id=user_id, timestamp=timestamp)
