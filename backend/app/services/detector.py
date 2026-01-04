# currently, we are trusting the client-side landmarks to reduce latency.
# This file is reserved for server-side verification if we switch to sending raw images.

class LandryMarkVerifier:
    def __init__(self):
        pass
    
    def verify_integrity(self, landmarks):
        # Simple check: do we have the expected number of points?
        # MediaPipe FaceMesh has 468 landmarks.
        if len(landmarks) != 468:
            return False
        return True