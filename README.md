# Distributed Sensor Platform

The overiew of this project is to create a simulation of a sensor monitoring system.

It involves creating a simulated sensor and reading the values via MQTT.

Data is logged to a local database hosted on postrgeSQL

## Dependencies
- YAML
- Psycopg
- paho-mqtt
- docker

## Installation
To create an image navigate to the root directory of this project and run the following command
```
docker build -t sensor-platform .
```
Then once the image is built, run the following command to start the container
```
docker run --rm sensor-platform
```

This command will execute the program with the default configuration. To use other configurations, append the configuration name to the end of the command
```
docker run --rm sensor-platform wsl
```