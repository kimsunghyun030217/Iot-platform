#졸음 감지 -> mysql

import cv2
import time

# Haar Cascade 파일 경로 설정
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')

# 카메라 열기
cap = cv2.VideoCapture(0)

# 졸음 감지 기준 설정
EYE_CLOSE_DURATION_THRESHOLD = 2  # 눈을 감은 지속 시간 임계값 (초)
MIN_EYE_SIZE = 10  # 눈의 최소 크기 (픽셀)
start_time = None

while True:
    ret, frame = cap.read()
    if not ret:
        print("프레임을 읽을 수 없습니다.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 얼굴 감지
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        # 눈 감지
        eyes = eye_cascade.detectMultiScale(roi_gray)
        eyes = eyes[:2]  # 최대 2개의 눈만 사용
        if len(eyes) == 0:
            if start_time is None:
                start_time = time.time()
            else:
                elapsed_time = time.time() - start_time
                if elapsed_time > EYE_CLOSE_DURATION_THRESHOLD:
                    cv2.putText(frame, "졸음", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        else:
            start_time = None  # 눈이 감지되면 타이머 초기화

        for (ex, ey, ew, eh) in eyes:
            # 눈의 너비와 높이가 최소 크기보다 큰 경우에만 표시
            if ew > MIN_EYE_SIZE and eh > MIN_EYE_SIZE:
                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

    cv2.imshow('Camera Streaming', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

