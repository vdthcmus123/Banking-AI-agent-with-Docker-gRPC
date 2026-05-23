"""Base client with common HTTP request handling."""

import logging
from typing import Any, Dict, Optional

import requests

logger = logging.getLogger(__name__)


class BaseHTTPClient:
    """Base HTTP client with timeout and error handling."""

    def __init__(self, base_url: str, timeout: float = 120.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    def post(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Send a POST request and return JSON response."""
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            logger.error("Request to %s timed out after %ss", url, self.timeout)
            raise
        except requests.exceptions.ConnectionError:
            logger.error("Cannot connect to %s", url)
            raise
        except requests.exceptions.HTTPError as e:
            logger.error("HTTP error from %s: %s", url, e.response.text)
            raise

    def get(self, endpoint: str) -> Dict[str, Any]:
        """Send a GET request and return JSON response."""
        url = f"{self.base_url}{endpoint}"
        response = self.session.get(url, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def close(self):
        """Close the HTTP session."""
        self.session.close()
