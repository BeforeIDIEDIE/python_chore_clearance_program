import customtkinter as ctk
import os
import subprocess
import beautifulsoup4 as bs4
import pandas as pd
#HW관련 기능 메뉴

def BatteryReport():
    # 이거 리포트 크롤링 해서 현 용량, 디자인 용량, 현용량/디자인용량% 이런식으로 할거임
    try:
        subprocess.run("powercfg /batteryreport", shell=True, check=True)
        ctk.CTkMessageBox(title="성공", message="배터리 리포트가 생성되었습니다. (사용자 폴더에 저장됨)")
    except subprocess.CalledProcessError as e:
        ctk.CTkMessageBox(title="오류", message=f"배터리 리포트 생성 중 오류 발생: {e}")

def UsageAnalysis():
    #판다스 사용해서 주단위 사용시간 분석 리포트 만들예정
    #주단위 사용시간 보여줄거임
    try:
        subprocess.run("powercfg /energy", shell=True, check=True)
        ctk.CTkMessageBox(title="성공", message="사용시간 분석 리포트가 생성되었습니다. (사용자 폴더에 저장됨)")
    except subprocess.CalledProcessError as e:
        ctk.CTkMessageBox(title="오류", message=f"사용시간 분석 리포트 생성 중 오류 발생: {e}")

    

        