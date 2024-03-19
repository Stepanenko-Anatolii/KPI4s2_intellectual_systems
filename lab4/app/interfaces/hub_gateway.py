from abc import ABC, abstractmethod
from app.entities.processed_agent_data import ProcessedAgentData
import psycopg2


class HubGateway(ABC):
    """
    Abstract class representing the Store Gateway interface.
    All store gateway adapters must implement these methods.
    """

    @abstractmethod
    def save_data(self, processed_data: ProcessedAgentData) -> bool:
        """
        Method to save the processed agent data in the database.
        Parameters:
            processed_data (ProcessedAgentData): The processed agent data to be saved.
        Returns:
            bool: True if the data is successfully saved, False otherwise.
        """
        pass

class HubGatewayVersion1(HubGateway):
    def __init__(self, db_config):
        self.db_config = db_config

    def save_data(self, processed_data: ProcessedAgentData) -> bool:
        try:
            connection = psycopg2.connect(**self.db_config) #connect to db
            cursor = connection.cursor()
            insert_query = 'INSERT INTO processed_agent_data (road_state) VALUES (%s)'
            cursor.execute(insert_query, (processed_data.road_state,))
            connection.commit()
            cursor.close()
            connection.close()

            return True
        except Exception as e:
            print(f"save_data error: {e}")
            return False
