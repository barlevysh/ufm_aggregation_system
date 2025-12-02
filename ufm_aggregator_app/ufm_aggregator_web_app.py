from contextlib import asynccontextmanager
import asyncio
import logging
import time
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from ufm_aggregator_app.ufm_aggrtegator_server import UfmAggregatorServer
from ufm_aggregator_app.ufm_performance_store import UfmPerformanceStore
from ufm_aggregator_app.ufm_telemetry_store import UfmTelemetryStore
from ufm_aggregator_app.ufm_common import LOG_FILE


class UfmAggregatorWebApp:
  def __init__(self, performance_store: UfmPerformanceStore, telemetry_store: UfmTelemetryStore):
    self.__config_logging()
    self.__logger = logging.getLogger('Ufm-Web-App')
    self.__performance_store = performance_store
    self.__telemetry_store = telemetry_store

  def __config_logging(self):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s',
                        handlers=[logging.FileHandler(LOG_FILE, mode='a'), logging.StreamHandler()])

  @asynccontextmanager
  async def __telemetry_lifespan(self, app: FastAPI):
    """
    An asynchronous context manager for managing the telemetry application lifespan.
    pre 'yield' instruction will run on startup.
    post 'yield' instruction will run on shutdown.
    """
    app.state.ufm_aggregator = UfmAggregatorServer(self.__performance_store, self.__telemetry_store)
    app.state.ufm_aggregator.start()
    yield
    await app.state.ufm_aggregator.stop()

  def create_telemetry_app(self):
    telemetry_app = FastAPI(lifespan=self.__telemetry_lifespan)

    @telemetry_app.middleware('http')
    async def time_measured_request(request: Request, call_next):
      t0 = time.perf_counter()
      response = await call_next(request)
      t1 = time.perf_counter()
      latency_ms = (t1 - t0) * 1000
      self.__performance_store.update_total_api_requests()
      self.__performance_store.update_api_duration_stat(latency_ms)
      self.__logger.info(f"{request.method} {request.url.path} - {latency_ms:.2f}ms")
      return response

    @telemetry_app.get('/telemetry/get_metric')
    async def get_metric(switch_name: str, metric: str):
      try:
        value = await self.__telemetry_store.get_metric(switch_name, metric)
        return JSONResponse({'switch_name': switch_name, 'metric': metric, 'value': value})
      except KeyError as e:
        self.__logger.info("Failed to find metric '{metric}' for switch '{switch_name}")
        self.__performance_store.update_total_api_requests_failures()
        raise HTTPException(status_code=404, detail=str(e))

    @telemetry_app.get('/telemetry/list_metrics')
    async def list_metrics():
      data = await self.__telemetry_store.list_metrics()
      return JSONResponse({'metrics': data})

    @telemetry_app.get('/telemetry/performance')
    async def get_perf():
      return JSONResponse(self.__performance_store.report_json())
    
    return telemetry_app
