import logging
import requests
import uvicorn
from fastapi import FastAPI, Request, Response
import argparse
from datetime import datetime
import os

# Initialize FastAPI app
app = FastAPI()

# Command line argument parser
parser = argparse.ArgumentParser(description="Forward HTTP requests to another service.")
parser.add_argument("--target", default="https://api.openai.com", help="Target service URL")
parser.add_argument("--logfile", default=f"logs/{datetime.now().strftime('%Y-%m-%d')}.log", help="Log file name")
args = parser.parse_args()

# Ensure the logs directory exists
os.makedirs(os.path.dirname(args.logfile), exist_ok=True)

# Set up logging
logging.basicConfig(filename=args.logfile, level=logging.INFO, format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)

# Add a stream handler to print logs to stdout
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(message)s')
console.setFormatter(formatter)
logger.addHandler(console)

# Target URL from command line argument
TARGET_URL = args.target

@app.middleware("http")
async def forward_request(request: Request, call_next):
    # Log the incoming request
    logger.info(f"Incoming request: {request.method} {request.url}")
    
    # Forward the request to the target service
    forward_url = f"{TARGET_URL}{request.url.path}?{request.query_params}"
    headers = dict(request.headers.items())
    body = await request.body()
    
    # Log the forward request details
    logger.info(f"Forwarding request to: {forward_url}")
    
    # Send the request to the target service
    response = requests.request(
        method=request.method,
        url=forward_url,
        headers=headers,
        data=body,
        cookies=request.cookies,
        allow_redirects=False
    )
    
    # Create a FastAPI response from the target service's response
    forwarded_response = Response(
        content=response.content,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.headers.get('content-type')
    )
    
    # Log the full response from the target service
    logger.info(f"Response from target service: {response.status_code} - {response.content}")
    
    return forwarded_response

@app.post("/log_llm_interaction", status_code=201)
async def log_llm_interaction(request: Request):
    body = await request.json()
    logger.info(f"LLM Interaction - Input: {body.get('input')}, Output: {body.get('output')}")
    return {"status": "logged"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)