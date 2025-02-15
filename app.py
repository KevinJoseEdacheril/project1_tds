from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from os import path
import os
import requests


app = FastAPI ()

app.add_middleware (
    CORSMiddleware,
    allow_origins = ['*'],
    allow_credentials = True ,
    allow_methods = ['GET', 'POST'],
    allow_headers = ['*']
)

tools = [
    {
        "type":"function",
        "function":{
            "name": "script runner",
            "description": "Run a python script",
            "parameters": {
                "script_url":{
                    "type":"string",
                    "description":"URL of the script to run"
                },
                "args":{
                    "type":"array",
                    "items":{
                        "type":"string"
                    },
                    "description":"List of arguments to pass to the script"
                },
                "required":["script_url","args"]
            }
        },
    },
]
AIRPROXY_TOKEN =os.getenv("AIRPROXY_TOKEN")
@app.get ("/")
def home ():
    return {"TDS"}

@app.get ("/{read}")
def read_item (read: str):
    try: 
        with open(path,"r") as f:
            return f.read()
    except Exception as e:
        raise HTTPException(status_code=404, detail="Fle not found")

@app.post("/run")
def task_runner(task: str):
    url = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer({AIRPROXY_TOKEN})"
    }
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": task
            },
            {
                "role": "system",
                "content": "I am a helpful AI assistant."
            }
        ],
        "tools": tools,
        "tools:choice":"auto"
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()
    
if __name__ == '__main__':
    import uvicorn
    uvicorn.run (app, host="0.0.0.0", port=8000)
