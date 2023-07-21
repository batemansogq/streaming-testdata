# Purpose: Consumes all messages from Kafka topic for testing purposes
# set to single testdata topic

import configparser
import json

from kafka import KafkaConsumer

from config.kafka import get_configs

config = configparser.ConfigParser()
config.read("configuration/configuration.ini")

# *** CONFIGURATION ***
topic_testdata = config["KAFKA"]["topic_testdata"]

def main():
    consume_messages()

def consume_messages():
    configs = get_configs()

    consumer = KafkaConsumer(
        topic_testdata,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        auto_offset_reset="earliest",
        **configs
    )

 
    for message in consumer:
        print(message.value) 

if __name__ == "__main__":
    main()
