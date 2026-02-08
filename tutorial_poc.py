#!/usr/bin/env python3
"""
Tutorial PoC for TaskWeaver HTTP API Endpoints

This script demonstrates how to interact with the TaskWeaver Chainlit UI
through its underlying HTTP API. The Chainlit UI doesn't expose a traditional
REST API, but we can test the backend components directly.

Usage:
    python tutorial_poc.py [--host HOST] [--port PORT] [--timeout SECONDS]

Options:
    --host    Host address (default: localhost)
    --port    Port number (default: 11280)
    --timeout Request timeout in seconds (default: 30)
"""

import argparse
import sys
import time
from typing import Any, Dict, List, Optional

try:
    import requests
    from requests.exceptions import ConnectionError, Timeout
except ImportError:
    print("Error: 'requests' package is required.")
    print("Install it with: pip install requests")
    sys.exit(1)


class TaskWeaverAPIClient:
    """
    Client for interacting with TaskWeaver's HTTP API endpoints.

    Note: TaskWeaver's Chainlit UI primarily uses WebSocket for real-time
    communication. This client demonstrates how to interact with the backend
    through HTTP endpoints where available.
    """

    def __init__(self, host: str = "localhost", port: int = 11280, timeout: int = 30):
        self.base_url = f"http://{host}:{port}"
        self.timeout = timeout
        self.session_id: Optional[str] = None

    def get_health(self) -> Dict[str, Any]:
        """
        Check the health status of the TaskWeaver service.

        Returns:
            Dict containing health status information.
        """
        try:
            response = requests.get(
                f"{self.base_url}/health",
                timeout=self.timeout
            )
            return {
                "status": "success",
                "data": response.json()
            }
        except ConnectionError:
            return {
                "status": "error",
                "message": f"Could not connect to {self.base_url}"
            }
        except Timeout:
            return {
                "status": "error",
                "message": f"Request to {self.base_url}/health timed out"
            }

    def get_version(self) -> Dict[str, Any]:
        """
        Get TaskWeaver version information.

        Returns:
            Dict containing version information.
        """
        try:
            response = requests.get(
                f"{self.base_url}/version",
                timeout=self.timeout
            )
            return {
                "status": "success",
                "data": response.json()
            }
        except ConnectionError:
            return {
                "status": "error",
                "message": f"Could not connect to {self.base_url}"
            }
        except Timeout:
            return {
                "status": "error",
                "message": f"Request to {self.base_url}/version timed out"
            }

    def create_session(self, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create a new conversation session.

        Args:
            payload: Optional session configuration.

        Returns:
            Dict containing session ID and status.
        """
        try:
            response = requests.post(
                f"{self.base_url}/session",
                json=payload or {},
                timeout=self.timeout
            )
            result = response.json()
            self.session_id = result.get("session_id")
            return {
                "status": "success",
                "data": result
            }
        except ConnectionError:
            return {
                "status": "error",
                "message": f"Could not connect to {self.base_url}"
            }
        except Timeout:
            return {
                "status": "error",
                "message": f"Request to {self.base_url}/session timed out"
            }

    def send_message(
        self,
        message: str,
        session_id: Optional[str] = None,
        files: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Send a message to the TaskWeaver agent.

        Args:
            message: The message text to send.
            session_id: Session ID (uses current session if not provided).
            files: Optional list of files to attach.

        Returns:
            Dict containing the agent's response.
        """
        session_id = session_id or self.session_id
        if not session_id:
            # Create a new session if none provided
            result = self.create_session()
            if result["status"] != "success":
                return result
            session_id = self.session_id

        payload = {
            "message": message,
            "session_id": session_id,
            "files": files or []
        }

        try:
            response = requests.post(
                f"{self.base_url}/chat",
                json=payload,
                timeout=self.timeout
            )
            return {
                "status": "success",
                "data": response.json()
            }
        except ConnectionError:
            return {
                "status": "error",
                "message": f"Could not connect to {self.base_url}"
            }
        except Timeout:
            return {
                "status": "error",
                "message": f"Request to {self.base_url}/chat timed out"
            }

    def get_session_list(self) -> Dict[str, Any]:
        """
        List all active sessions.

        Returns:
            Dict containing list of session IDs.
        """
        try:
            response = requests.get(
                f"{self.base_url}/sessions",
                timeout=self.timeout
            )
            return {
                "status": "success",
                "data": response.json()
            }
        except ConnectionError:
            return {
                "status": "error",
                "message": f"Could not connect to {self.base_url}"
            }
        except Timeout:
            return {
                "status": "error",
                "message": f"Request to {self.base_url}/sessions timed out"
            }

    def delete_session(self, session_id: str) -> Dict[str, Any]:
        """
        Delete a specific session.

        Args:
            session_id: The session ID to delete.

        Returns:
            Dict containing deletion status.
        """
        try:
            response = requests.delete(
                f"{self.base_url}/session/{session_id}",
                timeout=self.timeout
            )
            return {
                "status": "success",
                "data": response.json()
            }
        except ConnectionError:
            return {
                "status": "error",
                "message": f"Could not connect to {self.base_url}"
            }
        except Timeout:
            return {
                "status": "error",
                "message": f"Request to {self.base_url}/session/{session_id} timed out"
            }

    def get_plugins(self) -> Dict[str, Any]:
        """
        List available plugins.

        Returns:
            Dict containing list of plugin names and descriptions.
        """
        try:
            response = requests.get(
                f"{self.base_url}/plugins",
                timeout=self.timeout
            )
            return {
                "status": "success",
                "data": response.json()
            }
        except ConnectionError:
            return {
                "status": "error",
                "message": f"Could not connect to {self.base_url}"
            }
        except Timeout:
            return {
                "status": "error",
                "message": f"Request to {self.base_url}/plugins timed out"
            }

    def test_end_to_end(self, test_message: str = "What is 25 + 17?") -> Dict[str, Any]:
        """
        Run an end-to-end test of the TaskWeaver service.

        Args:
            test_message: The test message to send.

        Returns:
            Dict containing test results.
        """
        print(f"\n--- End-to-End Test ---")
        print(f"Test message: '{test_message}'")

        # Create session
        session_result = self.create_session()
        if session_result["status"] != "success":
            return session_result

        print(f"Created session: {self.session_id}")

        # Send message
        message_result = self.send_message(test_message)
        if message_result["status"] != "success":
            return message_result

        response_data = message_result.get("data", {})
        reply = response_data.get("reply", "No reply received")
        print(f"Response: {reply[:100]}..." if len(reply) > 100 else f"Response: {reply}")

        # Clean up
        self.delete_session(self.session_id)

        return {
            "status": "success",
            "data": {
                "session_id": self.session_id,
                "test_message": test_message,
                "response": reply
            }
        }


def main():
    """Main entry point for the tutorial PoC."""
    parser = argparse.ArgumentParser(
        description="TaskWeaver HTTP API Tutorial PoC"
    )
    parser.add_argument(
        "--host",
        default="localhost",
        help="Host address (default: localhost)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=11280,
        help="Port number (default: 11280)"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Request timeout in seconds (default: 30)"
    )
    parser.add_argument(
        "--test-message",
        default="What is 25 + 17?",
        help="Test message to send"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("TaskWeaver HTTP API Tutorial PoC")
    print("=" * 60)
    print(f"Base URL: {args.host}:{args.port}")
    print(f"Timeout: {args.timeout}s")
    print("=" * 60)

    # Create client
    client = TaskWeaverAPIClient(
        host=args.host,
        port=args.port,
        timeout=args.timeout
    )

    results = {}

    # Test 1: Health Check
    print("\n[1/5] Testing health endpoint...")
    health_result = client.get_health()
    results["health"] = health_result
    if health_result["status"] == "success":
        print(f"    Health check: OK")
        print(f"    Response: {health_result.get('data', {})}")
    else:
        print(f"    Health check: FAILED - {health_result.get('message', 'Unknown error')}")

    # Test 2: Get Version
    print("\n[2/5] Testing version endpoint...")
    version_result = client.get_version()
    results["version"] = version_result
    if version_result["status"] == "success":
        print(f"    Version: OK")
        print(f"    Response: {version_result.get('data', {})}")
    else:
        print(f"    Version: FAILED - {version_result.get('message', 'Unknown error')}")

    # Test 3: Get Plugins
    print("\n[3/5] Testing plugins endpoint...")
    plugins_result = client.get_plugins()
    results["plugins"] = plugins_result
    if plugins_result["status"] == "success":
        print(f"    Plugins: OK")
        plugins_data = plugins_result.get("data", {})
        plugin_list = plugins_data.get("plugins", [])
        print(f"    Available plugins: {len(plugin_list)}")
    else:
        print(f"    Plugins: FAILED - {plugins_result.get('message', 'Unknown error')}")

    # Test 4: Create Session
    print("\n[4/5] Testing session creation...")
    session_result = client.create_session()
    results["session_create"] = session_result
    if session_result["status"] == "success":
        print(f"    Session creation: OK")
        print(f"    Session ID: {client.session_id}")
    else:
        print(f"    Session creation: FAILED - {session_result.get('message', 'Unknown error')}")

    # Test 5: End-to-End Chat
    print("\n[5/5] Testing end-to-end chat...")
    e2e_result = client.test_end_to_end(args.test_message)
    results["end_to_end"] = e2e_result

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    for test_name, result in results.items():
        status = "PASS" if result["status"] == "success" else "FAIL"
        print(f"  {test_name}: {status}")

    print("=" * 60)

    # Check if we could connect
    if results["health"]["status"] != "success":
        print("\nNote: Could not connect to TaskWeaver service.")
        print(f"Please ensure the service is running at {args.host}:{args.port}")
        print("Usage: invoke.sh (to build and run with Docker)")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
