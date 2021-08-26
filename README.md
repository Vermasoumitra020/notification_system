# Notification System

Notification Service to handle group and personalized notifications supporting multiple providers.

## Documentation

### Services

- **Notification Gateway** 
  - Serves notifications to Kafka(Message Queue) for asynchronous notification handeling.
  - Provides initial basic validations to the requests being forwarded.
  
  [Read more](https://github.com/Vermasoumitra020/notification_system/blob/master/notification_gateway/README.md)
 
- **Notification Validator**
  - Pulls the notification from kafka and gets the user realted informations necessary for sending notifications.
  - Schedules the notifications and pushes the notifications to kafka.
  
  [Read more](https://github.com/Vermasoumitra020/notification_system/blob/master/notification_validator/README.md)
  
- **Notification Data Handler**
  - Exposes APIs to register, subscrbe and fetch users and subscription details.
  
  [Read more](https://github.com/Vermasoumitra020/notification_system/blob/master/notification_data_handler/README.md)
  
- **Provider Handler**
  - Pulls the notifications from the different topics in kafka and sends it to different provider handlers.
  
  [Read more](https://github.com/Vermasoumitra020/notification_system/blob/master/provider_handler/README.md)
  
- **Kafka Docker**
  - Docker compose file for kafka settings.
  
  [Read more](https://github.com/Vermasoumitra020/notification_system/blob/master/kafka_docker)
  


## Diagrams

### Architecture

![Architectural diagram](https://github.com/Vermasoumitra020/notification_system/blob/master/diagrams/Notification%20Service%20V1.jpg)

### Sequence

![Sequence diagram](https://github.com/Vermasoumitra020/notification_system/blob/master/diagrams/Sequence%20Diagram%20V1.jpg)


## How to Run

### Settings Changes

- **Kafka**
  - Please update the `KAFKA_ADVERTISED_LISTENERS` outside host to `OUTSIDE://<HOST IP>:9092` (for both the kafka).

- **Other Services**
  - Please udate the `BOOTSTRAP_SERVERS_CONSUMER` (if present), `BOOTSTRAP_SERVERS_PRODUCERS` (if present), `BASE_DATA_SERVICE_URL` (if present) inside `<project folder>/config/settings/base.py`
  
### Docker Run

After making the required changes in settings follow either of the below method to run the services.

- **Method 1: (Run using Script)**
  - To build the project run script : `./build.sh`
  - To run all services run script : `./run.sh`
  - To stop all services run script : `./kill.sh`

- **Method 2: (Run Individually)**
  - To build the project individually : `docker-compose -f local.yml build`
  - Run each service individually by command : `docker-compose -f local.yml up` or `docker-compose -f local.yml up -d` (for backgroud run)
  

## Future Improvements

- Implementation of priority notifications delivery first.
- Implementation of notification rate limiter to avoid sending excess notifications to users.
- Deployement in kubernetes for better docker management and scalability.

### Future Architechture

![Architectural diagram](https://github.com/Vermasoumitra020/notification_system/blob/master/diagrams/Notification%20Service%20V2.jpg)



  



  
