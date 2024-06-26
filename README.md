# LLM Connector

Welcome to **LLM Connector**, your seamless solution for bridging the gap between various HTTP services and Language Model APIs, like OpenAI. With LLM Connector, you can effortlessly forward and manage HTTP requests, ensuring smooth communication between your applications and external services.

**Note: LLM Connector is currently under heavy development. Expect frequent updates and potential changes in functionality.**

## Goal

The primary goal of LLM Connector is to simplify and streamline the process of routing HTTP requests to language model APIs and other services, making integration effortless and efficient. Whether you're developing a chatbot, an AI-driven application, or any service requiring robust language processing capabilities, LLM Connector is here to make your life easier.

## Features

- **Easy Request Forwarding**: Forward HTTP requests to any service with ease, maintaining the original request path and method.
- **Support for Multiple Methods**: Handle GET, POST, PUT, DELETE, and PATCH requests seamlessly.
- **Efficient and Fast**: Built using FastAPI and httpx for high performance and reliability.
- **Extensible**: Easily customizable to fit your specific needs.
- **Debugging and Local Intercept**: Use LLM Connector as a debugging tool and local intercept for monitoring and modifying requests.
- **Logging**: Log all LLM interactions with inputs and outputs for monitoring and debugging.
- **Configurable Target Service**: Set the target service via a command line flag for flexibility.

## Installation

To get started with LLM Connector, first install the necessary packages:

```bash
pip install fastapi uvicorn httpx
```

## Examples
- Forwarding a Chatbot Request
Imagine you're developing a chatbot that needs to process natural language using OpenAI's API. With LLM Connector, you can route user messages through your proxy server to OpenAI seamlessly:

```python

# User sends a message to your chatbot
user_message = "Tell me a joke."

# Your chatbot forwards this message to OpenAI via LLM Connector
response = httpx.post('http://localhost:8000/v1/engines/davinci/completions', headers=headers, json={"prompt": user_message, "max_tokens": 50})

# The response is processed and returned to the user
print("Chatbot Response:", response.json())
```

- Integrating with External Services
LLM Connector also allows you to integrate other external services without worrying about the complexities of direct API calls:

```python
Copy code
# Forward a data processing request to an external service
response = httpx.get('http://localhost:8000/data/process', params={"data": "sample data"})

# Process the response from the external service
print("Processed Data:", response.json())
```