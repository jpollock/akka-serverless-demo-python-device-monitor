"""
Copyright 2020 Lightbend Inc.
Licensed under the Apache License, Version 2.0.
"""

from dataclasses import dataclass, field
from typing import Dict, List
import time, calendar, datetime, math, json
import statistics
from sklearn import linear_model
import numpy as np


from google.protobuf.empty_pb2 import Empty
from cloudstate.event_sourced_context import EventSourcedCommandContext
from cloudstate.event_sourced_entity import EventSourcedEntity

from DeviceMonitor_pb2 import (NewMetricValue, MetricValue)
from DeviceMonitor_pb2 import (_DEVICEMONITOR, DESCRIPTOR as FILE_DESCRIPTOR)

import monitor_constants

@dataclass
class DeviceMonitorState:
    entity_id: str
    current: float
    last_reading_timestamp: int
    history: List[float]
    time_bucket_history: Dict[str, List[float]]

def init(entity_id: str) -> DeviceMonitorState:
    return DeviceMonitorState(entity_id, 0.0, 0, [], {})

entity = EventSourcedEntity(_DEVICEMONITOR, [FILE_DESCRIPTOR], init)


# helper function
def five_minute_bucket_from_time(timestamp):
    dt = datetime.datetime.fromtimestamp(timestamp)
    #print(monitor_constants.BUCKET_TYPE == 'minute')
    key = str(dt.hour) + '_' + str(math.floor(dt.minute if monitor_constants.BUCKET_TYPE == 'minute' else dt.second / monitor_constants.BUCKET))
    #print(key)
    return key

# helper function
def stats_for_list(history):
    stats = {}
    stats['median'] = statistics.median(history)
    stats['mean'] = statistics.fmean(history)
    stats['stdev'] = statistics.stdev(history)
    return stats

@entity.event_handler(NewMetricValue)
def new_metric_value(state: DeviceMonitorState, event: NewMetricValue):
    state.current = event.new_value
    state.last_reading_timestamp = event.timestamp
    state.history.append(event.new_value)

    # deal with time buckets (possible aggregation use case)
    dt_key = five_minute_bucket_from_time(event.timestamp)
    if dt_key not in state.time_bucket_history:
        state.time_bucket_history[dt_key] = []
    state.time_bucket_history[dt_key].append(event.new_value)

    # trim our lists if greater than limits
    if len(state.time_bucket_history[dt_key]) > monitor_constants.MAX_SIZE_BUCKET_HISTORY:
        state.time_bucket_history[dt_key] = state.time_bucket_history[dt_key][-monitor_constants.MAX_SIZE_BUCKET_HISTORY:]
    if len(state.history) > monitor_constants.MAX_SIZE_HISTORY: # just keep 1000 values
        state.history = state.histor[-monitor_constants.MAX_SIZE_HISTORY:]
    

@entity.command_handler("GetCurrentValue")
def get_current_value(state: DeviceMonitorState):
    value = MetricValue()
    value.current_value = state.current
    dt_key = five_minute_bucket_from_time(state.last_reading_timestamp)
    l_tb_history = state.time_bucket_history[dt_key]
    if len(state.history) > 1:
        value.prior_value = state.history[len(state.history)-2]
        stats = stats_for_list(state.history)
        value.stats_for_recent_history.median = stats['median']
        value.stats_for_recent_history.mean = stats['mean']
        value.stats_for_recent_history.stdev = stats['stdev']

    if len(state.history) > monitor_constants.PREDICTION_THRESHOLD:
        data = [[i,x] for i,x in enumerate(state.history)]
        X = np.array(data)[:,0].reshape(-1,1)
        y = np.array(data)[:,1].reshape(-1,1)
        to_predict_x= list(range(len(state.history), len(state.history)+monitor_constants.PREDICTION_THRESHOLD))
        to_predict_x= np.array(to_predict_x).reshape(-1,1)      
        regsr=linear_model.LinearRegression()
        regsr.fit(X,y)
        predicted_y = regsr.predict(to_predict_x)
        value.stats_for_recent_history.predictions.extend([flattened for value in predicted_y.tolist() for flattened in value])
    
    if len(l_tb_history) > monitor_constants.PREDICTION_THRESHOLD:
        stats = stats_for_list(l_tb_history)
        value.stats_for_time_bucket.median = stats['median']
        value.stats_for_time_bucket.mean = stats['mean']
        value.stats_for_time_bucket.stdev = stats['stdev']

        data = [[i,x] for i,x in enumerate(l_tb_history)]
        X = np.array(data)[:,0].reshape(-1,1)
        y = np.array(data)[:,1].reshape(-1,1)
        to_predict_x= list(range(len(l_tb_history), len(l_tb_history)+monitor_constants.PREDICTION_THRESHOLD))
        to_predict_x= np.array(to_predict_x).reshape(-1,1)      
        regsr=linear_model.LinearRegression()
        regsr.fit(X,y)
        predicted_y = regsr.predict(to_predict_x)
        value.stats_for_time_bucket.predictions.extend([flattened for value in predicted_y.tolist() for flattened in value])
    
    return value

@entity.command_handler("UpdateMetric")
def update_metric(item: NewMetricValue, ctx: EventSourcedCommandContext):
    ctx.emit(item)
    return Empty()


# current number
# stats: last n readings
# stats: same time
# prediction: