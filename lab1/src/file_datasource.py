from csv import DictReader
from datetime import datetime
from domain.aggregated_data import AggregatedData
from enum import Enum
from marshmallow import Schema
from schema.accelerometer_schema import AccelerometerSchema
from schema.gps_schema import GpsSchema
from schema.parking_schema import ParkingEmptyCount
from domain.parking import Parking
import config

class FileDatasource:
    class SensorCategory(Enum):
        ACCEL = 'accelerometer'
        GEOPOSITION = 'gps'
        PARKING = 'parking'
    
    def __init__(self, accelerometer_path: str, gps_path: str, parking_path: str):
        self.sensorRegistry = {
            self.SensorCategory.ACCEL: SensorInterface(accelerometer_path, AccelerometerSchema()),
            self.SensorCategory.GEOPOSITION: SensorInterface(gps_path, GpsSchema()),
            self.SensorCategory.PARKING: SensorInterface(parking_path, ParkingEmptyCount())
        }

    def startReading(self):
        for sensor in self.sensorRegistry.values():
            sensor.beginDataCapture()

    def stopReading(self):
        for sensor in self.sensorRegistry.values():
            sensor.endDataCapture()

    def process(self, sequence_length: int = 1):
        if any(not sensor.reader for sensor in self.sensorRegistry.values()):
            raise Exception("Sensor readers not initialized. Invoke 'activateSensors' prior to data gathering.")
        
        aggregatedResults = []
        for _ in range(sequence_length):
            sensorData = {category: sensor.fetchData() for category, sensor in self.sensorRegistry.items()}
            currentTime = datetime.now()
            aggregatedInfo = AggregatedData(sensorData[self.SensorCategory.ACCEL], sensorData[self.SensorCategory.GEOPOSITION], currentTime, config.USER_ID)
            parkingDetails = Parking(sensorData[self.SensorCategory.PARKING]["empty_count"], sensorData[self.SensorCategory.GEOPOSITION])
            aggregatedResults.append((aggregatedInfo, parkingDetails))
        return aggregatedResults

class SensorInterface:
    def __init__(self, file_location, schema: Schema):
        self.file_location = file_location
        self.schema = schema
        self.file_stream = None
        self.reader = None

    def beginDataCapture(self):
        self.file_stream = open(self.file_location, 'r')
        self.reader = DictReader(self.file_stream)

    def fetchData(self):
        record = next(self.reader, None)
        if record is None:
            self.resetReader()
            record = next(self.reader, None)
        return self.schema.load(record)

    def resetReader(self):
        self.file_stream.seek(0)
        self.reader = DictReader(self.file_stream)

    def endDataCapture(self):
        if self.file_stream:
            self.file_stream.close()
            self.file_stream = None
            self.reader = None
