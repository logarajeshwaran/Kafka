#!/bin/bash

################################################################################
# Script Name: create_or_replace_kafka_topic.sh
# Description: This script checks if a Kafka server is running, verifies if a
#              topic exists, deletes it if it does, and creates a new topic.
# Author: logarajeshwaran
# Created Date: 2025-04-20
# License: MIT License
################################################################################

# Kafka server details
KAFKA_SERVER="localhost:9092"
TOPIC="simple-messages"
PARTITIONS=1
REPLICATION_FACTOR=1
KAFKA_BIN_DIR="bin"

# Function to check if Kafka server is running
check_kafka_server() {
  echo "Checking if Kafka server is running on $KAFKA_SERVER..."
  nc -z -v -w5 $(echo $KAFKA_SERVER | cut -d':' -f1) $(echo $KAFKA_SERVER | cut -d':' -f2)
  if [ $? -eq 0 ]; then
    echo "Kafka server is running."
    return 0
  else
    echo "Kafka server is not running. Please start the Kafka server and try again."
    return 1
  fi
}

# Function to check if Kafka topic exists
topic_exists() {
  echo "Checking if topic '$TOPIC' exists..."
  $KAFKA_BIN_DIR/kafka-topics.sh --list --bootstrap-server $KAFKA_SERVER | grep -w $TOPIC > /dev/null
  if [ $? -eq 0 ]; then
    echo "Topic '$TOPIC' exists."
    return 0
  else
    echo "Topic '$TOPIC' does not exist."
    return 1
  fi
}

# Function to delete Kafka topic
delete_kafka_topic() {
  echo "Deleting existing Kafka topic '$TOPIC'..."
  $KAFKA_BIN_DIR/kafka-topics.sh --delete --topic $TOPIC --bootstrap-server $KAFKA_SERVER
  if [ $? -eq 0 ]; then
    echo "Kafka topic '$TOPIC' deleted successfully."
  else
    echo "Failed to delete Kafka topic '$TOPIC'."
  fi
}

# Function to create Kafka topic
create_kafka_topic() {
  echo "Creating Kafka topic '$TOPIC'..."
  $KAFKA_BIN_DIR/kafka-topics.sh --create --topic $TOPIC --bootstrap-server $KAFKA_SERVER --partitions $PARTITIONS --replication-factor $REPLICATION_FACTOR
  if [ $? -eq 0 ]; then
    echo "Kafka topic '$TOPIC' created successfully."
  else
    echo "Failed to create Kafka topic '$TOPIC'."
  fi
}

# Main script execution
check_kafka_server
if [ $? -eq 0 ]; then
  topic_exists
  if [ $? -eq 0 ]; then
    delete_kafka_topic
  fi
  create_kafka_topic
fi