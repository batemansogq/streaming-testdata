# Purpose: Produces test data set, based upon the config file, producing JSON messages onto Kafka topics
# Instructions: Modify the configuration.ini file to meet your requirements.

import configparser
import json
import random
import time
from datetime import datetime

from faker import Faker

from kafka import KafkaProducer
from config.kafka import get_configs

config = configparser.ConfigParser()
config.read("configuration/configuration.ini")


# *** CONFIGURATION ***
topic_testdata = config["KAFKA"]["topic_testdata"]

min_freq = int(config["STREAM"]["min_freq"])
max_freq = int(config["STREAM"]["max_freq"])
number_of_txt = int(config["STREAM"]["number_of_txt"])

print(min_freq, max_freq, number_of_txt)

# *** VARIABLES ***
LoginPayload = {}

class LoginData:

    def __init__(self):
        fake = Faker()
        self.password = "password@123"
        self.email = fake.email()
        self.username = fake.first_name()
        self.first_name = fake.first_name()
        self.last_name = fake.last_name()
        self.phone = random.randint(9000000000, 9999999999)
        self.city = fake.city()
        self.about = "This is a sample text"
        self.event_time = str(datetime.utcnow())

    def __str__(self):
        return (
            "password: {0}, email: {1}, username: {2}, first_name: {3}, "
            "last_name {4}, phone: {5}, city: {6}, about: {7}, "
            "event_time: {8}".format(
                self.password,
                self.email,
                self.first_name,
                self.first_name,
                self.last_name,
                self.phone,
                self.city,
                self.about,
                self.event_time,
            )
        )


def main():
    input_data()

# create the individual json payload a number of times and publish to kafka
def input_data():
    for i in range(0, number_of_txt):
        LoginDetail = LoginData()
      #  print(LoginDetail)
      #  LoginPayload.append(LoginDetail)
       # print(type(LoginPayload))
       # publish_to_kafka(topic_testdata, LoginPayload)
#delay for a period
    time.sleep(random.randint(min_freq, max_freq))


# serialize object to json and publish message to kafka topic
def publish_to_kafka(topic, message):
    configs = get_configs()

    producer = KafkaProducer(
        value_serializer=lambda v: json.dumps(vars(v)).encode("utf-8"),
        **configs,
    )
    producer.send(topic, value=message)
    print("Topic: {0}, Value: {1}".format(topic, message))


if __name__ == "__main__":
    main()
