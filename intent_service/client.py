"""Test client for the Intent Service gRPC server."""

import asyncio
import sys

import grpc

import intent_service_pb2
import intent_service_pb2_grpc


async def classify_intent(message: str, host: str = "localhost", port: int = 50051):
    """Send a classification request to the Intent Service.

    Args:
        message: Customer message to classify.
        host: gRPC server host.
        port: gRPC server port.
    """
    target = f"{host}:{port}"
    print(f"\nConnecting to Intent Service at {target}...")

    async with grpc.aio.insecure_channel(target) as channel:
        stub = intent_service_pb2_grpc.IntentServiceStub(channel)
        request = intent_service_pb2.IntentRequest(message=message)

        try:
            response = await stub.IntentRecognizer(request, timeout=30.0)
            print(f"\n{'='*50}")
            print(f"Message:    {message}")
            print(f"Intent:     {response.intent}")
            print(f"Confidence: {response.confidence:.4f}")
            print(f"Reason:     {response.reason}")
            print(f"{'='*50}")
            return response

        except grpc.aio.AioRpcError as e:
            print(f"\ngRPC Error: {e.code()} - {e.details()}")
            return None


async def main():
    """Run test classifications."""
    # Use command-line argument or default test messages
    if len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])
        await classify_intent(message)
    else:
        test_messages = [
            "I want to check my account balance",
            "My card was stolen yesterday",
            "How do I transfer money to another account?",
            "I need to change my PIN code",
            "There is a transaction I don't recognize on my statement",
        ]

        print("Running intent classification tests...\n")
        for msg in test_messages:
            await classify_intent(msg)
            print()


if __name__ == "__main__":
    asyncio.run(main())
