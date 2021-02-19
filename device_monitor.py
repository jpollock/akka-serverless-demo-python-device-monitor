"""
Copyright 2020 Lightbend Inc.
Licensed under the Apache License, Version 2.0.
"""

from cloudstate.cloudstate import CloudState
from device_monitor_entity import entity as device_monitor_entity
import logging

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    CloudState().register_event_sourced_entity(device_monitor_entity).start()