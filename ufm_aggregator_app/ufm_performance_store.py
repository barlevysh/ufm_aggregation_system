import json
from datetime import datetime, timedelta
from ufm_aggregator_app.ufm_common import PerformenceCounter, TIMESTAMP

class UfmPerformanceStore:
  def __init__(self):
    self.__last_reset = datetime.utcnow()

    self.__ingest_duration_update_count = 0
    self.__api_duration_update_count = 0    

    self.__ingest_counter = {
      PerformenceCounter.TOTAL_INGEST_COUNT_24.value: 0,
      PerformenceCounter.TOTAL_INGEST_FAILURES_24.value: 0,
      PerformenceCounter.MAX_INGEST_DURATION_MS.value: 0.0,
      PerformenceCounter.AVG_INGEST_DURATION_MS.value: 0.0,
      PerformenceCounter.MIN_INGEST_DURATION_MS.value: 0.0,
    }

    self.__api_counter = {
      PerformenceCounter.TOTAL_API_REQUESTS_24.value: 0,
      PerformenceCounter.TOTAL_API_REQUESTS_FAILURES_24.value: 0,
      PerformenceCounter.MIN_API_LATENCY_MS.value: 0.0,
      PerformenceCounter.AVG_API_LATENCY_MS.value: 0.0,
      PerformenceCounter.MAX_API_LATENCY_MS.value: 0.0,
    }

  def __reset(self):
    self.__ingest_counter[PerformenceCounter.TOTAL_INGEST_COUNT_24.value] = 0
    self.__ingest_counter[PerformenceCounter.TOTAL_INGEST_FAILURES_24.value] = 0
    self.__ingest_counter[PerformenceCounter.MAX_INGEST_DURATION_MS.value] = 0.0
    self.__ingest_counter[PerformenceCounter.AVG_INGEST_DURATION_MS.value] = 0.0
    self.__ingest_counter[PerformenceCounter.MIN_INGEST_DURATION_MS.value] = 0.0

    self.__api_counter[PerformenceCounter.TOTAL_API_REQUESTS_24.value] = 0
    self.__api_counter[PerformenceCounter.TOTAL_API_REQUESTS_FAILURES_24.value] = 0
    self.__api_counter[PerformenceCounter.MIN_API_LATENCY_MS.value] = 0.0
    self.__api_counter[PerformenceCounter.AVG_API_LATENCY_MS.value] = 0.0
    self.__api_counter[PerformenceCounter.MAX_API_LATENCY_MS.value] = 0.0

    self.__ingest_duration_update_count = 0
    self.__api_duration_update_count = 0    

  def __verify_reset(self):
    now = datetime.now()
    if timedelta(hours=24) <= now - self.__last_reset:
      self.__reset()
      self.__last_reset = now

  def update_total_ingest_requests(self, more: int = 1):
    self.__verify_reset()
    self.__ingest_counter[PerformenceCounter.TOTAL_INGEST_COUNT_24.value] += more

  def update_total_ingest_requests_failures(self, more: int = 1):
    self.__verify_reset()
    self.__ingest_counter[PerformenceCounter.TOTAL_INGEST_FAILURES_24.value] += more

  def update_ingest_duration_stat(self, duration: float):
    self.__verify_reset()
    self.__ingest_counter[PerformenceCounter.MAX_INGEST_DURATION_MS.value] = max(self.__ingest_counter
                                                                           [PerformenceCounter.MAX_INGEST_DURATION_MS.value],
                                                                           duration)
    self.__ingest_counter[PerformenceCounter.MIN_INGEST_DURATION_MS.value] = min(self.__ingest_counter
                                                                           [PerformenceCounter.MIN_INGEST_DURATION_MS.value],
                                                                           duration)
    new_avg = duration
    if self.__ingest_duration_update_count:
      prev_total_duration = self.__ingest_duration_update_count * self.__ingest_counter[
        PerformenceCounter.AVG_INGEST_DURATION_MS.value]
      new_sum = prev_total_duration + duration
      new_avg = new_sum / (self.__ingest_duration_update_count + 1)
    self.__ingest_duration_update_count += 1
    self.__ingest_counter[PerformenceCounter.AVG_INGEST_DURATION_MS.value] = new_avg

  def update_total_api_requests(self, more: int = 1):
    self.__verify_reset()
    self.__api_counter[PerformenceCounter.TOTAL_API_REQUESTS_24.value] += more

  def update_total_api_requests_failures(self, more: int = 1):
    self.__verify_reset()
    self.__api_counter[PerformenceCounter.TOTAL_API_REQUESTS_FAILURES_24.value] += more

  def update_api_duration_stat(self, latency: float):
    self.__verify_reset()
    self.__api_counter[PerformenceCounter.MAX_API_LATENCY_MS.value] = max(self.__api_counter
                                                                           [PerformenceCounter.MAX_API_LATENCY_MS.value],
                                                                           latency)
    self.__api_counter[PerformenceCounter.MIN_API_LATENCY_MS.value] = min(self.__api_counter
                                                                           [PerformenceCounter.MIN_API_LATENCY_MS.value],
                                                                           latency)
    new_avg = latency
    if self.__api_duration_update_count:
      prev_total_duration = self.__api_duration_update_count * self.__api_counter[
        PerformenceCounter.AVG_API_LATENCY_MS.value]
      new_sum = prev_total_duration + latency
      new_avg = new_sum / (self.__api_duration_update_count + 1)
    self.__api_duration_update_count += 1
    self.__api_counter[PerformenceCounter.AVG_API_LATENCY_MS.value] = new_avg

  def report_json(self):
    additional_info = {f'measure-{TIMESTAMP}': self.__last_reset.isoformat()}
    data = {**additional_info, **self.__ingest_counter, **self.__api_counter}
    return json.dumps(data, indent=4)