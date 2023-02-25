
"""
fakeapi.py - Emulates Patroni endpoints
"""
#from datetime import datetime, timezone
import json
import uvicorn
from fastapi import FastAPI, Response
from pydantic import BaseModel

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

@app.get("/patroni")
async def patroni_endpoint():
    with open('json/endpoint_patroni.json', 'r', encoding="utf-8") as file:
        data = json.load(file)
    return data

@app.get("/cluster")
async def cluster_endpoint():
    with open('json/endpoint_cluster.json', 'r', encoding="utf-8") as file:
        data = json.load(file)
    return data

@app.get("/history")
async def history_endpoint():
    with open('json/endpoint_history.json', 'r', encoding="utf-8") as file:
        data = json.load(file)
    return data

@app.get("/config")
async def config_endpoint():
    with open('json/endpoint_config.json', 'r', encoding="utf-8") as file:
        data = json.load(file)
    return data

@app.post("/reload")
async def reload_endpoint():
    return Response(content="Successfully scheduled reload", status_code=202)

@app.post("/restart")
async def restart_endpoint():
    return Response(content="Successfully scheduled restart", status_code=202)

# curl -s http://localhost:8888/switchover -XPOST  \
# -d '{"leader":"postgresql0","scheduled_at":"2019-09-24T12:00+00"}' \
# -H "Content-Type: application/json"
@app.post("/switchover")
async def switchover_endpoint(request: SwitchoverRequest):
    leader = request.leader
    scheduled_at = request.scheduled_at
    # perform the switchover logic here
    return {"message": f"Switching over to {leader} at {scheduled_at}."}

# curl -s http://localhost:8888/failover -XPOST \
# -d '{"candidate":"postgresql12","scheduled_at":"2019-09-25T12:00+00"}' \
# -H "Content-Type: application/json"
@app.post("/failover")
async def failover_endpoint(request: FailoverRequest):
    candidate = request.candidate
    scheduled_at = request.scheduled_at
    return {"message": f"Failing over to {candidate} at {scheduled_at}."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)
