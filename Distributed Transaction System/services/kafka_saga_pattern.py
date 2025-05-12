"""
File: kafka_saga_pattern.py
Author: logarajeshwaran
Date: 2025-05-12
Description: This script demonstrates the implementation of the Saga pattern using Kafka for distributed transactions.
             It consists of three microservices: Order Service, Payment Service, and Inventory Service, 
             which communicate with each other using Kafka topics.

Key Features:
- Order Service: Publishes "order-created" events and listens for "inventory-updated" events.
- Payment Service: Listens for "order-created" events and publishes "payment-processed" events.
- Inventory Service: Listens for "payment-processed" events and publishes "inventory-updated" events.
- Utilizes Kafka for asynchronous communication between services.

Kafka Topics:
- `order-created`: Published by Order Service when an order is created.
- `payment-processed`: Published by Payment Service after payment processing.
- `inventory-updated`: Published by Inventory Service after inventory update.

Dependencies:
- kafka-python (Install with `pip install kafka-python`)
- multiprocessing (Built-in Python library for parallel execution)

Usage:
- Run the script to simulate the distributed transaction flow using the Saga pattern.
"""

from kafka import KafkaProducer, KafkaConsumer
import json
import time

KAFKA_BROKER = 'localhost:9092'

def create_producer():
    return KafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

def create_consumer(topic, group_id):
    return KafkaConsumer(
        topic,
        bootstrap_servers=KAFKA_BROKER,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id=group_id,
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )

# ========================
# Order Service
# ========================
def order_service():
    producer = create_producer()
    order = {
        "orderId": "order_001",
        "userId": "user_001",
        "items": [{"itemId": "item_001", "qty": 1}],
        "total": 100
    }
    print("[Order Service] Sending order-created event")
    producer.send('order-created', order)
    producer.flush()

    consumer = create_consumer('inventory-updated', 'order-service')
    for msg in consumer:
        if msg.value['orderId'] == order['orderId']:
            print("[Order Service] Received inventory-updated. Order Completed!")
            break

# ========================
# Payment Service
# ========================
def payment_service():
    consumer = create_consumer('order-created', 'payment-service')
    producer = create_producer()

    for msg in consumer:
        order = msg.value
        print(f"[Payment Service] Processing payment for Order: {order['orderId']}")
        time.sleep(1)  
        payment_event = {
            "orderId": order['orderId'],
            "paymentStatus": "SUCCESS",
            "transactionId": "txn_123"
        }
        print("[Payment Service] Sending payment-processed event")
        producer.send('payment-processed', payment_event)
        producer.flush()

# ========================
# Inventory Service
# ========================
def inventory_service():
    consumer = create_consumer('payment-processed', 'inventory-service')
    producer = create_producer()

    for msg in consumer:
        payment = msg.value
        print(f"[Inventory Service] Updating inventory for Order: {payment['orderId']}")
        time.sleep(1)  
        inventory_event = {
            "orderId": payment['orderId'],
            "inventoryStatus": "UPDATED"
        }
        print("[Inventory Service] Sending inventory-updated event")
        producer.send('inventory-updated', inventory_event)
        producer.flush()

# ========================
# Main Entry Point
# ========================
if __name__ == '__main__':
    from multiprocessing import Process


    Process(target=payment_service).start()
    Process(target=inventory_service).start()
    time.sleep(2)  
    order_service()
