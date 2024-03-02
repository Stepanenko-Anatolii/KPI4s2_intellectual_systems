import json
import logging
from typing import List

import pydantic_core
import requests

from app.entities.processed_agent_data import ProcessedAgentData
from app.interfaces.store_gateway import StoreGateway


class StoreApiAdapter(StoreGateway):
    def __init__(self, api_base_url):
        self.api_base_url = api_base_url

    def save_data(self, processed_agent_data_batch: List[ProcessedAgentData]):
        """
        Save the processed road data to the Store API.
        Parameters:
            processed_agent_data_batch (dict): Processed road data to be saved.
        Returns:
            bool: True if the data is successfully saved, False otherwise.
        """
        base_url = f"{self.api_base_url}/processed_agent_data/"

        agent_data_json = [agent.model_dump_json() for agent in processed_agent_data_batch]
        json_payload = f"[{','.join(agent_data_json)}]"
        headers = {'Content-Type': 'application/json'}
        result = requests.post(base_url, data=json_payload, headers=headers)

        if result.status_code == 200:
            return True
        
        logging.info(f"Unexpected response from Hub\nPayload: {agent_data_json}\nResult: {result}")
        return False

