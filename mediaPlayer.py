import cv2
import mediapipe as mp
import pyautogui
import time
import pygetwindow as gw
import ctypes


def count_fingers(lst):
    cnt = 0

    thresh = (lst.landmark[0].y*100 - lst.landmark[9].y*100)/2
    print("thresh value", thresh)

    if (lst.landmark[5].y*100 - lst.landmark[8].y*100) > thresh:
        cnt += 1

    if (lst.landmark[9].y*100 - lst.landmark[12].y*100) > thresh:
        cnt += 1

    if (lst.landmark[13].y*100 - lst.landmark[16].y*100) > thresh:
        cnt += 1

    if (lst.landmark[17].y*100 - lst.landmark[20].y*100) > thresh:
        cnt += 1

    if (lst.landmark[5].x*100 - lst.landmark[4].x*100) > 6:
        cnt += 1

    return cnt
    #  --------------------------------
    # Use this if needed
    # ---------------------------------
# def take_screenshot():
#     active_window = gw.getActiveWindow()
#     x, y, width, height = active_window.left, active_window.top, active_window.width, active_window.height

#     screenshot = pyautogui.screenshot(region=(x, y, width, height))

#     timestamp = time.strftime("%Y%m%d%H%M%S")
#     screenshot_path = f"screenshot_{timestamp}.png"
#     screenshot.save(screenshot_path)

#     ctypes.windll.user32.MessageBoxW(active_window._hWnd, f"Screenshot saved as {screenshot_path}", "Screenshot Saved", 1)


def distance_between_points(p1, p2):
    return ((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2) ** 0.5


def interact_with_window(action):
    active_window = gw.getActiveWindow()

    if action == "minimize":
        active_window.minimize()
    elif action == "maximize":
        active_window.maximize()
    elif action == "restore":
        active_window.restore()
    elif action == "close":
        active_window.close()
    elif action == "get_info":
        print("Window Title:", active_window.title)
        print("Position:", (active_window.left, active_window.top))
        print("Size:", (active_window.width, active_window.height))


cap = cv2.VideoCapture(0)

drawing = mp.solutions.drawing_utils
hands = mp.solutions.hands
hand_obj = hands.Hands(max_num_hands=1)

start_init = False
prev = -1

while True:
    end_time = time.time()
    
     # Capture and flip the video frame
    _, frm = cap.read()
    frm = cv2.flip(frm, 1)
    
    
    
    # Process the frame with hand tracking
    res = hand_obj.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))

    if res.multi_hand_landmarks:
        hand_keyPoints = res.multi_hand_landmarks[0]
        cnt = count_fingers(hand_keyPoints)

        if not (prev == cnt):
            if not (start_init):
                start_time = time.time()
                start_init = True

            elif abs(end_time-start_time) > 0.2:
                print("Current finger count:", cnt)
                if (cnt == 1):
                    pyautogui.press("right")
                    print("Right Pressed")

                elif (cnt == 2):
                    thumb_tip = hand_keyPoints.landmark[4]
                    index_tip = hand_keyPoints.landmark[8]
                    distance = distance_between_points(thumb_tip, index_tip)

                    if distance < 0.3:
                        interact_with_window("minimize")
                        print(f"Gesture: Min Window, Distance: {distance}")

                    elif distance > 0.3:
                        interact_with_window("maximize")
                        

                elif (cnt == 3):
                    pyautogui.press("up")

                elif (cnt == 4):
                    pyautogui.press("down")

                elif (cnt == 5):
                    pyautogui.press("space")

                prev = cnt
                start_init = False

        drawing.draw_landmarks(frm, hand_keyPoints, hands.HAND_CONNECTIONS)

    cv2.imshow("window", frm)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()
