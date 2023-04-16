from . import *    
from .util import *       

def gen():
 
    mp_draw = mp.solutions.drawing_utils 
    mp_pose = mp.solutions.pose
    
    pose = mp_pose.Pose(min_detection_confidence=0.7,min_tracking_confidence=0.5) 
    cap = cv2.VideoCapture(0)
    label=""
    while cap.isOpened():
        ret,frames=cap.read()
        image =cv2.cvtColor(cv2.flip(frames,1),cv2.COLOR_BGR2RGB)
        frames = cv2.flip(frames,1)
        
        result = pose.process(image)
        
        if result.pose_landmarks:
            landmarks = result.pose_landmarks.landmark
            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            left_elbow    = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            left_elbow_angle = calculate_angle(left_shoulder,left_elbow,left_wrist)
            right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
            right_elbow_angle = calculate_angle(right_shoulder,right_elbow,right_wrist)
    #         left_elbow_angle = calculateAngle2(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
    #                                             landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
    #                                             landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value])
                
    #             # Get the angle between the right shoulder, elbow and wrist points. 
    #         right_elbow_angle = calculateAngle2(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
    #                                         landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
    #                                         landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value])   
            left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            left_shoulder_angle = calculate_angle(left_elbow, left_shoulder, left_hip)
            right_shoulder_angle = calculate_angle(right_hip,right_shoulder,right_elbow)
    #         # Get the angle between the left elbow, shoulder and hip points. 
    #         left_shoulder_angle = calculateAngle2(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
    #                                             landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
    #                                             landmarks[mp_pose.PoseLandmark.LEFT_HIP.value])

    #         # Get the angle between the right hip, shoulder and elbow points. 
    #         right_shoulder_angle = calculateAngle2(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
    #                                             landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
    #                                             landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value])
            left_knee=[landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            left_ankel=[landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            right_knee=[landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            right_ankel=[landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
            left_knee_angle = calculate_angle(left_hip,left_knee,left_ankel)
            right_knee_angle = calculate_angle(right_hip,right_knee,right_ankel)
    #         # Get the angle between the left hip, knee and ankle points. 
    #         left_knee_angle = calculateAngle2(landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
    #                                         landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value],
    #                                         landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value])
    #         right_knee_angle = calculateAngle2(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
    #                                   landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value],
    #                                   landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value])
    #         if left_elbow_angle > 165 and left_elbow_angle < 195 and right_elbow_angle > 165 and right_elbow_angle < 195:

    #     # Check if shoulders are at the required angle.
            if left_shoulder_angle > 80 and left_shoulder_angle < 110 and right_shoulder_angle > 80 and right_shoulder_angle < 110:

    # # Check if it is the warrior II pose.
    # #----------------------------------------------------------------------------------------------------------------

    #         # Check if one leg is straight.     
                    if left_knee_angle > 155 and left_knee_angle < 205 or right_knee_angle > 155 and right_knee_angle < 205:

                # Check if the other leg is bended at the required angle.
                        if left_knee_angle > 90 and left_knee_angle < 120 or right_knee_angle > 90 and right_knee_angle < 120:

                    # Specify the label of the pose that is Warrior II pose.
                            label = 'Warrior Pose - RIGHT'
                        else:
                            label = "Unknown Pose"     
            else: 
                label = 'Unknown Pose' 
 

            mp_draw.draw_landmarks(frames, result.pose_landmarks, mp_pose.POSE_CONNECTIONS) 
        cv2.putText(frames, str(label), (40, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        frame = cv2.imencode('.jpg',frames)[1].tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        key = cv2.waitKey(20)
        if key == 27: 
                break
        # cv2.imshow('Feed',cv2.cvtColor(image,cv2.COLOR_RGB2BGR))
        # if cv2.waitKey(10) & 0xFF == ord('q'):
        #     break  