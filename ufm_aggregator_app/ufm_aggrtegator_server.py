"""
Run this as: python aggregator_server.py

FastAPI server that:
- polls the telemetry generator at 127.0.0.1:9001/counters periodically (every 10s)
- keeps latest metrics in TelemetryStore
- exposes REST endpoints at 127.0.0.1:8080/telemetry/

Endpoints:
- GET /telemetry/get_metric?switch_id=sw-01&metric=bandwidth
- GET /telemetry/list_metrics?metrics=bandwidth,latency


Basic logging and per-request timing are implemented.
"""
import asyncio
import logging
import time
import httpx
from ufm_aggregator_app.ufm_counters_csv_parser import parse_counters_csv
from ufm_aggregator_app.ufm_telemetry_store import UfmTelemetryStore
from ufm_aggregator_app.ufm_performance_store import UfmPerformanceStore
from ufm_aggregator_app.ufm_common import LOG_FILE

class UfmAggregatorServer:
  TELEMETRY_SOURCE = 'http://localhost:9001/counters'
  POLL_INTERVAL = 10
  CLIENT_TIMEOUT_SEC = 5

  def __init__(self, performance_store: UfmPerformanceStore, telemetry_store: UfmTelemetryStore):
    self.__config_logging()
    self.__logger = logging.getLogger('Ufm-Aggregator-Server')
    self.__performance_store = performance_store
    self.__telemetry_store = telemetry_store
    self.__ingester_task = None

  def __config_logging(self):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s',
                        handlers=[logging.FileHandler(LOG_FILE, mode='a'), logging.StreamHandler()])

  async def __get_telemetry_counters(self):
    """Asynchronously fetches telemetry counters."""
    async with httpx.AsyncClient(timeout=self.CLIENT_TIMEOUT_SEC) as client:
      csv_response = ""
      try:
        response = await client.get(self.TELEMETRY_SOURCE, follow_redirects=True)
        response.raise_for_status()
        csv_response = response.text
        self.__logger.debug(f"Successfuly fetch counters: {csv_response}")
      except httpx.TimeoutException:
        self.__logger.exception(f"Fetch telemetry counters request timed out after {self.CLIENT_TIMEOUT_SEC} seconds.")
      except httpx.HTTPStatusError as e:
        self.__logger.exception(f"HTTP error occurred: {e}")
      except httpx.RequestError as e:
        self.__logger.exception(f"An error occurred while requesting: {e}")
      finally:
        return csv_response

  async def __ingester(self):
    self.__logger.info('Ufm Aggregator server ingest loop started successfuly')
    while True:
      try:
        t0 = time.perf_counter()        
        text = await self.__get_telemetry_counters()
        parsed = await parse_counters_csv(text)
        await self.__telemetry_store.replace_bulk(parsed)
        t1 = time.perf_counter()
        self.__performance_store.update_total_ingest_requests()
        self.__performance_store.update_ingest_duration_stat(t1- t0)
        self.__logger.info(f'Ingested telemetry: {len(parsed)} switches in {(t1 - t0):.3f} seconds')
      except Exception as e:
        self.__performance_store.update_total_ingest_requests_failures()
        self.__logger.exception('Failed to ingest telemetry')
      await asyncio.sleep(self.POLL_INTERVAL)

  def start(self):
    self.__ingester_task = asyncio.create_task(self.__ingester())

  async def stop(self):
    if self.__ingester_task:
      self.__ingester_task.cancel()
    try:
      await self.__ingester_task
    except asyncio.CancelledError:
      self.__logger.warning("Failed stopping ingestion task gracefuly")