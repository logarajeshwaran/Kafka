################################################################################
# Script Name: bank_commands_producer.py
# Description: This script produces Kafka messages for banking operations such
#              as creating accounts and transferring money. It sends commands
#              to the Kafka topic "bank-commands" using a KafkaProducer.
# Author: logarajeshwaran
# Created Date: 2025-05-11
# License: MIT License
# Requirements:
#   - Kafka server running on localhost:9092
#   - Python libraries: kafka-python, uuid, json (install kafka-python via pip)
# Usage:
#   - Define account creation commands with `create_account(name, initial_balance)`
#   - Define money transfer commands with `transfer_money(from_account, to_account, amount)`
# Notes:
#   - This script sends commands to the "bank-commands" topic for further processing.
################################################################################

from kafka import KafkaProducer
import uuid
import json

producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def create_account(name, initial_balance):
    command = {
        'command_id': str(uuid.uuid4()),
        'type': 'CREATE_ACCOUNT',
        'name': name,
        'initial_balance': initial_balance
    }
    producer.send('bank-commands', value=command)
    return command['command_id']

def transfer_money(from_account, to_account, amount):
    command = {
        'command_id': str(uuid.uuid4()),
        'type': 'TRANSFER_MONEY',
        'from_account': from_account,
        'to_account': to_account,
        'amount': amount
    }
    producer.send('bank-commands', value=command)
    return command['command_id']

# Example usage
create_account("Alice", 1000)
create_account("Bob", 500)
transfer_money("Alice", "Bob", 200)