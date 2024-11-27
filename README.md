# Quickstart instructions

## API Keys 
| API Keys                  | Documentation       |
|---------------------------|----------------------|
| **OpenWeatherMap API**    |    https://openweathermap.org/api       |
| **Faker API**             | https://faker.readthedocs.io/en/master  |
| **Codeforces API**        | https://codeforces.com/apiHelp          |

You need to apply for some APIs to use with this. The APIs might take days for application to be granted access. Sample API keys are given, but it can be blocked if too many users are running this.

To use the **OpenWeatherMap API**, please go the website, obtain the API key and  update the file "owm-producer/openweathermap_service.cfg".

## Create docker networks
```bash
$ docker network create kafka-network                         # create a new docker network for kafka cluster (zookeeper, broker, kafka-manager services, and kafka connect sink services)
$ docker network create cassandra-network                     # create a new docker network for cassandra. (kafka connect will exist on this network as well in addition to kafka-network)
```
## Starting Cassandra

Cassandra is setup so it runs keyspace and schema creation scripts at first setup so it is ready to use.
```bash
$ docker-compose -f cassandra/docker-compose.yml up -d
```

## Starting Kafka on Docker
```bash
$ docker-compose -f kafka/docker-compose.yml up -d            # start single zookeeper, broker, kafka-manager and kafka-connect services
$ docker ps -a                                                # sanity check to make sure services are up: kafka_broker_1, kafka-manager, zookeeper, kafka-connect service
```

> **Note:** 
Kafka-Manager front end is available at http://localhost:9000

You can use it to create cluster to view the topics streaming in Kafka.


**IMPORTANT**: To start the cassandra sinks, manually go the CLI of the "kafka-connect" container and run the below comment:
```
./start-and-wait.sh
```

## Starting Producers
```bash
$ docker-compose -f owm-producer/docker-compose.yml up -d     # start the producer that retrieves open weather map
$ docker-compose -f faker-producer/docker-compose.yml up -d # start the producer for faker
$ docker-compose -f codeforces-producer/docker-compose.yml up -d # start the producer for codeforces
```

## Starting Consumers (optional)

The consumers container is used to consume the data produced by the producers and write it to Cassandra. You can check if the producer is working by checking the logs of the consumer container. 

```bash
$ docker-compose -f consumer/docker-compose.yml up -d         # start the consumer
```

## Check that data is arriving to Cassandra

First login into Cassandra's container with the following command or open a new CLI from Docker Desktop if you use that.
```bash
$ docker exec -it cassandra bash
```
Once loged in, bring up cqlsh with this command and query weatherreport, fakerdata and codeforcesdata tables like this:
```bash
$ cqlsh --cqlversion=3.4.4 127.0.0.1 #make sure you use the correct cqlversion

cqlsh> use kafkapipeline; #keyspace name

cqlsh:kafkapipeline> select * from fakerdata;

cqlsh:kafkapipeline> select * from weatherreport;

cqlsh:kafkapipeline> select * from codeforcesdata;
```

And that's it! you should be seeing records coming in to Cassandra. 

## Codeforces API (Task 3)

The Codeforces API is a RESTful API that allows users to access data from the Codeforces platform. The API provides access to data such as user information, contest information, user rating, ranks, and problem information. The API is free to use and does not require an API key.

For more information on the Codeforces API, please refer to the official documentation: https://codeforces.com/apiHelp

## Visualization

Run the following command the go to http://localhost:8888 and run the visualization notebook accordingly

```
docker-compose -f data-vis/docker-compose.yml up -d
```

**Note**: When log in the at the fist time, the jupyter notebook might require a token to log in. The token is `EEET2574` which is configured in the `--NotebookApp.token` variable in the `data-vis/Dockerfile` file.

Once logged in, getting the data from weatherreport, fakerdata and codeforcesdata tables with these commands:
```bash
weather = getWeatherDF() # Get the weather data
 
faker = getFakerDF() # Get the faker data

codeforces = getCodeforcesDF() # Get the codeforces data
```

Below are some examples of the weather, faker and codeforces data:


