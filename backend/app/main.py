from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict

# IMPORT the modules
from app.services.gaze import GazeDetector
from app.services.emotion import EmotionDetector
from app.websockets.connection_manager import ConnectionManager

# --- THIS IS THE MISSING LINE THAT CAUSED THE ERROR ---
app = FastAPI() 

# Initialize Singletons
gaze_engine = GazeDetector()
emotion_engine = EmotionDetector()
manager = ConnectionManager()

@app.get("/")
def read_root():
    return {"status": "Smart Session Backend Running"}

@app.websocket("/ws/student")
async def student_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # 1. Receive JSON Data (Landmarks) from Client
            data = await websocket.receive_json()
            landmarks = data.get("landmarks")
            
            if not landmarks:
                continue

            # 2. Process Data
            gaze_status = gaze_engine.detect_distraction(landmarks)
            emotion_status = emotion_engine.detect_state(landmarks)

            # 3. Aggregation Logic
            final_state = "FOCUSED"
            if gaze_status == "LOOKING_AWAY":
                final_state = "PROCTOR_ALERT"
            elif emotion_status == "CONFUSED":
                final_state = "CONFUSED"
            
            # 4. Push to Teacher Dashboard
            await manager.broadcast_to_teachers({
                "student_id": "student_01",
                "status": final_state,
                "raw_emotion": emotion_status
            })

    except WebSocketDisconnect:
        print("Student Disconnected")

@app.websocket("/ws/teacher")
async def teacher_endpoint(websocket: WebSocket):
    await manager.connect_teacher(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect_teacher(websocket)