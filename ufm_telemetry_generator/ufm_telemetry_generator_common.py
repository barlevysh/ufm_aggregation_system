from enum import StrEnum, auto

TIMESTAMP = "timestamp"
SWITCH_NAME = "server_name"

class CounterType(StrEnum):
  BANDWIDTH_USAGE = auto()
  LATENCY = auto()
  PACKET_ERROR = auto()