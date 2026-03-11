
#눈이 인식되는지 테스트하는 코드

import cv2
import time
import mysql.connector
import RPi.GPIO as GPIO

# MySQL 연결 설정
mydb = mysql.connector.connect(
  host="localhost",      # MySQL 서버 호스트
  user="root",           # MySQL 사용자 이름
  password="1234",       # MySQL 비밀번호
  database="database_b"   # 사용할 데이터베이스
)

mycursor = mydb.cursor()

# Haar Cascade 파일 경로 설정
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')

# GPIO 핀 설정
VIBRATION_SENSOR_PIN = 17

# GPIO 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(VIBRATION_SENSOR_PIN, GPIO.OUT)

def vibe_on():
    GPIO.output(VIBRATION_SENSOR_PIN, GPIO.HIGH)
    print("진동 센서 켜짐")

def vibe_off():
    GPIO.output(VIBRATION_SENSOR_PIN, GPIO.LOW)
    print("진동 센서 꺼짐")

# 졸음 감지 기준 설정
MIN_EYE_SIZE = 20  # 눈의 최소 크기 (픽셀)
start_time = None
eye_closed_time = 3  # 눈을 감은 지속 시간 초기값 (초)

try:
    cap = cv2.VideoCapture(0)

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
                # 눈이 감지되지 않은 경우
                cv2.putText(frame, "close", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                eye_closed_time += 1  # 눈을 감은 시간을 1초씩 증가
                if eye_closed_time >= 3:
                    # 눈을 감은 시간이 3초 이상인 경우 진동 센서 활성화
                    vibe_on()
                    sql = "INSERT INTO sleep_detection (status) VALUES (%s)"
                    val = (1,)
                    mycursor.execute(sql, val)
                    mydb.commit()


            else:
                # 눈이 감지된 경우
                cv2.putText(frame, "open", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                # MySQL에 값 쓰기
                sql = "INSERT INTO sleep_detection (status) VALUES (%s)"
                val = (0,)
                mycursor.execute(sql, val)
                mydb.commit()
                eye_closed_time = 1  # 눈을 감은 시간을 1초로 초기화
                vibe_off()  # 눈이 열렸으니 진동 센서를 꺼줍니다.

            for (ex, ey, ew, eh) in eyes:
                # 눈의 너비와 높이가 최소 크기보다 큰 경우에만 표시
                if ew > MIN_EYE_SIZE and eh > MIN_EYE_SIZE:
                    cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

        cv2.imshow('Camera Streaming', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("프로그램 종료")

finally:
    # 데이터베이스의 값 1부터 리셋
    mycursor.execute("ALTER TABLE sleep_detection AUTO_INCREMENT = 1")
    mydb.commit()
    # GPIO 설정 초기화
    GPIO.cleanup()
    # 카메라 종료
    cap.release()
    cv2.destroyAllWindows()
