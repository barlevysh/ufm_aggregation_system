from pathlib import Path
import os
import uvicorn
from ufm_aggregator_app.ufm_aggregator_web_app import UfmAggregatorWebApp
from ufm_aggregator_app.ufm_performance_store import UfmPerformanceStore
from ufm_aggregator_app.ufm_telemetry_store import UfmTelemetryStore
from ufm_aggregator_app.ufm_common import LOG_FILE


def ensure_file_exists():
    """
    Checks if a file exists at the given filepath and creates it if it doesn't.
    """
    full_path = os.path.join(Path.cwd(), LOG_FILE)
    file_path_obj = Path(full_path)

    if not file_path_obj.exists():
        file_path_obj.parent.mkdir(parents=True, exist_ok=True)
        file_path_obj.touch()

if __name__ == "__main__":
  ensure_file_exists()
  performance_store = UfmPerformanceStore()
  telemetry_store = UfmTelemetryStore()
  telemetry_app = UfmAggregatorWebApp(performance_store=performance_store, telemetry_store=telemetry_store).create_telemetry_app()
  uvicorn.run(telemetry_app, host="127.0.0.1", port=8000)
