"""
File: log_aggregator.py
Author: logarajeshwaran
Date: 2025-04-20
Description: This script consumes log messages from a Kafka topic, aggregates log levels, 
             and prints a summary of the log statistics periodically.
"""

from kafka import KafkaConsumer
import json
from datetime import datetime

consumer = KafkaConsumer('application-logs', bootstrap_servers='localhost:9092',
                        group_id='log-aggregators')

log_counts = {'INFO': 0, 'WARN': 0, 'ERROR': 0}

try:
    for msg in consumer:
        log = msg.value.decode()
        service = msg.key.decode()
        
        # Count log levels
        for level in log_counts.keys():
            if level in log:
                log_counts[level] += 1
                
        # Print summary every 10 messages
        if sum(log_counts.values()) % 10 == 0:
            print(f"\nLog Summary at {datetime.now()}:")
            for level, count in log_counts.items():
                print(f"{level}: {count}")
                
except KeyboardInterrupt:
    print("\nFinal Log Counts:")
    print(json.dumps(log_counts, indent=2))