################################################################################
# Script Name: producer.py
# Description: This script acts as a Kafka producer to send messages to the
#              specified Kafka topic. It demonstrates how to connect to a Kafka
#              server and produce messages.
# Author: logarajeshwaran
# Created Date: 2025-04-20
# License: MIT License
################################################################################

from kafka import KafkaProducer
import time 


producer = KafkaProducer(bootstrap_servers='localhost:9092')

for i in range(10):
    message = f"Message {i} at {time.time()}"
    producer.send('simple-messages', message.encode('utf-8'))
    print(f"Sent: {message}")
    time.sleep(1)

producer.flush()

