"""
File: service_logger.py
Author: logarajeshwaran
Date: 2025-04-20
Description: This script simulates multiple services sending logs to a Kafka topic. 
             Each log contains a service name, log level, and timestamp.
"""

from kafka import KafkaProducer
import random
import time

services = ['auth-service', 'payment-service', 'inventory-service']
levels = ['INFO', 'WARN', 'ERROR']

producer = KafkaProducer(bootstrap_servers='localhost:9092')

while True:
    service = random.choice(services)
    level = random.choice(levels)
    log_msg = f"{level}: Action performed in {service} at {time.time()}"
    
    # Send to partition based on service name hash
    producer.send('application-logs', key=service.encode(), value=log_msg.encode())
    print(log_msg)
    time.sleep(random.uniform(0.1, 0.5))