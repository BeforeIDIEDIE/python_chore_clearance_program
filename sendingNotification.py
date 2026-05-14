from win10toast import ToastNotifier
import threading

def send_toast(message):
    toaster = ToastNotifier()
    toaster.show_toast(
        "허드렛일 예약 알림",
        message,
        duration=10,
        threaded=True
    )

def print_message(msg,time):
    try:
        timer = threading.Timer(time, send_toast, args = [msg])
        timer.start()
        return True
    except ValueError:
        return False
