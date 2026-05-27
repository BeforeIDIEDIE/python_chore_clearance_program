from plyer import notification
import threading

def SendToast(message):
    """plyer를 사용하여 윈도우 알림창을 띄우는 함수 (Python 3.13 호환)"""
    notification.notify(
        title="허드렛일 예약 알림",
        message=message,
        app_name="허드렛일 프로그램",
        timeout=10  # 알림이 유지되는 시간(초)
    )

def ReserveNotification(msg, seconds):
    """메인 메뉴에서 넘겨받은 초(seconds)만큼 대기 후 알림을 실행하는 스레드 타이머"""
    try:
        # 백그라운드에서 지정된 초만큼 대기 후 send_toast(msg) 실행
        timer = threading.Timer(seconds, SendToast, args=[msg])
        timer.start()
        return True
    except Exception:
        return False
