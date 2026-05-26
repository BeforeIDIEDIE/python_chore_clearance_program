import sys
import os
from plyer import notification
import threading
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                             QLineEdit, QPushButton, QLabel, QHBoxLayout)
from PyQt6.QtCore import Qt

def ShuttingDown(times):
    os.system(f"shutdown /s /t {times}")

def CancelShuttingDown():
    os.system("shutdown /a")
    SendCancelShuttingDown()

def SendCancelShuttingDown():
    notification.notify(
        title="꺼짐 예약취소",
        message="꺼짐 예약이 취소됨",
        app_name="허드렛일...프로그램!",
        timeout=10  # 알림이 유지되는 시간(초)
    )
