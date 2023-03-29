import cv2
import mediapipe as mp
import numpy as np
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

def calculate_angle(a,b,c):
    a=np.array(a)
    b=np.array(b)
    c = np.array(c)
    radians = np.arctan2(c[1]-b[1],c[0]-b[0]) - np.arctan2(a[1]-b[1],a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    if angle>180.0:
        angle = 360-angle
    return angle


counter = 0 
stage = None
flag = False
half = 10
text=""

class Video(object):
    def __init__(self):
        self.video=cv2.VideoCapture(0)
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    def __del__(self):
        self.video.release()
    def get_frame(self):
        ret,frame=self.video.read()
        image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        result = pose.process(image)
        if result.pose_landmarks:
            mp_drawing.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                 ) 
        ret,jpg=cv2.imencode('.jpg',frame)[1]
        return jpg.tobytes()