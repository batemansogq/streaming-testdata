This repo is subset of the "Streaming Synthetic Sales Data Generator" by [Gary Stafford](https://github.com/garystafford/streaming-sales-generator/blob/main/docker/spark-kstreams-stack.yml).

it takes the basic streaming elements and extends it using [Faker](https://pypi.org/project/Faker/) to create configurable test data payloads in JSON format. 

## TL;DR

Deploy Kafka
1. `docker stack deploy stream --compose-file docker/kafka-stack.yml` to create local instance of Kafka
Run the Test data creation scripts
2. `python -m pip install kafka-python` to install the `kafka-python` package
4. `python ./data_generator/test_data.py` to start generating streaming data to Apache Kafka
5. `python3 ./consumer.py` in a separate terminal window to view results

## Background

This is a intended to be a simple generator for streaming testdata, produced via Kafka endpoint.


## Docker Kafka Stack

```shell
# optional: delete previous stack
docker stack rm stream

# deploy kafka stack
docker swarm init
docker stack deploy stream --compose-file docker/kafka-stack.yml

# view results
docker ps

# stop service and remove stream
docker stack rm stream

```
### Containers

After a couple of mins, you will see the following containers:

```text
CONTAINER ID   IMAGE                                      PORTS                                    NAMES
6114dc4a9824   bitnami/kafka:3.2.1                        9092/tcp                                 stream_kafka.1...
837c0cdd1498   bitnami/zookeeper:3.8.0                    2181/tcp, 2888/tcp, 3888/tcp, 8080/tcp   stream_zookeeper.1...
eb9bfea05dd8   provectuslabs/kafka-ui                     8080/tcp                                 stream_kafka-ui
```

## Helpful Commands

To run the application:

```shell
# install `kafka-python` python package
python -m pip install kafka-python

cd data_generator/

# run in foreground
python ./test_data.py
# alternately, run as background process
nohup python ./test_data.py &
```

Manage the topics from within the Kafka container:

```shell
docker exec -it $(docker container ls --filter  name=stream_kafka.1 --format "{{.ID}}") bash

export BOOTSTRAP_SERVERS="localhost:9092"
export TOPIC_PRODUCTS="demo.products"
export TOPIC_TESTDATA="demo.testdata"


# list topics
kafka-topics.sh --list \
    --bootstrap-server $BOOTSTRAP_SERVERS

# describe topic
kafka-topics.sh --describe \
    --topic $TOPIC_PURCHASES \
    --bootstrap-server $BOOTSTRAP_SERVERS

# list consumer groups
kafka-consumer-groups.sh --list \
    --bootstrap-server $BOOTSTRAP_SERVERS
  
# delete topics
kafka-topics.sh --bootstrap-server $BOOTSTRAP_SERVERS --delete --topic $TOPIC_PRODUCTS
kafka-topics.sh --bootstrap-server $BOOTSTRAP_SERVERS --delete --topic $TOPIC_TESTDATA


# optional: create partitions (or will be automatically created)
kafka-topics.sh --create --topic $TOPIC_PRODUCTS \
    --partitions 1 --replication-factor 1 \
    --config cleanup.policy=compact \
    --bootstrap-server $BOOTSTRAP_SERVERS

kafka-topics.sh --create --topic $TOPIC_TESTDATA \
    --partitions 1 --replication-factor 1 \
    --config cleanup.policy=compact \
    --bootstrap-server $BOOTSTRAP_SERVERS

# read topics from beginning
kafka-console-consumer.sh \
    --topic $TOPIC_PRODUCTS --from-beginning \
    --bootstrap-server $BOOTSTRAP_SERVERS

kafka-console-consumer.sh \
    --topic $TOPIC_TESTDATA --from-beginning \
    --bootstrap-server $BOOTSTRAP_SERVERS


```


