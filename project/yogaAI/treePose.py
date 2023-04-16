from . import *   
from .util import *    

def gen():     
    mpDraw = mp.solutions.drawing_utils
    # creating our model to detected our pose
    my_pose = mp.solutions.pose
    pose = my_pose.Pose(min_detection_confidence=0.7,min_tracking_confidence=0.5) 

    """Video streaming generator function."""
    label="Unknown Pose"
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        success, img = cap.read()
        # converting image to RGB from BGR cuz mediapipe only work on RGB
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = pose.process(imgRGB)
        # print(result.pose_landmarks)
        if result.pose_landmarks:
            landmarks = result.pose_landmarks.landmark
            # Left_shoulder = [landmarks[my_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[my_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            # Left_elbow = [landmarks[my_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[my_pose.PoseLandmark.LEFT_ELBOW.value].y]
            # Left_wrist = [landmarks[my_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[my_pose.PoseLandmark.LEFT_WRIST.value].y]
            left_knee_angle = calculate_angle([landmarks[my_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[my_pose.PoseLandmark.LEFT_HIP.value].y],
                                    [ landmarks[my_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[my_pose.PoseLandmark.LEFT_KNEE.value].y],
                                     [landmarks[my_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[my_pose.PoseLandmark.LEFT_ANKLE.value].y])
            
                
            right_knee_angle = calculate_angle([landmarks[my_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[my_pose.PoseLandmark.RIGHT_HIP.value].y],
                                      [landmarks[my_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[my_pose.PoseLandmark.RIGHT_KNEE.value].y],
                                      [landmarks[my_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[my_pose.PoseLandmark.RIGHT_ANKLE.value].y])
            


            if left_knee_angle > 165 and left_knee_angle < 195 or right_knee_angle > 165 and right_knee_angle < 195:

        # Check if the other leg is bended at the required angle.
                if left_knee_angle > 315 and left_knee_angle < 335 or right_knee_angle > 25 and right_knee_angle < 45:

            # Specify the label of the pose that is tree pose.
                     label = 'Tree Pose - RIGHT'
                else:
                    label = 'Unknown Pose'
            else:
                label = 'Unknown Pose'   
            # cv2.putText(img, str(Left_elbowAngle), 
            #                tuple(np.multiply(Left_elbow, [640, 480]).astype(int)), 
            #                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 180, 255), 2, cv2.LINE_AA
            #                     )
            # cv2.putText(img, str(Right_elbowAngle), 
            #                tuple(np.multiply(Right_elbow, [640, 480]).astype(int)), 
            #                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 180, 255), 2, cv2.LINE_AA
            #                     )
            mpDraw.draw_landmarks(img, result.pose_landmarks, my_pose.POSE_CONNECTIONS)

        # checking video frame rate
        # current_time = time.time()  
        # fps = 1 / (current_time - previous_time)
        # previous_time = current_time

        # Writing FrameRate on video
        cv2.putText(img, str( label), (40, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        #cv2.imshow("Pose detection", img)
        frame = cv2.imencode('.jpg', img)[1].tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        key = cv2.waitKey(20) 
        if key == 27:
            break
#  if left_knee_angle > 165 and left_knee_angle < 195 or right_knee_angle > 165 and right_knee_angle < 195:

#         # Check if the other leg is bended at the required angle.
#         if left_knee_angle > 315 and left_knee_angle < 335 or right_knee_angle > 25 and right_knee_angle < 45:

#             # Specify the label of the pose that is tree pose.
#             label = 'Tree Pose'
 