# This repo is subset of the "Streaming Synthetic Sales Data Generator" by [Gary Stafford](https://github.com/garystafford/streaming-sales-generator/blob/main/docker/spark-kstreams-stack.yml)
# it takes the basic streaming elements and extends it using [Faker](https://pypi.org/project/Faker/)  

## TL;DR

1. `docker stack deploy streaming-stack --compose-file docker/spark-kafka-stack.yml` to create local instance of Kafka
2. `python3 -m pip install kafka-python` to install the `kafka-python` package
3. `cd sales_generator/`
4. `python3 ./producer.py` to start generating streaming data to Apache Kafka
5. `python3 ./consumer.py` in a separate terminal window to view results

## Background

This is a intended to be a simple generator for streaming testdata, produced via Kafka endpoint



## Docker Kafka Stack

```shell
# optional: delete previous stack
docker stack rm streaming-stack

# deploy kafka stack
docker swarm init
docker stack deploy streaming-stack --compose-file docker/spark-kstreams-stack.yml

# view results
docker stats

docker container ls --format "{{ .Names}}, {{ .Status}}"
```

### Containers

Example Apache Kafka, Zookeeper, Spark, Flink, Pinot, Superset, KStreams, and JupyterLab containers:

```text
CONTAINER ID   IMAGE                      PORTS                                    NAMES
8edd2caf765d   garystafford/kstreams-kafka-demo:0.7.0                              streaming-stack_kstreams.1...
1d7c6ab3009d   bitnami/spark:3.3                                                   streaming-stack_spark...
1d7c6ab3009d   bitnami/spark:3.3                                                   streaming-stack_spark-worker...
6114dc4a9824   bitnami/kafka:3.2.1        9092/tcp                                 streaming-stack_kafka.1...
837c0cdd1498   bitnami/zookeeper:3.8.0    2181/tcp, 2888/tcp, 3888/tcp, 8080/tcp   streaming-stack_zookeeper.1...

```

## Helpful Commands

To run the application:

```shell
# install `kafka-python` python package
python3 -m pip install kafka-python

cd sales_generator/

# run in foreground
python3 ./producer.py
# alternately, run as background process
nohup python3 ./producer.py &
```

Manage the topics from within the Kafka container:

```shell
docker exec -it $(docker container ls --filter  name=streaming-stack_kafka.1 --format "{{.ID}}") bash

export BOOTSTRAP_SERVERS="localhost:9092"
export TOPIC_PRODUCTS="demo.products"
export TOPIC_PURCHASES="demo.purchases"
export TOPIC_INVENTORIES="demo.inventories"

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
kafka-topics.sh --bootstrap-server $BOOTSTRAP_SERVERS --delete --topic $TOPIC_PURCHASES
kafka-topics.sh --bootstrap-server $BOOTSTRAP_SERVERS --delete --topic $TOPIC_INVENTORIES

# optional: create partitions (or will be automatically created)
kafka-topics.sh --create --topic $TOPIC_PRODUCTS \
    --partitions 1 --replication-factor 1 \
    --config cleanup.policy=compact \
    --bootstrap-server $BOOTSTRAP_SERVERS

kafka-topics.sh --create --topic $TOPIC_PURCHASES \
    --partitions 1 --replication-factor 1 \
    --config cleanup.policy=compact \
    --bootstrap-server $BOOTSTRAP_SERVERS

kafka-topics.sh --create --topic $TOPIC_INVENTORIES \
    --partitions 1 --replication-factor 1 \
    --config cleanup.policy=compact \
    --bootstrap-server $BOOTSTRAP_SERVERS

# read topics from beginning
kafka-console-consumer.sh \
    --topic $TOPIC_PRODUCTS --from-beginning \
    --bootstrap-server $BOOTSTRAP_SERVERS

kafka-console-consumer.sh \
    --topic $TOPIC_PURCHASES --from-beginning \
    --bootstrap-server $BOOTSTRAP_SERVERS

kafka-console-consumer.sh \
    --topic $TOPIC_INVENTORIES --from-beginning \
    --bootstrap-server $BOOTSTRAP_SERVERS
```


