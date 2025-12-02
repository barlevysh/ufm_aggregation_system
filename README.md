# Network telemetry aggregation system

## System Desription

- System developed in python (Python3.13.7)

- Utilizing packages/build-in: FastApi, CSV, asyncio, random, etc.

- System collects and exposes freshed telemetry data of network switch/server's.</br>
  e.g. bandwidth_usage, latency, packet_error</br>

- System Includes two seperated executables:</br>
  - ufm_telemetry_generator.main.py:
    - Run-it (preferably first): from local-relative folder on cmd-line: "python main.py"
    - Stop
    - Description:
      - a simulator generating fake dat every 10 seconds.</br>
      - Data is exposed via REST API endpoint '/counters/' on local host, port 9001</br>
  - main.py:
    - Run-it: from main folder "python main.py"
    - Description:
      - Fetch and ingest telemetry counters data (currently from above /counter/ endpoint),</br>
      - Stores ingested data in memory for fast fetching,</br>
      - Exposing two main functionalities via REST API endopint /telemetry/:</br>
        - 'get_metric': Retrieves a specific metric (from the fetched-ingested counters) for a specific server:</br>
            Usage example (browser): "*http://localhost:8000/telemetry/get_metric?switch_name=<server_name>&metric=<metric_type>*"</br>
        - 'list_metrics': retrieves all metrics (no filters)
        - 'performance':  retrieves performance counters of the INGESTION and API of the application

## System design (C4 like)

Read more [here](./network_telemetry_aggregate_system_nvidia_int1.pdf)