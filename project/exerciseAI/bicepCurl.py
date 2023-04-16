from . import *   
from .util import *    

def gen():
    previous_time = 0
    # creating our model to draw landmarks
    mpDraw = mp.solutions.drawing_utils
    # creating our model to detected our pose
    my_pose = mp.solutions.pose
    pose = my_pose.Pose(min_detection_confidence=0.7,min_tracking_confidence=0.5)
    counter = 0 
    stage = None
    flag = False
    half = 10
    text=""
    """Video streaming generator function."""
    cap = cv2.VideoCapture(0)
# with mp_pose.Pose(min_detection_confidence=0.5,min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        success, img = cap.read()
        # converting image to RGB from BGR cuz mediapipe only work on RGB
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = pose.process(imgRGB)
        # print(result.pose_landmarks)
        if result.pose_landmarks:
            flag = True if counter%2 == 0 else False
            landmarks = result.pose_landmarks.landmark
            if flag:
                shoulder = [landmarks[my_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[my_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                elbow = [landmarks[my_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[my_pose.PoseLandmark.LEFT_ELBOW.value].y]
                wrist = [landmarks[my_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[my_pose.PoseLandmark.LEFT_WRIST.value].y]
            else:
                shoulder = [landmarks[my_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[my_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                elbow = [landmarks[my_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[my_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                wrist = [landmarks[my_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[my_pose.PoseLandmark.RIGHT_WRIST.value].y]
            angle = calculate_angle(shoulder,elbow,wrist)
            if angle > 160:
                stage = "down"
            if angle < 30 and stage =='down':
                stage="up"
                counter +=1
            cv2.putText(img, str(angle), 
                           tuple(np.multiply(elbow, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 180, 255), 2, cv2.LINE_AA
                                )
            mpDraw.draw_landmarks(img, result.pose_landmarks, my_pose.POSE_CONNECTIONS,
                                mpDraw.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                mpDraw.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2))

        # checking video frame rate
        # current_time = time.time()
        # fps = 1 / (current_time - previous_time)
        # previous_time = current_time

        # Writing FrameRate on video
        if(counter==0):
            cv2.putText(img, str(int(counter)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        elif(counter != 0 and  counter%20)==0:
            cv2.putText(img, str("Good Job"), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)      
        else:
            cv2.putText(img, str(int(counter)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        
        #cv2.imshow("Pose detection", img)
        frame = cv2.imencode('.jpg', img)[1].tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        key = cv2.waitKey(20)
        if key == 27: 
            break
