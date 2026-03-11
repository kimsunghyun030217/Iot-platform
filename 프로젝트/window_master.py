#진동이 3분의 2이상 되면...창문 오픈되도록 하는 코드

import requests
import time
import RPi.GPIO as GPIO

# 1. Mobius 서버 및 환경 설정
MOBIUS_IP = "114.71.220.59"
MOBIUS_PORT = "2017"
AE_NAME = "Smart_Classroom"

# 감시 대상 학번 리스트 (3명)
STUDENT_LIST = ["20221309", "20201528", "20221301"]
TOTAL_SEATS = len(STUDENT_LIST)

# 2. 하드웨어 설정: SG90 서보모터
WINDOW_SERVO_PIN = 18  # 서보모터 신호선을 GPIO 18번에 연결
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(WINDOW_SERVO_PIN, GPIO.OUT)

pwm = GPIO.PWM(WINDOW_SERVO_PIN, 50)
pwm.start(0)

def control_window(open_mode):
    """
    서보모터를 이용해 창문을 제어합니다.
    open_mode가 True면 90도 개방, False면 0도 폐쇄합니다.
    """
    if open_mode:
        print("\n[이벤트] 2/3 이상 졸음 발생! 창문을 개방합니다.")
        pwm.ChangeDutyCycle(7.5)  # 90도 개방 (서보모터 사양에 따라 조정 가능)
    else:
        print("\n[이벤트] 상태 호전. 창문을 닫습니다.")
        pwm.ChangeDutyCycle(2.5)  # 0도 폐쇄
    
    time.sleep(1)      # 서보모터 동작 대기
    pwm.ChangeDutyCycle(0)  # 서보모터 떨림 방지를 위한 신호 중단

def get_status(student_id):
    """
    Mobius 서버에서 특정 학생의 최신 상태(Latest)를 가져옵니다.
    """
    url = f"http://{MOBIUS_IP}:{MOBIUS_PORT}/Mobius/{AE_NAME}/{student_id}/la"
    headers = {
        "X-M2M-Origin": "SOrigin", 
        "Accept": "application/json"
    }
    try:
        res = requests.get(url, headers=headers, timeout=2)
        if res.status_code == 200:
            content = res.json()["m2m:cin"]["con"]
            return int(content)
    except Exception as e:
        print(f"[{student_id}] 데이터 수신 오류: {e}")
        return 0
    return 0

# 3. 메인 감시 루프
try:
    print(f"[{AE_NAME}] 마스터 시스템 가동 시작...")
    window_is_open = False

    while True:
        drowsy_count = 0
        
        # 각 학생의 상태 확인
        for student_id in STUDENT_LIST:
            status = get_status(student_id)
            if status == 1:  # 1을 '졸음 상태'라고 가정
                drowsy_count += 1
        
        print(f"현재 졸음 인원: {drowsy_count}/{TOTAL_SEATS}")

        # 전체 인원의 2/3 이상이 졸고 있을 때 (3명 중 2명 이상)
        if drowsy_count >= (TOTAL_SEATS * 2 / 3):
            if not window_is_open:
                control_window(True)
                window_is_open = True
        else:
            if window_is_open:
                control_window(False)
                window_is_open = False
        
        time.sleep(5)  # 5초 간격으로 모니터링

except KeyboardInterrupt:
    print("\n사용자에 의해 시스템이 종료되었습니다.")

finally:
    pwm.stop()
    GPIO.cleanup()
    print("GPIO 리소스가 정리되었습니다.")