"""Base client interface for backend services."""

import logging

logger = logging.getLogger(__name__)


class BaseClient:
    """Base class for service clients."""

    async def connect(self):
        """Establish connection to the service."""
        raise NotImplementedError

    async def close(self):
        """Close connection to the service."""
        raise NotImplementedError
