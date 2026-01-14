import psycopg2
import json

class Database():
    def __init__(self, config, logger) -> None:
        self.config = config
        self.databaseConf = self.config["db"]
        self.logger = logger

        # Init values
        self.host = self.databaseConf["host"]
        self.port = self.databaseConf["port"]
        self.username = self.databaseConf["username"]
        self.password = self.databaseConf["password"]
        self.dbName = self.databaseConf["dbName"]

        #Connection objects
        self.conn = None
        self.isConnected = False
    
    def connect_to_db(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.dbName,
                user=self.username,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.isConnected = True
        except Exception as e:
            self.logger.error("Unable to connect to db")

    def upload_to_db(self, msg:str):
        '''
        @Brief: Function uploads to the database
        @Param: self - Instance of the class
        @Param: msg - The message in JSON format
        '''

        # Check the JSON is in the right format
        data = json.loads(msg)

        if len(data.keys()) != 2:
            self.logger.warning("Incorrect number of keys in JSON")
            return
        for key in data.keys():
            if key.lower() != "callmethod" and key.lower() != "args":
                self.logger.warning("Incorrect structure in JSON")
                return

        if isinstance(data["args"],dict):
            args = tuple(data["args"].values())
        else:
            args = tuple(data["args"])
        
        placeHolders = ','.join(["%s"] * len(args))
        callMethod = f"SELECT {data['callMethod']}({placeHolders})"

        cursor = None
        try:
            self.connect_to_db()
            cursor = self.conn.cursor()
            cursor.execute(callMethod, args)
            self.conn.commit()
            self.logger.info("Successfully logged data to db")
            self.logger.debug(f"{callMethod}, {args}")
    
        except Exception as e:
            self.logger.error(f"Error occured during processing of data {e}")
            if self.conn:
                # Rollback if there was an issue commiting the latest addition
                self.conn.rollback() 
        finally:
            if cursor:
                cursor.close()
            if self.is_connected():
                self.disconnect_db()

    def is_connected(self):
        '''
        @Brief: Function checks if the instance has a database connection
        @Param: self - Instance to the class
        @Return: True: if connected, else otherwise
        '''
        return self.isConnected

    def disconnect_db(self):
        '''
        @Brief: Function disconnects from database
        @Param: self - Instance of the class
        @Return: None
        '''
        try:
            self.conn.close()
            self.isConnected = False
        except Exception as e:
            self.logger.error("Error trying to close connection")

if __name__ == "__main__":
    from configuration import Configuration
    from logger import Logger
    from datetime import datetime as dt
    
    confObj = Configuration("/Users/matthew/dev/SensorPlatform/config/host.yaml")
    config = confObj.get_config()

    loggerObj = Logger(config, "Database")
    log = loggerObj.get_logger()

    # Init db
    dbObj = Database(config, log)

    jsonDict = {
    "callMethod" : "add_dni_values",
    "args" : {
        "logdatetime": dt.now().strftime("%Y-%m-%d %H:%M:%S"),
        "dni_id" : 111,
        "dni" : 1034.93
        }
    }

    jsonTxt = json.dumps(jsonDict)
    dbObj.upload_to_db(jsonTxt)

