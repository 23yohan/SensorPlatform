import argparse
import sys
from datetime import datetime as dt
from time import sleep 

from interfaces.configuration import Configuration
from interfaces.sensor import DniSensor
from interfaces.logger import Logger
from interfaces.mqtt import MQTT


def init_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', '-c', help="Configuration path", required=True)

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = init_args()
    config = args.config

    # Initialise configuration
    confObj = Configuration(config)
    config = confObj.get_config()
    
    # Initialise logger
    loggerObj = Logger(config=config, service="main")
    log = loggerObj.get_logger()
    
    # Initialise sensor
    dniObj = DniSensor(config, log)
    dniObj.start_sensor()

    try:
        while dniObj.is_sensor_running():
            res = dniObj.retrieve_values()
            print(f"DNI sensor at {dt.now().time()} : {res}")
            sleep(1)
    except KeyboardInterrupt as ke:
        print("User stopped sensor. Shutting down")
        successful = dniObj.stop_sensor()
        if successful:
            print("Application closed")
        else:
            print("forcefully closing")
            sys.exit(1)


