import random
from datetime import datetime
import asyncio
import io
import threading
import csv
from ufm_telemetry_generator_common import CounterType, TIMESTAMP, SWITCH_NAME
from ufm_metric_generator import UfmMetricGenerator

class UfmTelemetryGenerator:
  ALTERNATE_CSV_EXPORT_COUNT = 2
  UPDATE_INTERVAL_SEC = 10

  def __init__(self):
    self.__switches = [f"sw-{i:02d}" for i in range(1, 11)]
    self.__metric_generator = UfmMetricGenerator()
    self.__metrics = self.__metric_generator.initialize_metrics(self.__switches)
    self.__current_csv = 0
    self.__csv = [None] * self.ALTERNATE_CSV_EXPORT_COUNT
    self.__data_lock = threading.Lock()

  def __export_csv_alternate(self):
    csv_string = self.__build_csv()
    with self.__data_lock:
      self.__current_csv = (self.__current_csv + 1) % 2
      self.__csv[self.__current_csv] = csv_string

  def __build_csv(self):
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=[SWITCH_NAME, CounterType.BANDWIDTH_USAGE, CounterType.LATENCY, 
                                                CounterType.PACKET_ERROR, TIMESTAMP])
    writer.writeheader()
    writer.writerows(self.__metrics)
    csv_str = output.getvalue()
    print(csv_str)
    return csv_str

  async def __updater(self):
    while True:
      self.__metric_generator.update_metrics(self.__metrics)
      self.__export_csv_alternate()
      await asyncio.sleep(self.UPDATE_INTERVAL_SEC)

  def start(self):
    asyncio.create_task(self.__updater())

  async def get_csv(self):
    with self.__data_lock:
      return self.__csv[self.__current_csv]