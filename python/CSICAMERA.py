import cv2
import time

### Camera parameter
def gstreamer_pipeline(
    sensor_id=0,
    capture_width=3280,
    capture_height=2464,
    display_width=3280,
    display_height=2464,
    framerate=1,
    flip_method=2,
    ):
    return (
    "nvarguscamerasrc sensor-id=%d "
    "! "
    "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, format=(string)NV12, framerate=(fraction)%d/1 ! "
    "nvvidconv flip-method=%d ! "
    "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
    "videoconvert ! "
    "video/x-raw, format=(string)BGR ! appsink"
    % (
        sensor_id,
        capture_width,
        capture_height,
        framerate,
        flip_method,
        display_width,
        display_height,
    )
)
### Take a picture and Upload
def show_camera():
    cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    #cap.open(0)
    time.sleep(3)
    if(cap.isOpened()):
        ret_val, img_raw = cap.read()
        if (ret_val):
            print("Camera Capture Success !!")            
            # print("No.= {} parameter={}".format(3, cap.get(3)))
            # print("No.= {} parameter={}".format(4, cap.get(4)))
            # print("No.= {} parameter={}".format(15, cap.get(15)))
            cap.release()
            cv2.destroyAllWindows()
            return img_raw
        else :
            print("Camera Capture Fail !!")
            quit()
    #quit()