from ufm_aggregator_app.ufm_common import CounterType, SWITCH_NAME, TIMESTAMP

async def parse_counters_csv(text: str):
  out = []
  csv_pre_parse = text.replace('\\r\\n', ';')
  csv_lines = csv_pre_parse.split(';')
  fields = csv_lines[0].split(',')
  for line in csv_lines[1:]:
    if line:
      values = line.split(',')
      if values and len(values) == len(fields):
        out.append({
          SWITCH_NAME: values[0],
          CounterType.BANDWIDTH_USAGE.value: values[1],
          CounterType.LATENCY.value: values[2], 
          CounterType.PACKET_ERROR.value: values[3],
          TIMESTAMP: values[4]
        })
  return out

  
