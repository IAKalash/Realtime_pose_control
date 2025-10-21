import cv2
import CV_2_31 as pose

def detect_tiredness(frame, pose_detector, threshold=0.2):
    """
    Determines the person's status from the frame.

    Parameters:
        `frame` (np.ndarray): Input frame.
        `threshold` (float): Threshold distance between shoulders and face (scales with frame size,
                           the greater the distance, the smaller the threshold) 
        `pose_detector`: Pose detector from `initialize_pose_detector()`.

    Returns:
        str: `Tired`, `OK` or `No person`.

    Warning: 
        Argument checks are absent to avoid performance loss.
    """
    # Detect pose landmarks using the provided detector
    landmarks = pose.detect_pose_landmarks(pose_detector, frame)
    if landmarks is None:
        return 'No person'

    # Calculate centers for face and shoulders
    face_center = pose.calculate_face_center_point(landmarks)
    shoulders_center = pose.calculate_shoulders_center(landmarks)
    if face_center is None or shoulders_center is None:
        return 'No person'

    # Get frame height for denormalization
    height, _, _ = frame.shape
    face_y = face_center[1] * height
    shoulders_y = shoulders_center[1] * height

    # Determine status
    status = 'Tired' if shoulders_y < face_y + (threshold * height) else 'OK'

    return status


def main():
    source = input("0 - webcam; 1,2 - video samples\n")
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

    try:
        cap = cv2.VideoCapture(source)
        if not cap.isOpened():
            cap.release()
            raise ValueError("Error opening source!")
    except Exception as e:
        print(f"Error: {e}")
        return 1

    # Initialize pose detector
    pose_detector, _, _ = pose.initialize_pose_detector()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        try:
            print(detect_tiredness(frame, pose_detector, 0.2))

            # Only for visualizing points. Not recommended for use in real code. 
            # Partially duplicates the detect_tiredness function
            # landmarks = pose.detect_pose_landmarks(pose_detector, frame)
            # custom_connections = pose.create_custom_connections()
            # drawing_specs = pose.create_green_drawing_spec()
            # pose.draw_custom_pose_landmarks(frame, landmarks, custom_connections, drawing_specs)
            # End of visualization block
        
        except Exception as e:
            print(f"Frame processing error: {e}")
            continue

        # Display the processed frame
        cv2.imshow('Pose Control', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()