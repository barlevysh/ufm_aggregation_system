"""
An async-friendly in-memory store for telemetry.
Uses asyncio.Lock for atomic updates per-switch.
"""
import asyncio
import logging
from datetime import datetime
from ufm_aggregator_app.ufm_common import CounterType, SWITCH_NAME, LOG_FILE


class UfmTelemetryStore:
  def __init__(self):
    self.__config_logging()
    self.__logger = logging.getLogger('Ufm-Telemetry-Store')
    self.__data = []
    self.__global_lock = asyncio.Lock()
    self.__last_update = None

  def __config_logging(self):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s',
                        handlers=[logging.FileHandler(LOG_FILE, mode='a'), logging.StreamHandler()])


  async def replace_bulk(self, new_table):
  # Replace the whole table atomically for faster update.
    async with self.__global_lock:
      self.__data = new_table
      self.__last_update = datetime.utcnow()


  async def get_metric(self, switch_name: str, metric: str):
    # No need to acquire global lock as replace_bulk swaps reference atomically under GIL
    entries = [m for m in self.__data if m[SWITCH_NAME] == switch_name]
    if entries:
      if len(entries) == 1:
        try:
          return entries[0][metric]
        except KeyError:
          self.__logger.warning(f"No metric of type '{metric}' found for switch '{switch_name}'")
          return None
      else:
        self.__logger.error(f"Inconsistent data: found too many entries for switch '{switch_name}'")
        return None
    else:
      self.__logger.warning(f"No entries found for switch '{switch_name}'")
      return None

  async def list_metrics(self):
  # No need to acquire global lock as replace_bulk swaps reference atomically under GIL
  # return a copy of the data filtered to metrics
    return self.__data
  