import paho.mqtt.client as paho


class MQTT():
    def __init__(self, config: dict, logger) -> None:
        self.config = config
        self.mqttConf = self.config["mqtt"]
        self.port = self.mqttConf["port"]
        self.dns = self.mqttConf["dns"]
        self.timeout = self.mqttConf["timeout"]
        #self.username = self.mqttConf["username"]
        #self.password = self.mqttConf["password"]

        self.brokerCon = None
        self.isConnected = False
        self.logger = logger


    def on_subscribe(self, client, userdata, mid, reasonCode, properties):
        '''
        @Brief: Function is a callback for subscribing to broker
        @Param: self - Instance of the class
        @Param: client - The client ID
        @Param: userdata - The data attached to the client
        @Param: mid - The message ID
        @Param: reasonCode - The success of the subscription
        '''
        self.logger.info(f"Subscribed successfully, mid={mid}")

    def on_message(self, client, userdata, msg):
        '''
        @Brief: Function is a callback for receiving a message from a sub topic
        @Param: self - Instance of the class
        @Param: client - The client ID
        @Param: userdata - The data attached to the client
        @Param: msg - The message sent
        '''
        self.logger.info(f"{msg.topic}: {msg.payload.decode()}")

    def connect_to_broker(self):
        '''
        @Brief: Function connects to broker
        @Param: self - Instance of the class
        @Return: None
        '''
        try:
            self.brokerCon = paho.Client(paho.CallbackAPIVersion.VERSION2)
            self.brokerCon.on_subscribe = self.on_subscribe
            self.brokerCon.on_message = self.on_message
            #self.brokerCon.username_pw_set(self.username, self.password)
            res = self.brokerCon.connect(self.dns, self.port, self.timeout)
            if res == 0:
                self.logger.info("Connected to broker")
                self.isConnected = True
            else:
                self.logger.error(f"Connection failed with rc={res}")
                
            self.brokerCon.loop_start()
            
        except Exception as e:
            self.logger.error(f"Unable to connect to MQTT broker {e}")
    
    def disconnect_from_broker(self):
        '''
        @Brief: Function disconnects from broker
        @Param: self - Instance of the class
        @Return: None
        '''
        if self.isConnected:
            self.brokerCon.disconnect()
            self.brokerCon.loop_stop()

    def is_connected(self) -> bool:
        '''
        @Brief: Function checks if application is connected to broker
        @Param: self - Instance of the class
        @Return: bool - True is connected, False otherwise
        '''
        return self.isConnected

    def mqtt_subscribe(self, topic: str):
        '''
        @Brief: Function subscribes to a topic
        @Param: self - Instance of the class
        @Param: topic - The topic to subscribe to
        @Return: subscription success  - 0 if good, -1 otherwise
        '''

        # Check if connected
        if not self.isConnected:
            return -1
        try:
            self.brokerCon.subscribe(topic) #TODO: Set up QoS
            return 0
        except Exception as e:
            self.logger.error(f"Error trying to subscribe to topic on broker: {e}")
            return -1

if __name__ == "__main__":
    from logger import Logger
    from configuration import Configuration
    from time import sleep

    
    confObj = Configuration("/Users/matthew/dev/SensorPlatform/config/host.yaml")
    config = confObj.get_config()

    loggerObj = Logger(config, service="MQTT")
    logger = loggerObj.get_logger()

    mqttObj = MQTT(config, logger)
    mqttObj.connect_to_broker()

    if mqttObj.is_connected():
        topic = "DniSensor/"
        mqttObj.mqtt_subscribe(topic)
        print(f"successful connection to topic {topic}")
    else:
        print("Connection failed")
    try:
        while mqttObj.is_connected():
            sleep(0.5)
            # Waiting for responses
    except KeyboardInterrupt as e:
        logger.info("Exiting cleanly")
        mqttObj.disconnect_from_broker()    