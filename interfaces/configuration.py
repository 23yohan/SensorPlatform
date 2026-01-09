import yaml

class Configuration():
    
    def __init__(self, configPath: str ):
        self.configPath = configPath
        self.config = self.import_config()

    
    def import_config(self) -> dict:
        '''
        @Brief: Function imports a YAML config file
        @Param: self - Instance of the class 
        @Return: A dictionary of all the configuration parameters
        '''
        with open(self.configPath, 'r') as file:
            config = yaml.safe_load(file)
        return config

    def get_config(self) -> dict :
        '''
        @Brief: Function gets the config parameters
        @Param: self - Instance of the class
        @Return: A dictionary of the config
        '''
        return self.config

if __name__ == "__main__":
    configPath = "/Users/matthew/dev/SensorPlatform/config/default.yaml"
    config = Configuration(configPath)