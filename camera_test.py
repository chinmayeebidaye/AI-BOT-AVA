import cv2

camera_index = 1  # Assuming 1 is the OBS Virtual Camera
cap = cv2.VideoCapture(camera_index)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Save the frame to a file instead of displaying it
    cv2.imwrite("frame.jpg", frame)
    print("Frame saved to 'frame.jpg'")

    # Exit condition
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
