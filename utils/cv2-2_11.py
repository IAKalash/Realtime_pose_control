import cv2

#video_init
video_capture = cv2.VideoCapture(0)

#using haarcascade_met
face_casc = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

while True:
    good, cam_vid = video_capture.read()
    """
    # face_det
    # args:
    # 1.3 - scale factor (how much the image is reduced at each iteration)
    # 4 - minimum number of neighbors (affects the quality of detection)
    """ 
    faces = face_casc.detectMultiScale(cam_vid, 1.3, 4)

    # many faces_detection
    for (x, y, w, h) in faces:
        # adding "Face" upper face img
        # args: img, text, coords, font, scale, color, thickness
        cv2.putText(cam_vid, "Face", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # drawing rec
        # args: img, upper left angle, lower right angle, color, thickness
        cv2.rectangle(cam_vid, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # video on the screen
    cv2.imshow("Video", cam_vid)

    # break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# memory clear
video_capture.release()
cv2.destroyAllWindows()
