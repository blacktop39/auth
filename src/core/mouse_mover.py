import pyautogui
import random
import time
import sys
from datetime import datetime

# 안전장치 설정
pyautogui.FAILSAFE = True  # 마우스를 화면 구석으로 이동하면 프로그램 중지

def move_mouse_randomly():
    try:
        # 화면 해상도 얻기
        screen_width, screen_height = pyautogui.size()

        while True:
            # 랜덤한 위치 생성
            x = random.randint(0, screen_width)
            y = random.randint(0, screen_height)

            # 현재 시간 출력
            current_time = datetime.now().strftime("%H:%M:%S")
            print(f"[{current_time}] 마우스 이동: ({x}, {y})")

            # 마우스 부드럽게 이동 (duration은 이동하는데 걸리는 시간)
            pyautogui.moveTo(x, y, duration=1.5)

            # 다음 이동까지 대기 (5초)
            time.sleep(60)

    except KeyboardInterrupt:
        print("\n프로그램을 종료합니다.")
        sys.exit()
    except pyautogui.FailSafeException:
        print("\n안전장치가 작동되어 프로그램을 종료합니다.")
        sys.exit()

if __name__ == "__main__":
    print("마우스 자동 이동을 시작합니다...")
    print("프로그램을 종료하려면 Ctrl+C를 누르거나 마우스를 화면 구석으로 이동하세요.")
    move_mouse_randomly()
~                                                                                                                                                                                                               
~                                                                                                                                                                                                               
~                                                                                                                                                                                                               
~                                                                                                                                                                                                               
~                                                                                                                                                                                                               
~                                                                                                                                                                                                               
~                                                                                                                                                                                                               
~                                                                                                                                                                                                               