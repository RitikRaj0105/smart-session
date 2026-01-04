from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        # List to keep track of active teacher connections
        self.teacher_connections: list[WebSocket] = []

    async def connect_teacher(self, websocket: WebSocket):
        """Accepts a new teacher connection and stores it."""
        await websocket.accept()
        self.teacher_connections.append(websocket)
        print(f"Teacher connected. Total: {len(self.teacher_connections)}")

    def disconnect_teacher(self, websocket: WebSocket):
        """Removes a teacher connection when they leave."""
        if websocket in self.teacher_connections:
            self.teacher_connections.remove(websocket)
            print(f"Teacher disconnected. Total: {len(self.teacher_connections)}")

    async def broadcast_to_teachers(self, data: dict):
        """
        pushes JSON data to all connected teachers.
        Handles stale connections gracefully.
        """
        for connection in self.teacher_connections:
            try:
                await connection.send_json(data)
            except Exception as e:
                print(f"Error sending data: {e}")
                self.disconnect_teacher(connection)