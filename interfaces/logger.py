import logging
from datetime import datetime as dt
from pathlib import Path

class Logger:
    def __init__(self, config: dict, service: str = "main") -> None:
        self.service = service
        self.config = config

        self.loggingConf = self.config["logging"]
        self.loggingPath = Path(self.loggingConf["loggingPath"])

        # Map string level to logging level safely
        levelMap = {
            "debug": logging.DEBUG,
            "info": logging.INFO,
            "warning": logging.WARNING,
            "error": logging.ERROR,
            "critical": logging.CRITICAL,
        }
        self.loggingLevel = levelMap.get(
            self.loggingConf["level"].lower(),
            logging.INFO
        )

        # Ensure log directory exists
        self.loggingPath.mkdir(parents=True, exist_ok=True)

        # Build log file path
        logFilename = f"{self.service}_{dt.now().strftime('%d-%m-%y')}.log"
        filePath = self.loggingPath / logFilename

        # Create logger
        self.logger = logging.getLogger(self.service)
        self.logger.setLevel(self.loggingLevel)
        self.logger.propagate = False

        # Prevent duplicate handlers
        if not self.logger.handlers:
            formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s: %(message)s",
                datefmt="%m/%d/%Y %I:%M:%S %p",
            )

            fileHandler = logging.FileHandler(filePath, mode="a")
            fileHandler.setLevel(self.loggingLevel)
            fileHandler.setFormatter(formatter)

            self.logger.addHandler(fileHandler)

    def get_logger(self) -> logging.Logger:
        return self.logger


if __name__ == "__main__":
    from configuration import Configuration
    confObj = Configuration("/Users/matthew/dev/SensorPlatform/config/default.yaml")
    config = confObj.get_config()

    loggingObj = Logger(config, service="bkLog")
    log = loggingObj.get_logger()

    log.info("This works!")
