import cv2
import numpy as np
import os
import time
from pioneer_sdk import Pioneer, Camera

thing_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

min_v = 1300
max_v = 1700
frame_count = 0

pioneer_mini = Pioneer()
camera = Camera()

current_directory = os.path.dirname(os.path.abspath(__file__))
way_to_file_save = os.path.join(current_directory, 'frame_photos')
if not os.path.exists(way_to_file_save):
    os.makedirs(way_to_file_save)

print(
    """
    1 -- arm
    2 -- disarm
    3 -- takeoff
    4 -- land

    ↶q  w↑  e↷    i-↑
    ←a      d→     k-↓
        s↓
    
    x -- take photo
    esc -- exit
    """
)

try:
    while True:
        ch_1 = 1500
        ch_2 = 1500
        ch_3 = 1500
        ch_4 = 1500
        ch_5 = 2000
        frame = camera.get_frame()
        if frame is not None:
            camera_frame = cv2.imdecode(np.frombuffer(frame, dtype=np.uint8), cv2.IMREAD_COLOR)
            cv2.imshow("pioneer_camera_stream", camera_frame)

            things = thing_cascade.detectMultiScale(camera_frame, scaleFactor=1.2, minNeighbors=3, minSize=(30, 30))
            for (x, y, w, h) in things:
                cv2.rectangle(camera_frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            key = cv2.waitKey(1)
            if key == 27:  # esc
                print("Exiting...")
                pioneer_mini.land()
                break
            elif key == ord("1"):
                pioneer_mini.arm()
            elif key == ord("2"):
                pioneer_mini.disarm()
            elif key == ord("3"):
                time.sleep(2)
                pioneer_mini.arm()
                time.sleep(1)
                pioneer_mini.takeoff()
                time.sleep(2)
            elif key == ord("4"):
                pioneer_mini.land()
                time.sleep(2)
            elif key == ord("w"):
                ch_3 = min_v
            elif key == ord("s"):
                ch_3 = max_v
            elif key == ord("a"):
                ch_4 = min_v
            elif key == ord("d"):
                ch_4 = max_v
            elif key == ord("q"):
                ch_2 = 2000
            elif key == ord("e"):
                ch_2 = 1000
            elif key == ord("i"):
                ch_1 = 2000
            elif key == ord("k"):
                ch_1 = 1000
            elif key == ord("x"):
                frame_name = f'frame_{frame_count}.png'
                cv2.imwrite(os.path.join(way_to_file_save, frame_name), camera_frame)
                print(f'Frame saved as {frame_name}')
                frame_count += 1

            pioneer_mini.send_rc_channels(
                channel_1=ch_1,
                channel_2=ch_2,
                channel_3=ch_3,
                channel_4=ch_4,
                channel_5=ch_5,
            )
            time.sleep(0.02)
finally:
    time.sleep(1)
    pioneer_mini.land()
    pioneer_mini.close_connection()
    del pioneer_mini
    cv2.destroyAllWindows()
