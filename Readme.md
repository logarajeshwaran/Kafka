# Kafka Cheat Sheet

## 1. Confluent-Kafka Overview

`confluent-kafka` is a high-performance Kafka client for Python, built on top of the C-based `librdkafka`. It offers:

- **High Performance**: Faster than `kafka-python`.
- **Better Error Handling**: Provides robust error handling mechanisms.
- **Advanced Configuration Options**: Allows for fine-tuned configurations to meet specific use cases.

## 2. kafka-python Overview

`kafka-python` is a pure Python implementation of Kafka. It provides:

- **Flexibility**: A more flexible implementation for Python developers.
- **Slower Performance**: Compared to `confluent-kafka`, it is slower due to its pure Python nature.

---

## 3. Producer Methods

### Confluent-Kafka Producer (`confluent_kafka.Producer`)

- **`produce(topic, key=None, value=None, partition=None, on_delivery=None, timestamp=None, headers=None)`**
- **`flush(timeout=None)`**
- **`poll(timeout=0)`**
- **`init_transactions(timeout=30.0)`**
- **`begin_transaction()`**
- **`commit_transaction()`**
- **`abort_transaction()`**

### kafka-python Producer (`kafka.KafkaProducer`)

- **`send(topic, key=None, value=None, partition=None, timestamp_ms=None, headers=None)`**
- **`flush(timeout=None)`**
- **`close(timeout=None)`**

---

## 4. Consumer Methods

### Confluent-Kafka Consumer (`confluent_kafka.Consumer`)

- **`subscribe(topics, on_assign=None, on_revoke=None)`**
- **`poll(timeout=None)`**
- **`consume(num_messages=1, timeout=None)`**
- **`commit(offsets=None, asynchronous=False)`**
- **`close()`**

### kafka-python Consumer (`kafka.KafkaConsumer`)

- **`subscribe(topics)`**
- **`poll(timeout_ms=None)`**
- **`consume()`**
- **`commit()`**
- **`close()`**

---

## 1. Producer Methods

### 1.1 confluent-kafka Producer

Before using any producer methods, you need to create a `Producer` instance:

```python
from confluent_kafka import Producer

conf = {
    'bootstrap.servers': 'localhost:9092'  # Kafka broker address
}

producer = Producer(conf)
```

#### 1.1.1 `produce()`

**Definition:**

```python
produce(topic, key=None, value=None, partition=None, on_delivery=None, timestamp=None, headers=None)
```

- **Parameters:**
  - `topic` (str, required): Topic to send the message to.
  - `key` (bytes or str, optional): Key for message partitioning.
  - `value` (bytes or str, required): Message payload.
  - `partition` (int, optional): Explicit partition to send the message to.
  - `on_delivery` (callback, optional): Callback function when the message is delivered.
  - `timestamp` (int, optional): Message timestamp (default: broker-assigned).
  - `headers` (dict, optional): Headers for the message.

**Example:**

```python
def delivery_report(err, msg):
    if err:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

producer.produce("test_topic", key="key1", value="Hello Kafka!", on_delivery=delivery_report)
producer.flush()
```

#### 1.1.2 `flush()`

**Definition:**

```python
flush(timeout=None)
```

- **Parameters:**
  - `timeout` (float, optional): Max time to wait for messages to be delivered.

**Example:**

```python
producer.flush(10)  # Waits up to 10 seconds
```

#### 1.1.3 `poll()`

**Definition:**

```python
poll(timeout=0)
```

- **Parameters:**
  - `timeout` (float, optional): Time to wait for background events.

**Example:**

```python
producer.poll(0)
```

#### 1.1.4 `init_transactions()`

**Definition:**

```python
init_transactions(timeout=30.0)
```

- **Parameters:**
  - `timeout` (float, optional): Time to initialize transactions.

**Example:**

```python
producer.init_transactions(10.0)
```

#### 1.1.5 `begin_transaction()`

**Definition:**

```python
begin_transaction()
```

- **Description:** Starts a new transaction.

**Example:**

```python
producer.begin_transaction()
```

#### 1.1.6 `commit_transaction()`

**Definition:**

```python
commit_transaction()
```

- **Description:** Commits the current transaction.

**Example:**

```python
producer.commit_transaction()
```

#### 1.1.7 `abort_transaction()`

**Definition:**

```python
abort_transaction()
```

- **Description:** Aborts the current transaction.

**Example:**

```python
producer.abort_transaction()
```

---

### 1.2 kafka-python Producer

Before using any producer methods, you need to create a `KafkaProducer` instance:

```python
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    key_serializer=str.encode,
    value_serializer=str.encode
)
```

#### 1.2.1 `send()`

**Definition:**

```python
send(topic, key=None, value=None, partition=None, timestamp_ms=None, headers=None)
```

- **Parameters:**
  - `topic` (str, required): Topic to send the message to.
  - `key` (bytes, optional): Key for partitioning.
  - `value` (bytes, required): Message value.
  - `partition` (int, optional): Explicit partition.
  - `timestamp_ms` (int, optional): Timestamp in milliseconds.
  - `headers` (list of tuples, optional): Headers.

**Example:**

```python
future = producer.send("test_topic", key="key1", value="Hello Kafka!")
result = future.get(timeout=10)
print(result)
```

#### 1.2.2 `flush()`

**Definition:**

```python
flush(timeout=None)
```

- **Description:** Waits for all messages to be sent.

**Example:**

```python
producer.flush(10)
```

#### 1.2.3 `close()`

**Definition:**

```python
close(timeout=None)
```

- **Description:** Closes the producer.

**Example:**

```python
producer.close()
```

---
## 2. Consumer Methods

### 2.1 confluent-kafka Consumer

Before using any consumer methods, create a `Consumer` instance:

```python
from confluent_kafka import Consumer

conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'mygroup',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
```

#### 2.1.1 `subscribe()`

**Definition:**

```python
subscribe(topics, on_assign=None, on_revoke=None)
```

- **Parameters:**
  - `topics` (list, required): List of topics to subscribe to.
  - `on_assign` (callback, optional): Callback on partition assignment.
  - `on_revoke` (callback, optional): Callback on partition revocation.

**Example:**

```python
consumer.subscribe(["test_topic"])
```

#### 2.1.2 `poll()`

Fetches a single message.

**Example:**

```python
msg = consumer.poll(1.0)
if msg:
    print(f"Received: {msg.value().decode()}")
```

#### 2.1.3 `consume()`

Fetch multiple messages.

**Example:**

```python
messages = consumer.consume(num_messages=5, timeout=10)
for msg in messages:
    print(f"Received: {msg.value().decode()}")
```

#### 2.1.4 `commit()`

Commits the current offset.

**Example:**

```python
consumer.commit()
```

#### 2.1.5 `close()`

Closes the consumer.

**Example:**

```python
consumer.close()
```

---

### 2.2 kafka-python Consumer

Before using any consumer methods, create a `KafkaConsumer` instance:

```python
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'test_topic',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    group_id='mygroup'
)
```

#### 2.2.1 `subscribe()`

Subscribes to topics.

**Example:**

```python
consumer.subscribe(["test_topic"])
```

#### 2.2.2 `poll()`

Fetches messages.

**Example:**

```python
messages = consumer.poll(timeout_ms=1000)
```

#### 2.2.3 `commit()`

Commits offsets.

**Example:**

```python
consumer.commit()
```

#### 2.2.4 `close()`

Closes the consumer.

**Example:**

```python
consumer.close()
```

---


# Kafka Consumer Guide: `auto_offset_reset` Behavior

The `auto_offset_reset` configuration in **kafka-python** determines where a consumer starts reading messages when:

- There is no previously committed offset for the consumer group.
- The committed offset is invalid (e.g., messages were deleted due to Kafka's retention policy).

---

## 1. `auto_offset_reset="earliest"` (Start from the Beginning)

- **Behavior:**
  - If no committed offset exists, the consumer starts reading from the **first available message** in the partition.
  - Useful when you want to process **all historical messages** in the topic.
  - If offsets were committed, the consumer resumes from the **last committed offset**.

- **Example Scenario:**
  - Kafka topic `test_topic` has messages with offsets `[0,1,2,3,4]`.
  - A new consumer group (`mygroup`) starts consuming.
  - Since no offset is found, it starts from offset `0`.

- **Code Example:**

```python
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'test_topic',
    bootstrap_servers='localhost:9092',
    group_id='mygroup',
    auto_offset_reset='earliest'  # Read from beginning if no offset is found
)
```

---

## 2. `auto_offset_reset="latest"` (Start from New Messages)

- **Behavior:**
  - If no committed offset exists, the consumer starts reading **only new messages** (ignoring old messages).
  - Ideal for **real-time stream processing** when you don’t care about past messages.
  - If offsets were committed, the consumer resumes from the **last committed offset**.

- **Example Scenario:**
  - Kafka topic `test_topic` has messages `[0,1,2,3,4]`.
  - A new consumer group (`mygroup`) starts consuming.
  - Since no offset is found, it skips existing messages and waits for new messages.

- **Code Example:**

```python
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'test_topic',
    bootstrap_servers='localhost:9092',
    group_id='mygroup',
    auto_offset_reset='latest'  # Start reading only new messages
)
```

---

## 3. `auto_offset_reset="none"` (Throw an Error if No Offset Found)

- **Behavior:**
  - If there is no committed offset, the consumer will fail and raise an exception (`NoOffsetForPartitionError`).
  - Useful when you require a committed offset and don’t want to start from an arbitrary position.
  - Ensures that the consumer does not process messages unless offsets exist.

- **Example Scenario:**
  - Kafka topic `test_topic` has messages `[0,1,2,3,4]`.
  - A new consumer group (`mygroup`) starts consuming.
  - Since no offset is found, an error is thrown.

- **Code Example:**

```python
from kafka import KafkaConsumer
from kafka.errors import NoOffsetForPartitionError

consumer = KafkaConsumer(
    'test_topic',
    bootstrap_servers='localhost:9092',
    group_id='mygroup',
    auto_offset_reset='none'  # Raise error if no offset is found
)

# Handling the Error
try:
    for msg in consumer:
        print(msg.value.decode())
except NoOffsetForPartitionError:
    print("No offset found for this partition!")
```

---

## Comparison Table

| Setting        | Behavior                                     |
|----------------|----------------------------------------------|
| `"earliest"`   | Reads all past messages if no offset is found. |
| `"latest"`     | Reads only new messages if no offset is found. |
| `"none"`       | Throws an error if no offset is found.         |

---

# 🔧 Kafka CLI Tool Categories

## ✅ Basic Setup

All Kafka CLI tools are typically located in the `bin/` directory of your Kafka installation:

```bash
cd /path/to/kafka/bin
```

---

## 📜 Kafka CLI Commands

### 1. 🔄 Kafka Server Start & Stop

- **Start Zookeeper** (if not using KRaft):

```bash
bin/zookeeper-server-start.sh config/zookeeper.properties
```

- **Start Kafka Broker:**

```bash
bin/kafka-server-start.sh config/server.properties
```

- **Stop Kafka Broker:**

```bash
bin/kafka-server-stop.sh
```

- **Stop Zookeeper:**

```bash
bin/zookeeper-server-stop.sh
```

---

### 2. 📌 Topic Management

- **Create a Topic:**

```bash
bin/kafka-topics.sh --create \
  --topic my-topic \
  --bootstrap-server localhost:9092 \
  --partitions 3 \
  --replication-factor 1
```

- **List Topics:**

```bash
bin/kafka-topics.sh --list --bootstrap-server localhost:9092
```

- **Describe a Topic:**

```bash
bin/kafka-topics.sh --describe --topic my-topic --bootstrap-server localhost:9092
```

- **Delete a Topic:**

```bash
bin/kafka-topics.sh --delete --topic my-topic --bootstrap-server localhost:9092
```

---

### 3. 📨 Producer & Consumer CLI

- **Kafka Console Producer:**

```bash
bin/kafka-console-producer.sh \
  --broker-list localhost:9092 \
  --topic my-topic
```

  - Type messages and press Enter to send.

- **Kafka Console Consumer:**

```bash
bin/kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic my-topic \
  --from-beginning
```

---

### 4. 👥 Consumer Group Management

- **List Consumer Groups:**

```bash
bin/kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --list
```

- **Describe a Consumer Group:**

```bash
bin/kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --describe --group my-group
```

- **Reset Offsets:**

```bash
bin/kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --group my-group \
  --topic my-topic \
  --reset-offsets --to-earliest --execute
```

---

### 5. 📦 Managing Kafka Partitions

- **Add Partitions to a Topic:**

```bash
bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --alter --topic my-topic \
  --partitions 6
```

---

### 6. 📤 Kafka Data Dump & Import

- **Dump Topic to File:**

```bash
bin/kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic my-topic \
  --from-beginning > output.txt
```

- **Load File to Topic:**

```bash
bin/kafka-console-producer.sh \
  --broker-list localhost:9092 \
  --topic my-topic < input.txt
```

---

### 7. 🧪 Kafka Performance Tools

- **Producer Performance Test:**

```bash
bin/kafka-producer-perf-test.sh \
  --topic test-topic \
  --num-records 100000 \
  --record-size 100 \
  --throughput -1 \
  --producer-props bootstrap.servers=localhost:9092
```

- **Consumer Performance Test:**

```bash
bin/kafka-consumer-perf-test.sh \
  --broker-list localhost:9092 \
  --topic test-topic \
  --messages 100000 \
  --threads 1 \
  --group test-group
```

---

### 8. 🧾 Kafka Configuration CLI (KRaft Mode)

- **Create/Update Configuration:**

```bash
bin/kafka-configs.sh \
  --bootstrap-server localhost:9092 \
  --entity-type topics \
  --entity-name my-topic \
  --alter --add-config retention.ms=60000
```

- **Describe Configuration:**

```bash
bin/kafka-configs.sh \
  --bootstrap-server localhost:9092 \
  --entity-type topics \
  --entity-name my-topic \
  --describe
```

---

### 9. 🛠️ Kafka Utilities

- **Check Offsets of Topic Partitions:**

```bash
bin/kafka-run-class.sh kafka.tools.GetOffsetShell \
  --broker-list localhost:9092 \
  --topic my-topic \
  --time -1
```

---

## ⚙️ CLI Help Command

Use `--help` with any command for all available flags and options:

```bash
bin/kafka-topics.sh --help
```

---
# 🔧 Kafka CLI Tool Categories

## ✅ Basic Setup

All Kafka CLI tools are typically located in the `bin/` directory of your Kafka installation:

```bash
cd /path/to/kafka/bin
```

---

## 📜 Kafka CLI Commands

### 1. 🔄 Kafka Server Start & Stop

- **Start Zookeeper** (if not using KRaft):

```bash
bin/zookeeper-server-start.sh config/zookeeper.properties
```

- **Start Kafka Broker:**

```bash
bin/kafka-server-start.sh config/server.properties
```

- **Stop Kafka Broker:**

```bash
bin/kafka-server-stop.sh
```

- **Stop Zookeeper:**

```bash
bin/zookeeper-server-stop.sh
```

---

### 2. 📌 Topic Management

- **Create a Topic:**

```bash
bin/kafka-topics.sh --create \
  --topic my-topic \
  --bootstrap-server localhost:9092 \
  --partitions 3 \
  --replication-factor 1
```

- **List Topics:**

```bash
bin/kafka-topics.sh --list --bootstrap-server localhost:9092
```

- **Describe a Topic:**

```bash
bin/kafka-topics.sh --describe --topic my-topic --bootstrap-server localhost:9092
```

- **Delete a Topic:**

```bash
bin/kafka-topics.sh --delete --topic my-topic --bootstrap-server localhost:9092
```

---

### 3. 📨 Producer & Consumer CLI

- **Kafka Console Producer:**

```bash
bin/kafka-console-producer.sh \
  --broker-list localhost:9092 \
  --topic my-topic
```

  - Type messages and press Enter to send.

- **Kafka Console Consumer:**

```bash
bin/kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic my-topic \
  --from-beginning
```

---

### 4. 👥 Consumer Group Management

- **List Consumer Groups:**

```bash
bin/kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --list
```

- **Describe a Consumer Group:**

```bash
bin/kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --describe --group my-group
```

- **Reset Offsets:**

```bash
bin/kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --group my-group \
  --topic my-topic \
  --reset-offsets --to-earliest --execute
```

---

### 5. 📦 Managing Kafka Partitions

- **Add Partitions to a Topic:**

```bash
bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --alter --topic my-topic \
  --partitions 6
```

---

### 6. 📤 Kafka Data Dump & Import

- **Dump Topic to File:**

```bash
bin/kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic my-topic \
  --from-beginning > output.txt
```

- **Load File to Topic:**

```bash
bin/kafka-console-producer.sh \
  --broker-list localhost:9092 \
  --topic my-topic < input.txt
```

---

### 7. 🧪 Kafka Performance Tools

- **Producer Performance Test:**

```bash
bin/kafka-producer-perf-test.sh \
  --topic test-topic \
  --num-records 100000 \
  --record-size 100 \
  --throughput -1 \
  --producer-props bootstrap.servers=localhost:9092
```

- **Consumer Performance Test:**

```bash
bin/kafka-consumer-perf-test.sh \
  --broker-list localhost:9092 \
  --topic test-topic \
  --messages 100000 \
  --threads 1 \
  --group test-group
```

---

### 8. 🧾 Kafka Configuration CLI (KRaft Mode)

- **Create/Update Configuration:**

```bash
bin/kafka-configs.sh \
  --bootstrap-server localhost:9092 \
  --entity-type topics \
  --entity-name my-topic \
  --alter --add-config retention.ms=60000
```

- **Describe Configuration:**

```bash
bin/kafka-configs.sh \
  --bootstrap-server localhost:9092 \
  --entity-type topics \
  --entity-name my-topic \
  --describe
```

---

### 9. 🔐 Security & ACL Management

- **Add ACLs:**

```bash
bin/kafka-acls.sh \
  --authorizer-properties zookeeper.connect=localhost:2181 \
  --add --allow-principal User:alice \
  --operation Read --topic my-topic
```

- **List ACLs:**

```bash
bin/kafka-acls.sh \
  --authorizer-properties zookeeper.connect=localhost:2181 \
  --list
```

- **Remove ACLs:**

```bash
bin/kafka-acls.sh \
  --authorizer-properties zookeeper.connect=localhost:2181 \
  --remove --allow-principal User:alice \
  --operation Read --topic my-topic
```

---

### 10. 🔧 Replication & Partition Tooling

- **Replica Reassignment (deprecated in newer Kafka):**

```bash
bin/kafka-reassign-partitions.sh \
  --zookeeper localhost:2181 \
  --reassignment-json-file reassignment.json \
  --execute
```

- **Partition Reassignment Tool (KRaft mode):**

```bash
bin/kafka-reassign-partitions.sh \
  --bootstrap-server localhost:9092 \
  --reassignment-json-file reassignment.json \
  --execute
```

---

### 11. 🧱 Kafka Storage Tool (KRaft Mode Only)

- **Format Log Directory:**

```bash
bin/kafka-storage.sh format \
  -t <uuid> \
  -c config/kraft-server.properties
```

---

### 12. 🧭 Metadata Quorum Tools (KRaft Only)

- **Check Metadata Quorum Status:**

```bash
bin/kafka-metadata-quorum.sh \
  --bootstrap-server localhost:9092 \
  --describe
```

---

### 13. 🛑 Broker Shutdown Tool (for KRaft)

- **Trigger Broker Shutdown:**

```bash
bin/kafka-leader-election.sh \
  --bootstrap-server localhost:9092 \
  --election-type PREFERRED \
  --topic my-topic
```

---

## ⚙️ CLI Help Command

Use `--help` with any command for all available flags and options:

```bash
bin/kafka-topics.sh --help
```

---

# Choosing Between Kafka Libraries: `confluent-kafka` vs `kafka-python`

This document compares the features of two popular Kafka libraries for Python: **`confluent-kafka`** and **`kafka-python`**, to help you choose the right library for your use case.

---

## **Feature Comparison**

| **Feature**             | **confluent-kafka**         | **kafka-python**          |
|--------------------------|-----------------------------|---------------------------|
| **Performance**          | High (C-backed)            | Moderate (pure Python)    |
| **Complexity**           | Moderate                   | Simple                    |
| **Production Readiness** | High                       | Medium                    |
| **Transaction Support**  | Yes                        | No                        |
| **Async I/O**            | No                         | Yes (with asyncio)        |
| **Rebalancing Callbacks**| Yes                        | Yes                       |
| **Delivery Guarantees**  | Exactly-once (with config) | At-least-once             |

---

## **Key Takeaways**

- **Use `confluent-kafka`** if:
  - You require **high performance** (e.g., for large-scale production systems).
  - You need **transaction support**.
  - You want **exactly-once delivery guarantees**.
  - You prioritize **production readiness**.

- **Use `kafka-python`** if:
  - You prefer a **simpler API** for quick prototyping.
  - You need **async I/O** support (e.g., for integration with `asyncio`).

Remember that the choice largely depends on your application's requirements and complexity.

---
