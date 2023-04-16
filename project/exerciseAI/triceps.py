from . import *   
from .util import *    

def gen():   
    up_pos = None
    down_pos = None
    pushup_pos = None 
    display_pos = None
    push_up_counter = 0
    mp_draw = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    
    pose = mp_pose.Pose(min_detection_confidence=0.7,min_tracking_confidence=0.5)
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret,frames=cap.read()
        image =cv2.cvtColor(cv2.flip(frames,1),cv2.COLOR_BGR2RGB)
        frames = cv2.flip(frames,1)
        # image.flags.writeable = False
        result = pose.process(image)
        # image.flags.writeable=True
        
        if result.pose_landmarks:
            landmarks = result.pose_landmarks.landmark
            Left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            Left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            Left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            Right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            Right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            Right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
            left_arm_angle = int(calculate_angle(Left_shoulder, Left_elbow, Left_wrist))
            right_arm_angle = int(calculate_angle(Right_shoulder, Right_elbow, Right_wrist))

            # left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            # right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            # left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            # right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            # left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            # right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
            # left_leg_angle = int(calculate_angle(left_hip, left_knee, left_ankle))
            # right_leg_angle = int(calculate_angle(right_hip, right_knee, right_ankle))
            # print(left_arm_angle,right_arm_angle )
            # print(left_arm_angle,right_arm_angle)
            if left_arm_angle > 140 and right_arm_angle>140:
                up_pos = 'Up'
                display_pos = 'Up'

            if left_arm_angle < 40 and right_arm_angle<40 and up_pos == 'Up':
                down_pos = 'Down'
                display_pos = 'Down'    

            if left_arm_angle > 140 and right_arm_angle>140 and down_pos == 'Down':

                pushup_pos = "up"
                display_pos = "up"
                push_up_counter += 1
                    # print(push_up_counter)
                up_pos = None
                down_pos = None
                pushup_pos = None  
            mp_draw.draw_landmarks(frames, result.pose_landmarks,mp_pose.POSE_CONNECTIONS)
        cv2.putText(frames, str(int(push_up_counter)), (15,70), 
                cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 3, cv2.LINE_AA)  
        frame = cv2.imencode('.jpg', frames)[1].tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        key = cv2.waitKey(20)
        if key == 27: 
            break