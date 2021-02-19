import time, calendar, datetime, math, json
from device_monitor_entity import DeviceMonitorState, new_metric_value, get_current_value
from DeviceMonitor_pb2 import (NewMetricValue, MetricValue)

d = DeviceMonitorState('1', 0.0, 0, [], {})

v = NewMetricValue()
v.device_id = '1'
v.timestamp = calendar.timegm(time.gmtime())
v.new_value = 1.2
new_metric_value(d, v)
print(get_current_value(d))
time.sleep(1)
v.timestamp = calendar.timegm(time.gmtime())
v.new_value = 1.3
new_metric_value(d, v)
print(get_current_value(d))
time.sleep(1)

v.timestamp = calendar.timegm(time.gmtime())
v.new_value = 1.4
new_metric_value(d, v)
print(get_current_value(d))
time.sleep(1)

v.timestamp = calendar.timegm(time.gmtime())
v.new_value = 1.5
new_metric_value(d, v)
print(get_current_value(d))
time.sleep(1)

v.timestamp = calendar.timegm(time.gmtime())
v.new_value = 1.3
new_metric_value(d, v)
print(get_current_value(d))
time.sleep(1)

v.timestamp = calendar.timegm(time.gmtime())
v.new_value = 1.65
new_metric_value(d, v)
print(get_current_value(d))
time.sleep(1)

v.timestamp = calendar.timegm(time.gmtime())
v.new_value = 1.66
new_metric_value(d, v)
print(get_current_value(d))

v.timestamp = calendar.timegm(time.gmtime())
v.new_value = 1.70
new_metric_value(d, v)
print(get_current_value(d))

v.timestamp = calendar.timegm(time.gmtime())
v.new_value = 1.73
new_metric_value(d, v)
print(get_current_value(d))

v.timestamp = calendar.timegm(time.gmtime())
v.new_value = 1.78
new_metric_value(d, v)
print(get_current_value(d))

v.timestamp = calendar.timegm(time.gmtime())
v.new_value = 1.82
new_metric_value(d, v)
print(get_current_value(d))

v.timestamp = calendar.timegm(time.gmtime())
v.new_value = 1.82
new_metric_value(d, v)
print(get_current_value(d))

v.timestamp = calendar.timegm(time.gmtime())
v.new_value = 1.82
new_metric_value(d, v)
print(get_current_value(d))

v.timestamp = calendar.timegm(time.gmtime())
v.new_value = 1.78
new_metric_value(d, v)

print(get_current_value(d))

v.timestamp = calendar.timegm(time.gmtime())
v.new_value = 1.80
new_metric_value(d, v)
print(get_current_value(d))

v.timestamp = calendar.timegm(time.gmtime())
v.new_value = 1.81
new_metric_value(d, v)
print(get_current_value(d))

v.timestamp = calendar.timegm(time.gmtime())
v.new_value = 1.82
new_metric_value(d, v)

print(get_current_value(d))

#print(d)