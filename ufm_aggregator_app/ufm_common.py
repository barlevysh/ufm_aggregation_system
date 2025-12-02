from enum import StrEnum, auto

TIMESTAMP = "timestamp"
SWITCH_NAME = "server_name"
LOG_FILE = "logs/ufm_telemetry.log"

class PerformenceCounter(StrEnum):
  TOTAL_INGEST_COUNT_24 = auto()
  TOTAL_INGEST_FAILURES_24 = auto()
  MAX_INGEST_DURATION_MS = auto()
  AVG_INGEST_DURATION_MS = auto()
  MIN_INGEST_DURATION_MS = auto()

  TOTAL_API_REQUESTS_24 = auto()
  TOTAL_API_REQUESTS_FAILURES_24 = auto()
  MAX_API_LATENCY_MS = auto()
  AVG_API_LATENCY_MS = auto()
  MIN_API_LATENCY_MS = auto()

class CounterType(StrEnum):
  BANDWIDTH_USAGE = auto()
  LATENCY = auto()
  PACKET_ERROR = auto()