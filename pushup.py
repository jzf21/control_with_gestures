import cv2 as cv
import numpy as np
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
from cvzone.HandTrackingModule import HandDetector
import pyautogui


# Function to set the speaker volume
def set_speaker_volume(volume):
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume_interface = session._ctl.QueryInterface(ISimpleAudioVolume)
        volume_interface.SetMasterVolume(volume, None)


cap = cv.VideoCapture(0)
hd = HandDetector()
val = 0
count = 0
while 1:
    _, img = cap.read()
    hands, img = hd.findHands(img)

    if hands:
        lm = hands[0]["lmList"]
        # get distance between point 0 and middle finger
        # only works if  fists are clenched

        length2, info2, img = hd.findDistance(lm[0][0:2], lm[12][0:2], img)

        print(length2)

        if length2 < 60:
            length, info, img = hd.findDistance(lm[8][0:2], lm[4][0:2], img)
            volume = np.interp(
                length, [25, 145], [0, 1]
            )  # Interpolate the volume between 0 and 1
            set_speaker_volume(volume)

            cv.rectangle(img, (20, 150), (85, 400), (0, 255, 255), 4)
            cv.rectangle(img, (20, int(val)), (85, 400), (0, 0, 255), -1)
            cv.putText(
                img,
                f"{int(volume * 100)}%",
                (20, 430),
                cv.FONT_HERSHEY_COMPLEX,
                1,
                (255, 0, 0),
                3,
            )
        else:
            length3, info3, img = hd.findDistance(lm[8][0:2], lm[4][0:2], img)
            if length3 < 50 and count == 0:
                count = 1
                pyautogui.keyDown("playpause")
                print("space")

            elif count == 1 and length3 > 100:
                count = 0
                pyautogui.keyDown("playpause")
                print("space up")

        for hand in hands:
            for i, lm in enumerate(hand["lmList"]):
                x, y = lm[0:2]
                cv.circle(img, (x, y), 8, (255, 0, 0), cv.FILLED)
                cv.putText(
                    img, str(i), (x + 10, y), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1
                )

    cv.imshow("frame", img)
    if cv.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
        break

cv.destroyAllWindows()
