# 😴 Smart Drowsiness Classroom

> **OpenCV와 IoT를 활용한 실시간 졸음 감지 및 스마트 교실 제어 시스템**

수업 중 학생의 눈 상태를 실시간으로 분석하여 졸음을 감지하고,  
졸음이 감지된 학생에게는 **의자 진동을 통해 개별 알림**을 제공합니다.

또한 교실 전체 학생의 졸음 상태를 모니터링하여  
**전체 수업 인원의 1/3 이상이 졸음 상태로 판단될 경우 서보모터를 이용해 창문을 자동으로 개방**하도록 구현한 IoT 기반 스마트 교실 프로젝트입니다.

---

## 🌟 Project Overview

장시간 진행되는 수업에서는 학생들의 집중력이 떨어지면서
졸음으로 인해 학습 효율이 저하될 수 있습니다.

기존의 단순한 졸음 감지 시스템을 넘어,
학생 개인의 졸음 상태뿐만 아니라 **교실 전체의 집중 상태를 파악하고
실제 환경을 자동으로 제어하는 스마트 교실**을 구현하고자 했습니다.

OpenCV를 활용하여 카메라 영상에서 학생의 얼굴과 눈 영역을 검출하고, 눈의 상태 변화를 기반으로 졸음 여부를 판단합니다.

졸음이 감지되면 해당 학생의 의자에 설치된 진동 장치를 작동시켜
개별적으로 졸음을 깨울 수 있도록 하였으며,

전체 수업 인원의 **1/3 이상에서 졸음이 감지될 경우**
교실 환경에도 문제가 있다고 판단하여
서보모터로 창문을 자동 개방하도록 구현했습니다.

---

## ✨ Key Features

### 👁️ Real-time Drowsiness Detection

- 카메라를 통한 실시간 영상 입력
- 학생 얼굴 및 눈 영역 검출
- 눈의 열림 / 감김 상태 분석
- 일정 시간 동안의 상태 변화를 기반으로 졸음 여부 판단

### 📳 Individual Vibration Alert

- 특정 학생의 졸음 상태 감지
- 해당 학생의 의자에 설치된 진동 장치 작동
- 주변 학생에게 영향을 최소화하면서 개별적으로 졸음 알림 제공

### 🪟 Automatic Classroom Ventilation

- 수업 중 전체 학생의 졸음 상태 집계
- **전체 인원의 1/3 이상이 졸음 상태일 경우 환경 제어 조건 충족**
- 서보모터를 이용하여 교실 창문 자동 개방
- 교실 환기를 통한 학습 환경 개선

### 🎯 Detection Logic Improvement

- 순간적인 눈 깜빡임과 지속적인 눈 감김 구분
- 얼굴 및 눈 검출 실패에 따른 오판단 감소
- 실제 환경에서의 테스트를 통해 눈 검출 로직 개선
- 연속적인 상태 변화를 고려하여 졸음 판별 정확도 향상

---

## 🔄 System Flow

```text
                     Camera
                        │
                        ▼
                 실시간 영상 입력
                        │
                        ▼
                얼굴 및 눈 검출
                        │
                        ▼
                   눈 상태 분석
                        │
                        ▼
                  졸음 여부 판단
                        │
             ┌──────────┴──────────┐
             │                     │
             ▼                     ▼
       개인 졸음 상태          전체 졸음 상태 집계
             │                     │
             ▼                     ▼
      해당 학생 의자          전체 인원의 1/3 이상?
       진동 장치 ON                  │
                                   │ YES
                                   ▼
                              Servo Motor
                                   │
                                   ▼
                              창문 자동 개방
                                   │
                                   ▼
                                교실 환기
```



---

## 🏫 Classroom Control Logic

졸음 감지 결과는 개인 알림과 교실 환경 제어에 각각 사용됩니다.

```text
학생 A  😴
학생 B  🙂
학생 C  😴
학생 D  🙂
학생 E  😴
학생 F  🙂

졸음 학생 : 3명
전체 학생 : 6명

3 / 6 = 50%

          ↓

졸음 학생 비율 ≥ 1/3

          ↓

Servo Motor 작동

          ↓

교실 창문 OPEN
```

이를 통해 특정 학생의 문제에는 **개별 진동 알림**으로 대응하고,
다수의 학생에게 동시에 졸음이 발생하면 **교실 환경 자체를 조절**하도록 설계했습니다.

---

## ⚙️ Tech Stack

### Programming

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

### Computer Vision

![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)

`Face Detection` `Eye Detection` `Image Processing`

### IoT / Embedded

![Raspberry Pi](https://img.shields.io/badge/Raspberry_Pi-A22846?style=for-the-badge&logo=raspberrypi&logoColor=white)

### Hardware

`Camera` `Vibration Motor` `Servo Motor`
---

## 📂 Repository Structure

```text
Iot-platform
│
├── 과제/
│   └── IoT 플랫폼 전공 수업 과제
│
├── 라즈베리파이 실습/
│   └── Raspberry Pi 실습 코드
│
└── 프로젝트/
    └── Smart Drowsiness Classroom
```

---

## 💡 What I Learned

이 프로젝트를 통해 카메라에서 입력되는 영상 데이터를 분석하는
컴퓨터 비전 기술과 실제 하드웨어 제어를 하나의 시스템으로 연결했습니다.

특히 졸음 감지 결과를 단순히 화면에 표시하는 데 그치지 않고,

**졸음 감지 → 개인 진동 알림 → 전체 상태 집계 → 교실 환경 제어**

까지 연결하면서 소프트웨어의 판단 결과가 실제 환경의 동작으로
이어지는 IoT 시스템을 구현했습니다.

또한 실제 테스트 과정에서 발생한 눈 검출 오차를 확인하고
판단 로직을 수정하면서 **실제 환경에서 발생하는 데이터의 불확실성을
고려한 로직 설계의 중요성**을 경험했습니다.

---

## 🎯 Project Goal

> **학생 개인의 상태와 교실 전체의 상태를 함께 분석하여  
> 능동적으로 학습 환경을 개선하는 스마트 교실 구현**

컴퓨터 비전을 이용한 졸음 감지와 IoT 하드웨어 제어를 결합하여
학생 개인에게는 즉각적인 피드백을 제공하고,
다수의 학생에게 동시에 졸음이 발생하는 경우에는
교실 환경까지 자동으로 조절하는 것을 목표로 구현했습니다.
