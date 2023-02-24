#from datetime import datetime, timezone
from fastapi import FastAPI, Response
from pydantic import BaseModel
import uvicorn
import json

app = FastAPI()

#
# Patroni formatted timestamp string
#
#now = datetime.utcnow()
#timestamp = now.strftime('%Y-%m-%dT%H:%M:%S.%f%z')[:-2]
#print(timestamp)

class SwitchoverRequest(BaseModel):
    leader: str
    scheduled_at: str

class FailoverRequest(BaseModel):
    candidate: str
    scheduled_at: str

# TODO verification if this is the right request and response
@app.get("/patroni")
async def read_json():
    with open('json/endpoint_patroni.json', 'r') as f:
        data = json.load(f)
    return data

# TODO verification if this is the right request and response
@app.get("/cluster")
async def read_json():
    with open('json/endpoint_cluster.json', 'r') as f:
        data = json.load(f)
    return data

# TODO verification if this is the right request and response
@app.get("/history")
async def read_json():
    with open('json/endpoint_history.json', 'r') as f:
        data = json.load(f)
    return data

# TODO verification if this is the right request and response
@app.get("/config")
async def read_json():
    with open('json/endpoint_config.json', 'r') as f:
        data = json.load(f)
    return data

# TODO verification if this is the right request and response
@app.post("/reload")
async def reload_config():
    return Response(content="Successfully scheduled reload", status_code=202)

# TODO verification if this is the right request and response
@app.post("/restart")
async def reload_config():
    return Response(content="Successfully scheduled restart", status_code=202)

# TODO verification if this is the right request and response
# curl -s http://localhost:8888/switchover -XPOST -d '{"leader":"postgresql0","scheduled_at":"2019-09-24T12:00+00"}' -H "Content-Type: application/json"
@app.post("/switchover")
async def perform_switchover(request: SwitchoverRequest):
    leader = request.leader
    scheduled_at = request.scheduled_at
    # perform the switchover logic here
    return {"message": f"Switching over to {leader} at {scheduled_at}."}

# TODO verification if this is the right request and response
# curl -s http://localhost:8888/failover -XPOST -d '{"candidate":"postgresql12","scheduled_at":"2019-09-25T12:00+00"}' -H "Content-Type: application/json"
@app.post("/failover")
async def perform_failover(request: FailoverRequest):
    candidate = request.candidate
    scheduled_at = request.scheduled_at
    # perform the failover logic here
    return {"message": f"Failing over to {candidate} at {scheduled_at}."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)
