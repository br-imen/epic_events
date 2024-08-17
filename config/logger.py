import logging
from os import getenv
from sentry_sdk.integrations.logging import LoggingIntegration
import sentry_sdk


def get_logger():
    # Check if the logger already exists
    logger = logging.getLogger('epic_events_logger')
    if logger.hasHandlers():
        # Logger already exists, return the existing instance
        return logger

    # Initialize Sentry
    sentry_logging = LoggingIntegration(
        level=logging.INFO,        # Capture info and above as breadcrumbs
        event_level=logging.INFO   # Send info and above as events
    )

    sentry_sdk.init(
        dsn=getenv("SENTRY_DSN"),
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
        integrations=[sentry_logging]
    )

    # Set the minimum logging level
    logger.setLevel(logging.DEBUG)

    # Create and set up the console handler
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
