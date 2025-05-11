################################################################################
# Script Name: generate_user_events.py
# Description: This script simulates user events and sends them to a Kafka topic
#              named "user-events". It generates random user actions such as
#              login, view_product, add_to_cart, checkout, and logout, 
#              and sends these events with a timestamp to the Kafka topic.
# Author: logarajeshwaran
# Created Date: 2025-04-21
# License: MIT License
################################################################################


from kafka import KafkaProducer
import random
import time

actions = ['login', 'view_product', 'add_to_cart', 'checkout', 'logout']
user_ids = [f"user_{i}" for i in range(1000)]

producer = KafkaProducer(bootstrap_servers='localhost:9092')

while True:
    user = random.choice(user_ids)
    action = random.choice(actions)
    timestamp = int(time.time() * 1000)  # milliseconds
    
    event = {
        'user_id': user,
        'action': action,
        'timestamp': timestamp
    }
    
    producer.send('user-events', value=str(event).encode())
    time.sleep(random.uniform(0.01, 0.1))