# How run the service
### Run in docker (it avoids problems with dependencies/pyenvbut e.g. on MacOS docker can be really slow and load all CPU)
Prerequisites: 
1. docker and docker-compose is installed (see https://docs.docker.com/engine/install/, https://docs.docker.com/compose/install/)
2. docker daemon is running
3. ```git clone git@github.com:Dinara301/canonical.git```
4. ```cd ./canonical/```

Run 
```
docker-compose build && docker-compose up
```



### Run in python environment
Prerequisites:
1. python3.9
2. mongod

Depending on OS you need to have one 
```
cd ./canonical/
pip install virtualenv
python3 -m venv canonicalenv
source canonicalenv/bin/activate
pip install -r requirements.txt
# Start mongodb 
mkdir /tmp/dblocal/
mongod --dbpath /tmp/dblocal/ 
# start server
export DATABASE_URL="mongodb://127.0.0.1:27017"
uvicorn src.main:app --reload
```

# Testing
1. In browser on address http://0.0.0.0:8000/docs  FastAPI will create OpenAPI documentaion
2. You can try out request there (click "Try it out")

### Another option
1. example_requests.sh

# Design overview 

Implemented service is an MVP.

Further I'll describe a better design for this use-case that requires more resources and time to implement.

There're few services available on the market that can cover this use-case, eg Splunk. If there're any specific 
requirements/cost concerns similar custom service can be implemented.

### Assumptions
1. There're many different business services that write audit logs, high-load logger service needed
2. Fully ready market solutions are not used 

### Main points to consider
1. #### Throughput, reliability
Log aggregation is needed, it can be agent on business services themselves or intermediate log aggregator service (like the current one - but with balancer).
In any case pub-sub system should be used as a queue for all incoming logs (e.g. Kafka)
2. #### Easy search over database 
Current solution uses MongoDB, but it's not the best choice. ElasticSearch or similar 
solutions can be used to store and retrieve logs.
3. #### Data amount 
Archiving of data is needed, audit logs are important and should be stored 
for a long time, for this case archived storages can be used (e.g. AWS S3 Glacier)
