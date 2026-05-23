"""Async gRPC client for the Intent Service."""

import logging
import os
import sys
from typing import Dict, Any

# Add the intent_grpc directory to sys.path to allow absolute imports in generated gRPC code
current_dir = os.path.dirname(os.path.abspath(__file__))
grpc_dir = os.path.join(current_dir, "intent_grpc")
if grpc_dir not in sys.path:
    sys.path.append(grpc_dir)

import grpc
from grpc import aio

from app.clients.base import BaseClient

logger = logging.getLogger(__name__)


class IntentGRPCClient(BaseClient):
    """Async gRPC client to communicate with the Intent Service."""

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.target = f"{host}:{port}"
        self.channel = None
        self.stub = None

    async def connect(self):
        """Establish gRPC channel and create stub."""
        self.channel = aio.insecure_channel(self.target)
        # Import generated gRPC code
        from app.clients.intent_grpc import (
            intent_service_pb2_grpc,
        )
        self.stub = intent_service_pb2_grpc.IntentServiceStub(self.channel)
        logger.info("Connected to Intent Service at %s", self.target)

    async def classify(self, message: str) -> Dict[str, Any]:
        """Call the IntentRecognizer RPC to classify a message.

        Args:
            message: Customer message to classify.

        Returns:
            Dict with intent, confidence, and reason.
        """
        from app.clients.intent_grpc import intent_service_pb2

        if self.stub is None:
            await self.connect()

        request = intent_service_pb2.IntentRequest(message=message)

        try:
            response = await self.stub.IntentRecognizer(
                request, timeout=30.0
            )
            return {
                "intent": response.intent,
                "confidence": response.confidence,
                "reason": response.reason,
            }
        except aio.AioRpcError as e:
            if e.code() == grpc.StatusCode.UNAVAILABLE:
                logger.error("Intent Service unavailable: %s", e.details())
                return {
                    "intent": "general_inquiry",
                    "confidence": 0.0,
                    "reason": f"Intent Service unavailable: {e.details()}",
                }
            elif e.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
                logger.error("Intent Service timeout: %s", e.details())
                return {
                    "intent": "general_inquiry",
                    "confidence": 0.0,
                    "reason": "Intent Service timeout",
                }
            else:
                logger.error("gRPC error: %s - %s", e.code(), e.details())
                return {
                    "intent": "general_inquiry",
                    "confidence": 0.0,
                    "reason": f"gRPC error: {e.details()}",
                }

    async def close(self):
        """Close the gRPC channel."""
        if self.channel:
            await self.channel.close()
            logger.info("Disconnected from Intent Service")
