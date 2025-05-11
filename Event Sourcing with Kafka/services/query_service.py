################################################################################
# Script Name: query_service.py
# Description: This script acts as a query service by consuming events from the
#              Kafka topic "bank-events". It maintains an in-memory state of 
#              accounts (e.g., balances) based on the events received, such as
#              account creation, money debits, and credits. The current state
#              of all accounts is displayed after processing each event.
# Author: logarajeshwaran
# Created Date: 2025-05-11
# License: MIT License
# Requirements:
#   - Kafka server running on localhost:9092
#   - Python libraries: kafka-python, json (install kafka-python via pip)
# Usage:
#   - Run the script to process events from the Kafka topic "bank-events"
#     and display the current state of accounts.
# Notes:
#   - This script uses an in-memory store (`accounts` dictionary) to track
#     account balances. In a production setup, this would typically be replaced
#     with a database.
################################################################################

from kafka import KafkaConsumer
import json

consumer = KafkaConsumer('bank-events', bootstrap_servers='localhost:9092',
                         group_id='query-service',
                         value_deserializer=lambda x: json.loads(x.decode('utf-8')))

accounts = {}

print("Starting query service...")
for event in consumer:
    if event.value['type'] == 'ACCOUNT_CREATED':
        accounts[event.value['account_id']] = {
            'name': event.value['name'],
            'balance': event.value['balance']
        }
    elif event.value['type'] == 'MONEY_DEBITED':
        accounts[event.value['account_id']]['balance'] = event.value['new_balance']
    elif event.value['type'] == 'MONEY_CREDITED':
        accounts[event.value['account_id']]['balance'] = event.value['new_balance']
    
    print("\nCurrent Account State:")
    for account_id, data in accounts.items():
        print(f"Account {account_id}: {data['name']} - Balance: {data['balance']}")