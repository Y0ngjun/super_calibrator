import numpy as np
import cv2 as cv

# The given video and calibration data
video_file = "data/chessboard.avi"
K = np.array(
    [
        [607.21421351, 0.0, 631.61705825],
        [0.0, 611.4314851, 376.7056395],
        [0.0, 0.0, 1.0],
    ]
)  # Derived from `calibrate_camera.py`
dist_coeff = np.array([0.01249517, -0.00812537, -0.00134196, -0.00195656, 0.00709386])

# Open a video
video = cv.VideoCapture(video_file)
assert video.isOpened(), "Cannot read the given input, " + video_file

# make a video
frame_width = int(video.get(cv.CAP_PROP_FRAME_WIDTH))
frame_height = int(video.get(cv.CAP_PROP_FRAME_HEIGHT))
fps = video.get(cv.CAP_PROP_FPS)
fourcc = cv.VideoWriter_fourcc(*'XVID')
out = cv.VideoWriter('data/output.avi', fourcc, fps, (frame_width, frame_height))

# Run distortion correction
show_rectify = True
map1, map2 = None, None
while True:
    # Read an image from the video
    valid, img = video.read()
    if not valid:
        break

    # Rectify geometric distortion (Alternative: `cv.undistort()`)
    info = "Original"
    if show_rectify:
        if map1 is None or map2 is None:    
            map1, map2 = cv.initUndistortRectifyMap(
                K, dist_coeff, None, None, (img.shape[1], img.shape[0]), cv.CV_32FC1
            )
        img = cv.remap(img, map1, map2, interpolation=cv.INTER_LINEAR)
        info = "Rectified"
    cv.putText(img, info, (10, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 0))

    out.write(img)

    # Show the image and process the key event
    cv.imshow("Geometric Distortion Correction", img)
    key = cv.waitKey(10)
    if key == ord(" "):  # Space: Pause
        key = cv.waitKey()
    if key == 27:  # ESC: Exit
        break
    elif key == ord("\t"):  # Tab: Toggle the mode
        show_rectify = not show_rectify

video.release()
out.release()
cv.destroyAllWindows()