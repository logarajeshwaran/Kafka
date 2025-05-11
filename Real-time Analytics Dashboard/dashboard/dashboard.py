################################################################################
# Script Name: dashboard.py
# Description: This script reads Kafka event data from a JSON file and generates
#              a chart showing the distribution of user actions.
# Author: logarajeshwaran
# Created Date: 2025-04-21
# License: MIT License
################################################################################

import json
import matplotlib.pyplot as plt
from collections import Counter

# Path to the JSON file containing Kafka events
json_file_path = "/home/kafka/kafka-work/Real-time Analytics Dashboard/images/user_events_output.json"

# Load the JSON data
with open(json_file_path, "r") as f:
    events = json.load(f)

# Extract actions from the events
actions = [event["action"] for event in events]

# Count the occurrences of each action
action_counts = Counter(actions)

# Prepare data for the chart
actions = list(action_counts.keys())
counts = list(action_counts.values())

# Generate a bar chart
plt.figure(figsize=(10, 6))
plt.bar(actions, counts, color='skyblue')
plt.title("Distribution of User Actions")
plt.xlabel("Actions")
plt.ylabel("Counts")
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Save the chart as a PNG image
output_image_path = "/home/kafka/kafka-work/Real-time Analytics Dashboard/images/user_actions_distribution.png"
plt.savefig(output_image_path)
print(f"Chart saved as {output_image_path}")

# Show the chart
plt.show()