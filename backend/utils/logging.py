import structlog
from structlog.typing import FilteringBoundLogger

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer()
    ],
    logger_factory=structlog.BytesLoggerFactory(),
)

logger: FilteringBoundLogger = structlog.get_logger()