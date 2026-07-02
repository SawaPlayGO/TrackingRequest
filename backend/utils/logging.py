import logging
import sys

import structlog
from structlog.typing import FilteringBoundLogger

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.dev.ConsoleRenderer() 
    ],
    logger_factory=structlog.PrintLoggerFactory(file=sys.stderr),
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    cache_logger_on_first_use=True,
)

logger: FilteringBoundLogger = structlog.get_logger()
