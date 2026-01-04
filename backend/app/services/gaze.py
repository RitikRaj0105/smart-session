import numpy as np

class GazeDetector:
    def __init__(self):
        # MediaPipe landmark indices for eyes
        self.LEFT_EYE = [33, 160, 158, 133, 153, 144]
        self.RIGHT_EYE = [362, 385, 387, 263, 373, 380]

    def _get_eye_ratio(self, eye_points, landmarks):
        # Calculate vertical distances
        A = np.linalg.norm(landmarks[eye_points[1]] - landmarks[eye_points[5]])
        B = np.linalg.norm(landmarks[eye_points[2]] - landmarks[eye_points[4]])
        # Calculate horizontal distance
        C = np.linalg.norm(landmarks[eye_points[0]] - landmarks[eye_points[3]])
        # Compute Eye Aspect Ratio (EAR)
        return (A + B) / (2.0 * C)

    def detect_distraction(self, landmarks):
        """
        Input: List of (x, y) coordinates from FaceMesh.
        Output: Boolean (True if distracted/looking away).
        """
        # Convert to numpy array for easier math
        lm_arr = np.array([(lm.x, lm.y) for lm in landmarks])
        
        # Simple Logic: If nose points deeply left/right/up/down
        nose_tip = lm_arr[1]
        left_cheek = lm_arr[234]
        right_cheek = lm_arr[454]
        
        # Check horizontal head turn (Yaw)
        face_width = np.linalg.norm(left_cheek - right_cheek)
        dist_to_left = np.linalg.norm(nose_tip - left_cheek)
        dist_to_right = np.linalg.norm(nose_tip - right_cheek)
        
        ratio = dist_to_left / (dist_to_right + 1e-6)

        # Thresholds: If ratio is too high/low, user is looking sideways
        if ratio < 0.4 or ratio > 2.5:
             return "LOOKING_AWAY"
             
        return "FOCUSED"