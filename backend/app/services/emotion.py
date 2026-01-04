import numpy as np

class EmotionDetector:
    def detect_state(self, landmarks):
        """
        Classifies state into: FOCUSED, HAPPY, CONFUSED
        """
        lm_arr = np.array([(lm.x, lm.y) for lm in landmarks])

        # 1. Brow Furrowing (Confusion Indicator)
        # Measure distance between left and right eyebrows
        # Indices: 107 (Left Brow Inner), 336 (Right Brow Inner)
        brow_dist = np.linalg.norm(lm_arr[107] - lm_arr[336])
        
        # Normalize by face width to account for camera distance
        face_width = np.linalg.norm(lm_arr[234] - lm_arr[454])
        normalized_brow_dist = brow_dist / face_width

        # 2. Smile Detection (Happy Indicator)
        # Measure distance between mouth corners
        # Indices: 61 (Left Corner), 291 (Right Corner)
        mouth_width = np.linalg.norm(lm_arr[61] - lm_arr[291])
        normalized_mouth = mouth_width / face_width

        # --- DECISION TREE ---
        
        # Thresholds (You must tune these in your 'Integrity Video')
        if normalized_mouth > 0.55: 
            return "HAPPY"  # Wide mouth usually means smiling
            
        # If brows are pinched together and mouth is not wide
        if normalized_brow_dist < 0.22:
            return "CONFUSED" 

        return "FOCUSED"