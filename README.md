# Menu API Demo

## Summary

This is a demonstration of API design for restaurant application. It uses `ElasticSearch` as the data store and `FastAPI/uvicorn` as the API server.


## Prerequisites
The below is the settings for development/testing environment.
* Linux or Windows WSL2
* Git
* Python 3.10
* Docker 23.0.5, 20.10.23
* Docker Compose v2.17.3, v2.19.0
  
## Quick Start

Using docker compose is the fastest way to start the application (Be sure that ports 8000 and 9200 are not used by other processes).

```shell
    $ git clone https://github.com/bochen0909/menu-api-demo.git
    $ cd menu-api-demo
```
All the following commands are assumed to run under `menu-api-demo` folder.

Build the image
```shell
    $ docker build -f dockerfile/Dockerfile -t menuapidemo:latest dockerfile
    $ docker image list menuapidemo
    REPOSITORY    TAG       IMAGE ID       CREATED        SIZE
    menuapidemo   latest    e46ed4b862a8   17 hours ago   1.08GB

```
Start the application
```shell
    $ docker compose up
```

When it shows
```
menu-api-demo-api-1            | INFO:     Started server process [8]
menu-api-demo-api-1            | INFO:     Waiting for application startup.
menu-api-demo-api-1            | INFO:     Application startup complete.
menu-api-demo-api-1            | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

open [Swagger UI](http://127.0.0.1:8000/docs) to test the APIs,

or alternatively to call it from command line. 

For example, find the top 3 restaurants that service coffee.

```shell
    $ curl http://127.0.0.1:8000/v1/food/coffee?limit=3
    [{"id":"1364","score":2.8030283},{"id":"3677","score":1.9024392},{"id":"6022","score":1.9024392}]
```

Find the menu URL by id.

```shell
    $ curl http://127.0.0.1:8000/v1/restaurant/1364
    {"id":"1364","name":"REVIVE CLUB & CAFE","city":"CICERO","state":"IL","menu_url":"https://reviveclubandcafe.com/"}
```
Cleanup
```shell
    $ docker compose down  # be sure in project root folder

```
## Manually (step by step)

### Clone the code 
```shell
    $ git clone https://github.com/bochen0909/menu-api-demo.git
    $ cd menu-api-demo
```
All the following commands are assumed to run under `menu-api-demo` folder.

### Build the image
```shell
    $ docker build -f dockerfile/Dockerfile -t menuapidemo:latest dockerfile
    $ docker image list menuapidemo
    REPOSITORY    TAG       IMAGE ID       CREATED        SIZE
    menuapidemo   latest    e46ed4b862a8   17 hours ago   1.08GB

```
### Create a new network
```shell
    $ docker network create menudemo
    $ docker network list  | grep menudemo
    4707dbcee347   menudemo   bridge    local
``` 
### Start Elasticsearch instance
```shell
    $ docker run -p 9200:9200  -e "discovery.type=single-node"  -e "xpack.security.enabled=false"  -it --rm  --name es01 --net=menudemo  docker.elastic.co/elasticsearch/elasticsearch:8.8.1
    $ docker container list -f name=es01
    CONTAINER ID   IMAGE                                                 COMMAND                  CREATED         STATUS         PORTS                              NAMES
9de65331d4e1   docker.elastic.co/elasticsearch/elasticsearch:8.8.1   "/bin/tini -- /usr/l…"   6 minutes ago   Up 6 minutes   0.0.0.0:9200->9200/tcp, 9300/tcp   es01
```
Here security is disabled so that there is no needs to handle user/password and http certificate authentication. Be aware that it is not applicable to a production environment.

### Populate sample data
```shell
    $ docker run -v `pwd`/data/restaurants:/data --network menudemo -it --rm  menuapidemo load_data_elasticsearch.py /data
    2023-06-28 14:41:22,759 [INFO] Loading 20 files from '/data'.
    2023-06-28 14:41:23,104 [INFO] HEAD http://es01:9200/ [status:200 duration:0.042s]
    2023-06-28 14:41:23,410 [INFO] PUT http://es01:9200/_bulk [status:200 duration:0.305s]
```
It loaded all json files from `data/restaurants` folder to elastic search instance.

### Start the API instance
```shell
    $ docker run  -p 8000:8000 --network menudemo --name api   -it --rm  menuapidemo
    INFO:     Started server process [7]
    INFO:     Waiting for application startup.
    INFO:     Application startup complete.
    INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

Now the whole application is up. See [Quick Start]($quick-start) for examples to call the API's. 

### Cleanup

```shell
    $ docker stop container api
    $ docker stop container es01
    $ docker network remove menudemo
```

## Design

When developing a demonstration application, there are several options to consider:

- Load data in memory.
- Load data into a database.
- Single Node vs Multi Nodes.
- ...

For scalability and large deployments, it is recommended to separate the data storage and API services. This separation allows for better management and flexibility in scaling the application.

The API of the application needs to perform text data searching. While traditional databases have the ability to handle text matching, tools like Lucene or Elasticsearch offer more versatility and robustness in terms of search functions.

Taking into account the scalability and efficient search requirements, the final design choice is to use FastAPI for developing the APIs, while leveraging Elasticsearch as the data store.

By implementing this design, the application can benefit from the powerful searching capabilities of Elasticsearch while enjoying the high-performance and user-friendly development experience provided by FastAPI.

## Development

### Clone the code 
```shell
    $ git clone https://github.com/bochen0909/menu-api-demo.git
    $ cd menu-api-demo
```
All the following commands are assumed to run under `menu-api-demo` folder.

### Create a Virtual Environment
```shell
    $ python -m venv .venv
    $ source .venv/bin/activate
```
Alternativly use `conda` to create an environment.

### Install required libs
```shell
    $ pip install -r requirements.txt
```

### Start an Elasticsearch instance (might take a few time)
```shell
    $ docker run -p 9200:9200  -e "discovery.type=single-node"  -e "xpack.security.enabled=false"  -it --rm  --name es01 docker.elastic.co/elasticsearch/elasticsearch:8.8.1
```
### Populate sample data
```shell
    $ python scripts/load_data_elasticsearch.py data/restaurants/ http://localhost:9200 
```

### Start `uvicorn` instance
```shell
    $ ES_ENDPOINT=http://localhost:9200 PYTHONPATH=`pwd`/src uvicorn app.main:app --reload
```

Now use your favorite IDE to open the project.

