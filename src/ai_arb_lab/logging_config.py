"""Logging configuration with structlog or standard logging."""

import logging
import sys

from ai_arb_lab.config import LOG_LEVEL, LOG_FORMAT


def setup_logging() -> None:
    """Configure logging. Uses structlog if available, else standard logging."""
    level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
    try:
        import structlog
        structlog.configure(
            processors=[
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
                structlog.dev.ConsoleRenderer() if LOG_FORMAT == "console" else structlog.processors.JSONRenderer(),
            ],
            wrapper_class=structlog.stdlib.BoundLogger,
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )
    except ImportError:
        # Fallback to standard logging
        logging.basicConfig(
            level=level,
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            stream=sys.stdout,
        )
    else:
        logging.getLogger().setLevel(level)
