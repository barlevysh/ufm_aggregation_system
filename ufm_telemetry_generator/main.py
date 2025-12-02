import uvicorn
from ufm_telemetry_generator_app import UfmTelemetryGeneratorWebAppBuilder

if __name__ == "__main__":
  counters_app = UfmTelemetryGeneratorWebAppBuilder().create_counters_app()
  uvicorn.run(counters_app, host="127.0.0.1", port=9001)
