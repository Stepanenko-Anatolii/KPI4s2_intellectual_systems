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
    
    # TODO: Implement it
    quality: str = "medium"
    value = abs(agent_data.accelerometer.y)

    if value <= 80:
        quality = "Good"
    elif 80 < value <= 150:
        quality = "Medium"
    else:
        quality = "Poor"

    return ProcessedAgentData(road_state=quality, agent_data=agent_data)