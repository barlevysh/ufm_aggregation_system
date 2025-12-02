import random
from datetime import datetime
from ufm_telemetry_generator_common import CounterType, SWITCH_NAME, TIMESTAMP

class UfmMetricGenerator:
  def initialize_metrics(self, switches):
    metrics = []
    for sw in switches:
      metrics.append({
        SWITCH_NAME: sw,
        TIMESTAMP: datetime.utcnow().isoformat(),
        CounterType.BANDWIDTH_USAGE: round(random.uniform(100.0, 900.0), 2), # Mbps
        CounterType.LATENCY: round(random.uniform(0.3, 10.0), 3), # milliseconds
        CounterType.PACKET_ERROR: 0})
    return metrics
  
  def update_metrics(self, metrics):
    for sw_metric in metrics:
      self.__update_metric(sw_metric=sw_metric)

  def __generate_bandwidth(self, currentBandwidth: int) -> int:
    delta = random.uniform(-20.0, 20.0)
    if random.random() < 0.05:
      delta += random.uniform(-200.0, 200.0)
    return max(0.0, round(currentBandwidth + delta, 2))

  def __generate_latency(self, currentLatency: int) -> int:
      if random.random() < 0.02:
        return round(currentLatency + random.uniform(50, 200), 3)
      else:
        return max(0.1, round(currentLatency + random.uniform(-1.0, 1.0), 3))

  def __generate_packet_errors(self, currentErros: int) -> int:
      if random.random() < 0.01:
        return currentErros + 1
      return currentErros

  def __get_utc_now(self):
    return datetime.utcnow().isoformat()

  def __update_metric(self, sw_metric):
    sw_metric[TIMESTAMP] = self.__get_utc_now()
    sw_metric[CounterType.BANDWIDTH_USAGE] = self.__generate_bandwidth(sw_metric[CounterType.BANDWIDTH_USAGE])
    sw_metric[CounterType.LATENCY] = self.__generate_latency(sw_metric[CounterType.LATENCY])
    sw_metric[CounterType.PACKET_ERROR] = self.__generate_packet_errors(sw_metric[CounterType.PACKET_ERROR])

