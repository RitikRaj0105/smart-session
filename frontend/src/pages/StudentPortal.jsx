import React, { useEffect, useRef, useState } from 'react';
import Webcam from 'react-webcam';
import { FaceMesh } from '@mediapipe/face_mesh';
import { Camera } from '@mediapipe/camera_utils';

const StudentPortal = () => {
  const webcamRef = useRef(null);
  const socketRef = useRef(null);

  useEffect(() => {
    // 1. Setup WebSocket
    socketRef.current = new WebSocket('ws://localhost:8000/ws/student');
    
    // 2. Setup MediaPipe
    const faceMesh = new FaceMesh({
      locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/${file}`,
    });
    
    faceMesh.setOptions({
      maxNumFaces: 1,
      refineLandmarks: true,
      minDetectionConfidence: 0.5,
      minTrackingConfidence: 0.5,
    });

    faceMesh.onResults((results) => {
      if (results.multiFaceLandmarks && results.multiFaceLandmarks.length > 0) {
        // Send landmarks to Python Backend
        if (socketRef.current.readyState === WebSocket.OPEN) {
          socketRef.current.send(JSON.stringify({
            landmarks: results.multiFaceLandmarks[0]
          }));
        }
      }
    });

    if (webcamRef.current) {
      const camera = new Camera(webcamRef.current.video, {
        onFrame: async () => {
          await faceMesh.send({ image: webcamRef.current.video });
        },
        width: 640,
        height: 480,
      });
      camera.start();
    }
  }, []);

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-900 text-white">
      <h1 className="text-2xl mb-4">Student Portal</h1>
      <div className="border-4 border-blue-500 rounded-lg overflow-hidden">
        <Webcam ref={webcamRef} className="w-[640px] h-[480px]" />
      </div>
      <p className="mt-4 text-gray-400">Monitoring Active... Good Luck!</p>
    </div>
  );
};

export default StudentPortal;