################################################################################
# Script Name: analytics_processor.py
# Description: This script simulates user events and sends them to a Kafka topic
#              named "user-events". It generates random user actions such as
#              login, view_product, add_to_cart, checkout, and logout,
#              and sends these events with a timestamp to the Kafka topic.
#              The script also stores the events in a JSON file for 2 minutes
#              before terminating.
# Author: logarajeshwaran
# Created Date: 2025-04-21
# License: MIT License
################################################################################

from kafka import KafkaProducer
import random
import time
import json

actions = ['login', 'view_product', 'add_to_cart', 'checkout', 'logout']
user_ids = [f"user_{i}" for i in range(1000)]
output_file = "/home/kafka/kafka-work/Real-time Analytics Dashboard/images/user_events_output.json"

producer = KafkaProducer(bootstrap_servers='localhost:9092')

start_time = time.time()
events = []  # List to store events

while True:
    user = random.choice(user_ids)
    action = random.choice(actions)
    timestamp = int(time.time() * 1000)  # milliseconds
    
    event = {
        'user_id': user,
        'action': action,
        'timestamp': timestamp
    }
    
    # Send the event to Kafka
    producer.send('user-events', value=json.dumps(event).encode('utf-8'))
    
    # Store the event in the list
    events.append(event)
    
    # Check if 2 minutes have elapsed
    if time.time() - start_time > 120:
        break
    
    time.sleep(random.uniform(0.01, 0.1))

# Write the events to a JSON file
with open(output_file, 'w') as f:
    json.dump(events, f, indent=4)

print(f"Stored {len(events)} events in {output_file}.")