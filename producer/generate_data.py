import argparse
import datetime as dt
import io
import json
import os
import random
import sys
import time

import boto3

class MeasurementRecord(object):
    def __init__(self):
        self.sensorid = random.randint(1,10)
        self.timestamp = round(time.time())
        self.measurement = round(random.random()*10+20,1)
    def get_record(self):
        record = {
            "sensorid": self.sensorid,
            "eventtime": self.timestamp,
            "temperature": self.measurement
        }
        data = json.dumps(record)
        return {"Data": bytes(data, "utf-8"), "PartitionKey": "partition_key"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--streamname", action="store", dest="stream_name")
    args = parser.parse_args()
    session = boto3.Session(profile_name="app_user")
    try:
        kinesis_client = session.client("kinesis", "us-east-1")
        while True:
            kinesis_client.put_records(StreamName=args.stream_name,
                                       Records=[MeasurementRecord().get_record() for _ in range(10)])
            time.sleep(1)
    except:
        print("Error:", sys.exc_info()[0])
        raise
