from ufm_telemetry_generator_common import CounterType, TIMESTAMP, SWITCH_NAME

class UfmTelemetryMetric:{
    SWITCH_NAME: str,
    TIMESTAMP: int,
    CounterType.BANDWIDTH_USAGE: int,
    CounterType.LATENCY: int,
    CounterType.PACKET_ERROR: int,
}