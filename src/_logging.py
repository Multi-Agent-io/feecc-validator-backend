import sys

# set up logging configurations
BASE_LOGGING_CONFIG = {
    "colorize": True,
    "backtrace": True,
    "diagnose": True,
    "catch": True,
}

# logging settings for the console logs
CONSOLE_LOGGING_CONFIG = {
    **BASE_LOGGING_CONFIG,  # type: ignore
    "level": "DEBUG",
    "sink": sys.stdout,
}
