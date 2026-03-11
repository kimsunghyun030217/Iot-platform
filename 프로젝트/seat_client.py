#최종 프로젝트용 (각 자리마다 라즈베리파이 존재)

import cv2
import time
import requests
import RPi.GPIO as GPIO

# --- [Mobius 및 좌석 설정] ---
MOBIUS_IP = "114.71.220.59"
MOBIUS_PORT = "2017"
AE_NAME = "Smart_Classroom"  
MY_STUDENT_ID = "sch20221309"  # 본인 학번에 맞게 수정

MOBIUS_URL = f"http://{MOBIUS_IP}:{MOBIUS_PORT}/Mobius/{AE_NAME}/{MY_STUDENT_ID}"

HEADERS = {
    "Accept": "application/json",
    "X-M2M-RI": "12345",
    "X-M2M-Origin": f"S{AE_NAME}",
    "Content-Type": "application/vnd.onem2m-res+json; ty=4"
}

# --- [하드웨어 설정] ---
VIBRATION_PIN = 17
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(VIBRATION_PIN, GPIO.OUT)

# --- [인식 엔진 및 기준 설정] ---
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')

EYE_CLOSE_THRESHOLD = 3.0  # 3초 이상 감을 시 졸음 판정
start_time = None
is_sleeping = False

def send_to_mobius(status):
    try:
        payload = {"m2m:cin": {"con": str(status)}}
        requests.post(MOBIUS_URL, json=payload, headers=HEADERS, timeout=1)
    except:
        print("Mobius 전송 실패 (네트워크 확인 필요)")

def vibe_control(on_off):
    GPIO.output(VIBRATION_PIN, GPIO.HIGH if on_off else GPIO.LOW)

try:
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret: break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        eyes_detected = False

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            
            # 눈 감지 (이미지처럼 사각형 표시를 위해 튜닝)
            eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 10)
            
            if len(eyes) >= 2: # 두 눈이 모두 보일 때만 open으로 간주 (더 정확한 판별)
                eyes_detected = True
                for (ex, ey, ew, eh) in eyes:
                    # 이미지와 동일한 초록색 사각형 표시
                    cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
                # 이미지와 동일한 위치에 "open" 표시
                cv2.putText(frame, "open", (x + int(w/2) - 20, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            else:
                # 눈이 안 보일 때 "close" 표시
                cv2.putText(frame, "close", (x + int(w/2) - 20, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # --- 졸음 판단 및 액션 ---
        if not eyes_detected:
            if start_time is None:
                start_time = time.time()
            elif time.time() - start_time >= EYE_CLOSE_THRESHOLD:
                if not is_sleeping:
                    vibe_control(True)
                    send_to_mobius(1)
                    is_sleeping = True
        else:
            if is_sleeping:
                vibe_control(False)
                send_to_mobius(0)
                is_sleeping = False
            start_time = None

        cv2.imshow('Drowsiness Check', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): break

finally:
    GPIO.cleanup()
    cap.release()
    cv2.destroyAllWindows()