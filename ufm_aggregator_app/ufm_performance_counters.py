from ufm_common import PerformenceCounter

class UfmIngestPerformanceCounters:{
  PerformenceCounter.TOTAL_INGEST_COUNT_24: int,
  PerformenceCounter.TOTAL_INGEST_FAILURES_24: int,
  PerformenceCounter.MAX_INGEST_DURATION_MS: float,
  PerformenceCounter.AVG_INGEST_DURATION_MS: float,
  PerformenceCounter.MIN_INGEST_DURATION_MS: float,
}

class UfmApiPerformanceCounters:{
  PerformenceCounter.TOTAL_API_REQUESTS_24: int,
  PerformenceCounter.TOTAL_API_REQUESTS_FAILURES_24: int,
  PerformenceCounter.MIN_API_LATENCY_MS: float,
  PerformenceCounter.AVG_API_LATENCY_MS: float,
  PerformenceCounter.MAX_API_LATENCY_MS: float,
}
