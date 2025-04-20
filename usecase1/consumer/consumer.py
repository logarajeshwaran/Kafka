################################################################################
# Script Name: consumer.py
# Description: This script acts as a Kafka consumer to consume messages from the
#              specified Kafka topic. It demonstrates how to connect to a Kafka
#              server and consume messages.
# Author: logarajeshwaran
# Created Date: 2025-04-20
# License: MIT License
################################################################################

from kafka import KafkaConsumer

consumer = KafkaConsumer('simple-messages', bootstrap_servers='localhost:9092')

print("Starting consumer...")
for msg in consumer:
    print(f"Received: {msg.value.decode('utf-8')}")