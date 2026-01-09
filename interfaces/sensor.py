import math
import random
from datetime import datetime as dt
from datetime import time
import threading
from time import sleep
from threading import Lock
from queue import Queue


class DniSensor():
    def __init__(self, config) -> None:
        self.config = config
        self.sensorConf = self.config["dniSensor"]
        self.minLim = self.sensorConf["minimumLimit"]
        self.maxLim = self.sensorConf["maximumLimit"]
        self.limStep = self.sensorConf["limitStep"]
        self.sunriseTime = time(self.sensorConf["sunrise"], 0)
        self.sunsetTime = time(self.sensorConf["sunset"], 0)
        
        self.sunriseSec = self.to_seconds(self.sunriseTime)
        self.sunsetSec = self.to_seconds(self.sunsetTime)

        # Define threading parameters
        self._sensorThread = threading.Thread(target=self.sensor_thread)
        self._sensorActive = False
        self.lock = Lock()
        self.dataQueue = Queue()
    
    def to_seconds(self, t: dt) -> int:
        '''
        @Brief: Helper function for the dni_simulator
        @Param: self - Instance of the class itself
        @return: number of seconds elapsed since midnight
        '''
        return (t.hour * 3600) + (t.minute * 60) + t.second

    def dni_simulator(self) -> float:
        '''
        @Brief: This function is going to simulate DNI sensor values over a day
        @Param: self - Instance of the class
        @Return: float
        '''
        # Find the current time in seconds
        currentTime = dt.now().time()
        currTimeSec = self.to_seconds(currentTime)
                
        # If we are in the night time
        if currTimeSec > self.sunsetSec or currTimeSec < self.sunriseSec:
            return float(self.minLim)

        # Normalise the daylight
        tNorm = (currTimeSec - self.sunriseSec) / (self.sunsetSec - self.sunriseSec)

        currentDni = self.maxLim * math.sin(math.pi * tNorm)

        # Add some noise to this
        currentDni += random.gauss(0,self.sensorConf["stdDev"])

        # Make sure this is still in the limits of acceptable range
        dni = max(0, min(currentDni, self.maxLim))
        return round(dni, 2)

    def sensor_thread(self):
        '''
        @Brief: Function is a threading target which generates the sensor data
        @Param: self - Instance of the class
        @Return: None
        '''
        while self._sensorActive:
            res = self.dni_simulator()
            self.dataQueue.put(res)
            sleep(1)
    
    def start_sensor(self):
        '''
        @Brief: Function that starts the thread
        @Param: self - Instance of the class
        @Return: None
        '''
        self._sensorActive = True
        self._sensorThread.start()
    
    def is_sensor_running(self) -> bool:
        '''
        @Brief: Function checks if the sensor is running
        @Param: Instance of the class
        @Return: True if yes, No otherwise
        '''
        return self._sensorActive
    
    def stop_sensor(self) -> bool:
        '''
        @Brief: Function stops the thread
        @Param: self - Instance of the class
        @Return true if stopped, false otherwise
        '''
        try:
            self._sensorActive = False
            self._sensorThread.join()
        except Exception as e:
            print(f"Unable to stop sensor {e}")
        finally:
            return True if not self._sensorActive else False

    def retrieve_values(self) -> float:
        '''
        @Brief: Function retrieves the latest value of the queue
        @Param: self - Instance of the class 
        @Return: value from the queue, -1.0 if cannot retrieve
        '''
        try:
            return self.dataQueue.get()
        except Exception as e:
            print(f"Error retreving value off queue {e}")
            return -1.0

    
if __name__ == "__main__":
    from configuration import Configuration
    
    confObj = Configuration("/Users/matthew/dev/SensorPlatform/config/default.yaml")
    config = confObj.get_config()
    dniSim = DniSensor(config)
    dniSim.dni_simulator()

    i = 0
    while i < 10:
        print(f"DNI Measurement at {dt.now().time()}: {dniSim.dni_simulator()}")
        i+=1
        sleep(1)        

    

        