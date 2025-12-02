"""
Run: python telemetry_generator.py

An asynchronous HTTP server:
  - Endpoints:
    > GET /counters -> CSV matrix of telemetry.
  - Maintains an in-memory switches/servers table
  - Updates metrics for each switch every 10 seconds with relevant random values.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from datetime import datetime
from ufm_telemetry_generator import UfmTelemetryGenerator

class UfmTelemetryGeneratorWebAppBuilder:
  def __init__(self):
    self.__server = None

  @asynccontextmanager
  async def __counters_lifespan(self, app: FastAPI):
    """
    An asynchronous context manager for managing the application lifespan.
    pre 'yield' instruction will run on startup.
    post 'yield' instruction will run on shutdown.
    """
    app.state.ufm_generator = UfmTelemetryGenerator()
    app.state.ufm_generator.start()
    yield

  def create_counters_app(self):
    counters_app = FastAPI(lifespan=self.__counters_lifespan)

    @counters_app.get("/counters/")
    async def get_counters():
      csv_string = await counters_app.state.ufm_generator.get_csv()
      return csv_string
    
    return counters_app
