import logging
import sys

def setup_logger():
    """
    Configures a logger that writes to both the console and a file.
    """
    # Create a logger
    logger = logging.getLogger("intelli_core")
    logger.setLevel(logging.INFO)

    # Create a formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Create a handler for console output
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    # Create a handler for file output
    file_handler = logging.FileHandler("app.log")
    file_handler.setFormatter(formatter)

    # Add handlers to the logger, but only if they haven't been added before
    if not logger.handlers:
        logger.addHandler(stream_handler)
        logger.addHandler(file_handler)
        
    return logger

# Instantiate the logger
log = setup_logger()

if __name__ == '__main__':
    log.info("This is an info message.")
    log.warning("This is a warning message.")
    log.error("This is an error message.")
    print("Check the console and app.log for output.")
