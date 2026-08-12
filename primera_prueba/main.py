from fastapi import websockets
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.websockets import WebSocket
from src.routes.auth_routes import app as auth_routes


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    name:str
    edad:int

app.include_router(auth_routes, prefix="/auth", tags=["auth"])


@app.middleware("http")
async def add_custom_header(request, call_next):
    response = await call_next(request)
    response.headers["x-custom-header"] = "custom_value"
    return response

@app.on_event("startup")
async def startup_event():
    print("Startup event")
    
@app.on_event("shutdown")
async def shutdown_event():
    print("Shutdown event")

@app.post("/items/")
async def create_item(item: Item):
    return item

connected_clients=[]
@app.websocket("/ws/data")
async def websocket_data(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(WebSocket)
    try:
        while True:
            await websocket.receive_text()  
    except:
        connected_clients.remove(websocket)

@app.get("/")
async def read_root():
    return {"message": "Hello World!"}



