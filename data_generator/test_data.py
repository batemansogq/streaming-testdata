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


class LoginData:
    def __init__(
            self, 
            password: str, 
            email: str,
            username: str,
            first_name: str,
            last_name: str,
            phone: float,
            city: str,
            about: str,
            event_time: str,
            cc_num: str,
    ):
        self.password = str(password)
        self.email = str(email)
        self.username = str(first_name)
        self.first_name = str(first_name)
        self.last_name = str(last_name)
        self.phone = float(phone)
        self.city = str(city)
        self.about = str(about)
        self.event_time = str(event_time)
        self.cc_num = str(cc_num)

    def __str__(self):
        return (
            "password: {0}, email: {1}, username: {2}, first_name: {3}, "
            "last_name {4}, phone: {5}, city: {6}, about: {7}, "
            "event_time: {8}, cc_num: {9}".format(
                self.password,
                self.email,
                self.first_name,
                self.first_name,
                self.last_name,
                self.phone,
                self.city,
                self.about,
                self.event_time,
                self.cc_num,
            )
        )


def main():
    input_data()

# create the individual json payload a number of times and publish to kafka
def input_data():
    for i in range(0, number_of_txt):
    # define/clear payload
        LoginPayload = []
    #load faker
        fake = Faker()
    #use faker to generate data
        LoginDetail = LoginData(
            "password@123",
            fake.email(),
            fake.first_name(),
            fake.first_name(),
            fake.last_name(),
            random.randint(9000000000, 9999999999),
            fake.city(),
            "This is a sample text",
            str(datetime.utcnow()),
            fake.credit_card_number(),
        )
        LoginPayload.append(LoginDetail)
    #publish record to kafka
        publish_to_kafka(topic_testdata, LoginPayload[0])

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
