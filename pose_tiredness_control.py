import cv2
import CV_2_31 as pose

def detect_tiredness(frame, threshold=0.2, pose_detector=None):
    landmarks = pose.detect_pose_landmarks(pose_detector, frame)
    if landmarks is None:
        return 'No person'

    face_center = pose.calculate_face_center_point(landmarks)
    shoulders_center = pose.calculate_shoulders_center(landmarks)

    height, _, _ = frame.shape
    face_y = face_center[1] * height
    shoulders_y = shoulders_center[1] * height

    status = 'Tired' if shoulders_y < face_y + (threshold * height) else 'OK'

    custom_connections = pose.create_custom_connections()
    drawing_specs = pose.create_green_drawing_spec()
    pose.draw_custom_pose_landmarks(frame, landmarks, custom_connections, drawing_specs)

    return status

def main():
    source = input("0 - webcam, 1-3 - samples\n")
    match source:
        case '0':
            source = 0
        case '1':
            source = './samples/sample1.mp4'
        case '2':
            source = "./samples/sample2.mp4"
        case _:
            print("Incorrect input!")
            return 1

    cap = cv2.VideoCapture(source)

    pose_detector, _, _ = pose.initialize_pose_detector()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        print(detect_tiredness(frame, 0.2, pose_detector))

        cv2.imshow('Pose Control', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()