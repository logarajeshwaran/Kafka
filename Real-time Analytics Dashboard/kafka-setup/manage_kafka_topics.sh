#!/bin/bash
# ====================================================================================
# Script Name: manage_kafka_topics.sh
# Description: This script checks if Kafka and Zookeeper are running, then manages
#              Kafka topics ("user-events" and "event-metrics"). If the topics
#              exist, they are deleted. Otherwise, they are created with 3 partitions.
# Author: Your Name (logarajeshwaran)
# Date: 2025-04-21
# Version: 1.0
# Usage: ./manage_kafka_topics.sh
# ====================================================================================

# Kafka and Zookeeper running check
KAFKA_PORT=9092
ZOOKEEPER_PORT=2181

# Function to check if a port is in use
is_port_in_use() {
  local PORT=$1
  netstat -an | grep ":$PORT" | grep LISTEN > /dev/null 2>&1
}

# Check if Kafka is running
if ! is_port_in_use $KAFKA_PORT; then
  echo "Kafka is not running on port $KAFKA_PORT. Please start Kafka and try again."
  exit 1
fi

# Check if Zookeeper is running
if ! is_port_in_use $ZOOKEEPER_PORT; then
  echo "Zookeeper is not running on port $ZOOKEEPER_PORT. Please start Zookeeper and try again."
  exit 1
fi

# Kafka topics to manage
TOPICS=("user-events" "event-metrics")
PARTITIONS=3
BOOTSTRAP_SERVER="localhost:$KAFKA_PORT"

# Function to check if a topic exists
topic_exists() {
  local TOPIC=$1
  /home/kafka/kafka/kafka/bin/kafka-topics.sh --bootstrap-server $BOOTSTRAP_SERVER --list | grep -w $TOPIC > /dev/null 2>&1
}

# Managing topics
for TOPIC in "${TOPICS[@]}"; do
  if topic_exists $TOPIC; then
    echo "Topic '$TOPIC' exists. Deleting it now..."
    /home/kafka/kafka/kafka/bin/kafka-topics.sh --bootstrap-server $BOOTSTRAP_SERVER --delete --topic $TOPIC
  else
    echo "Topic '$TOPIC' does not exist. Creating it now..."
    /home/kafka/kafka/kafka/bin/kafka-topics.sh --bootstrap-server $BOOTSTRAP_SERVER --create --topic $TOPIC --partitions $PARTITIONS
  fi
done

echo "Kafka topic management completed."