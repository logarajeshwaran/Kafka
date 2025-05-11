################################################################################
# Script Name: event_processor.py
# Description: This script listens to the "bank-commands" Kafka topic, processes
#              banking commands (e.g., account creation, money transfer), and
#              produces corresponding events to the "bank-events" Kafka topic.
#              The script uses an in-memory store to simulate account management.
# Author: logarajeshwaran
# Created Date: 2025-05-11
# License: MIT License
# Requirements:
#   - Kafka server running on localhost:9092
#   - Python libraries: kafka-python, json, uuid (install kafka-python via pip)
# Usage:
#   - Run the script to process commands and generate events in real-time.
# Notes:
#   - This script uses an in-memory store (`accounts` dictionary) to simulate
#     account management. In a production environment, replace this with a
#     persistent database.
################################################################################

from kafka import KafkaConsumer, KafkaProducer
import uuid
import json

consumer = KafkaConsumer('bank-commands', bootstrap_servers='localhost:9092',
                         group_id='event-processor',
                         value_deserializer=lambda x: json.loads(x.decode('utf-8')))

producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Simple in-memory store (would be a DB in production)
accounts = {}

for command in consumer:
    print(f"Processing command: {command.value}")
    
    if command.value['type'] == 'CREATE_ACCOUNT':
        account_id = str(len(accounts) + 1)
        event = {
            'event_id': str(uuid.uuid4()),
            'type': 'ACCOUNT_CREATED',
            'account_id': account_id,
            'name': command.value['name'],
            'balance': command.value['initial_balance']
        }
        accounts[account_id] = {
            'name': command.value['name'],
            'balance': command.value['initial_balance']
        }
        producer.send('bank-events', value=event)
        
    elif command.value['type'] == 'TRANSFER_MONEY':
        from_id = command.value['from_account']
        to_id = command.value['to_account']
        amount = command.value['amount']
        
        if from_id in accounts and to_id in accounts and accounts[from_id]['balance'] >= amount:
            # Create debit event
            debit_event = {
                'event_id': str(uuid.uuid4()),
                'type': 'MONEY_DEBITED',
                'account_id': from_id,
                'amount': amount,
                'new_balance': accounts[from_id]['balance'] - amount
            }
            accounts[from_id]['balance'] -= amount
            producer.send('bank-events', value=debit_event)
            
            # Create credit event
            credit_event = {
                'event_id': str(uuid.uuid4()),
                'type': 'MONEY_CREDITED',
                'account_id': to_id,
                'amount': amount,
                'new_balance': accounts[to_id]['balance'] + amount
            }
            accounts[to_id]['balance'] += amount
            producer.send('bank-events', value=credit_event)