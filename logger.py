import logging
import threading
from datetime import datetime
import os


class NMGLogger:
    """
    A simple logger class that writes messages prefixed with a custom name to a single file with a dynamic name based on run date and time.
    """

    _lock = threading.Lock()
    _filename = None
    _handler = None

    def __init__(self, name, level=logging.INFO):
        """
        Initializes the logger with a custom name and log level.

        Args:
            name (str): The name to prefix log messages with.
            level (int, optional): The logging level. Defaults to logging.INFO.
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Acquire lock to ensure thread-safe creation of file handler
        with NMGLogger._lock:
            if NMGLogger._handler is None:
                self.create_file_handler()
            self.logger.addHandler(NMGLogger._handler)

    def create_file_handler(self):
        """
        Creates a new FileHandler with a dynamic filename based on current date and time (called only once).

        Creates a "Logs" folder if it doesn't exist.
        """
        now = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        filename = f"Logs/run-{now}-log.txt"

        # Ensure the Logs directory exists
        os.makedirs("Logs", exist_ok=True)  # Create directory if it doesn't exist

        NMGLogger._filename = filename
        handler = logging.FileHandler(filename)
        formatter = logging.Formatter("%(name)s => %(message)s")
        handler.setFormatter(formatter)
        NMGLogger._handler = handler

    def log(self, message, *args, **kwargs):
        """
        Logs a message prefixed with the logger name to the current log file.

        Args:
            message (str): The message to log.
            *args: Additional arguments to be formatted with the message.
            **kwargs: Additional keyword arguments to be formatted with the message.
        """
        self.logger.log(logging.INFO, message, *args, **kwargs)

    def __call__(self, message, *args, **kwargs):
        """
        Allows using the class instance like a function for logging.

        Args:
            message (str): The message to log.
            *args: Additional arguments to be formatted with the message.
            **kwargs: Additional keyword arguments to be formatted with the message.
        """
        self.log(message, *args, **kwargs)


# # Example usage
# logger1 = NMGLogger("MainModule")
# logger2 = NMGLogger("AnotherModule")  # Both use the same file

# logger1("This is a message from the main module.")
# logger2("This is a message from another module.")