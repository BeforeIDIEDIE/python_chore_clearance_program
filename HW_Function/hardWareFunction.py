from bs4 import BeautifulSoup
import customtkinter as ctk
import os
import subprocess
import bs4 #beautifulsoup4는 bs4 라는 별칭으로 써야됨, html파싱 라이브러리~
import pandas as pd

#HW관련 기능 메뉴

def BatteryReport():
    # 이거 리포트 크롤링 해서 현 용량, 디자인 용량, 현용량/디자인용량% 이런식으로 할거임
    report_filename = "battery_report.html"
    battery_data = {}
    
    #행여나 기존의 리포트파일 참조를 방지하기 위해
    if os.path.exists(report_filename):
        try:
            os.remove(report_filename)
        except OSError:
            print(f"{report_filename} 파일을 삭제하지 못했습니다. 파일이 열려있을 수 있습니다.")
            return battery_data
        
    # 1. Windows 명령어를 실행하여 배터리 리포트 HTML 생성
    # powercfg == 윈도우에서 전원 설정과 관련된 명령어를 실행할 수 있는 유틸리티임
    # /batteryreport == 배터리 리포트 생성 명령어
    # /output == 리포트 저장 경로 지정
    subprocess.run(["powercfg", "/batteryreport", "/output", report_filename], shell=True, stdout=subprocess.DEVNULL)
    
    if not os.path.exists(report_filename):
        print("리포트 파일을 생성하지 못했습니다.")
        return battery_data

    # 2. HTML 파일 읽기
    try:
        with open(report_filename, "r", encoding="utf-8", errors="ignore") as f:
            html_content = f.read()
        
        soup = BeautifulSoup(html_content, "html.parser")
        
        # 3. "DESIGN CAPACITY"가 포함된 테이블 탐색 및 데이터 추출
        tables = soup.find_all("table")
        target_table = None
        for table in tables:
            if "DESIGN CAPACITY" in table.get_text().upper():
                target_table = table
                break
                
        if target_table:
            rows = target_table.find_all("tr")
            for row in rows:
                #STRIP() == 문자열의 양쪽 끝에서 공백 제거하는 메서드임
                #find_all(["td", "th"]) == <td>와 <th> 태그를 모두 찾는 메서드임
                cols = [col.get_text().strip() for col in row.find_all(["td", "th"])]
                if len(cols) >= 2 and cols[0]:#리포트상 그럴일은 없지만 만에하나 두개 이하의 열을 포함하는 데이터가 있는경우
                    if "BATTERY" in cols[0].upper():
                        continue
                    battery_data[cols[0]] = cols[1]
                    
    finally:#해당 구문은 TRY가 선행되어야하며 TRY구문에서 예외가 발생하더라도 반드시 실행됨
        if os.path.exists(report_filename):
            try:
                os.remove(report_filename)
            except OSError:
                pass
                
    return battery_data

#배터리 리포트 결과를 보여주는 팝업창 띄우는 함수
#재사용할수도 있어서 배터리 리포트 결과를 보여주는 팝업창 띄우는 함수는 따로 빼놓음
def OpenBatteryResultPopup(parent, battery_data):

    popup = ctk.CTkToplevel(parent)
    popup.title("배터리 리포트 결과")
    popup.geometry("400x450")
    popup.attributes("-topmost", True)  # 항상 위 설정
    
    # 타이틀 레이블
    title_label = ctk.CTkLabel(popup, text="🔋 배터리 분석 결과", font=("Pretendard", 20, "bold"))
    title_label.pack(pady=(20, 10))
    
    # 딕셔너리 데이터를 예쁜 문자열 포맷으로 변환
    report_text = "====================================\n"
    report_text += "        BATTERY REPORT DETAILS      \n"
    report_text += "====================================\n\n"
    
    
    # 매개변수 battery_data의 아이템들을 순회
    for key, value in battery_data.items():
        report_text += f"▶ {key:<15} : {value}\n\n"
        if key.upper() == "DESIGN CAPACITY":
            design_capacity = float("".join(filter(str.isdigit, value)))
            #"".join~뭐시기 이리썼는데 ""안의 문자를 구분자로 리스트의 요소들을 하나의 문자열로 합치는 메서드임
        if key.upper() == "FULL CHARGE CAPACITY":
            full_charge_capacity = float("".join(filter(str.isdigit, value)))
    if design_capacity and full_charge_capacity:
        percentage = (full_charge_capacity / design_capacity) * 100
        report_text += f"▶ BATTERY HEALTH : {percentage:.2f}%\n\n"
        match True:
            case _ if percentage >= 85:
                report_text += "배터리 양호\n"
            case _ if percentage >= 80:
                report_text += "배터리 보통\n"
            case _ if percentage >= 70:
                report_text += "배터리 주의\n"
            case _:
                report_text += "배터리 나쁨\n"
    report_text += "===================================="

    # 텍스트 상자 생성 및 데이터 삽입
    result_textbox = ctk.CTkTextbox(popup, width=350, height=260, font=("Pretendard", 14))
    result_textbox.pack(pady=10, padx=20)
    
    result_textbox.insert("0.0", report_text)
    result_textbox.configure(state="disabled")  # 읽기 전용으로 잠금
        
    # 닫기 버튼
    close_button = ctk.CTkButton(popup, text="확인", fg_color="#3498db", hover_color="#2980b9", command=popup.destroy)
    close_button.pack(pady=(10, 20))


def UsageAnalysis(parent):
    """사용시간 및 에너지 분석 리포트 생성 (관리자 권한 필요, 약 60초 소요)"""
    # CustomTkinter 표준에 맞춘 간단한 상태창 알림 팝업 함수
    def show_alert(title, message):
        alert = ctk.CTkToplevel(parent)
        alert.title(title)
        alert.geometry("350x150")
        alert.attributes("-topmost", True)
        ctk.CTkLabel(alert, text=message, font=("Pretendard", 13), wraplength=300).pack(pady=30)
        ctk.CTkButton(alert, text="확인", width=100, command=alert.destroy).pack()

    try:
        # 주석: powercfg /energy 명령어는 기본적으로 60초 동안 시스템을 관찰하므로 멈춘 것처럼 보일 수 있음
        subprocess.run("powercfg /energy /output energy_report.html", shell=True, check=True, stdout=subprocess.DEVNULL)
        show_alert("성공", "사용시간(에너지) 분석 리포트가 현재 폴더에 energy_report.html 파일로 생성되었습니다.")
    except subprocess.CalledProcessError as e:
        show_alert("오류", "리포트 생성에 실패했습니다.\n(이 기능은 '관리자 권한'으로 실행해야 합니다.)")

def UsageAnalysis():
    #판다스 사용해서 주단위 사용시간 분석 리포트 만들예정
    #주단위 사용시간 보여줄거임
    try:
        subprocess.run("powercfg /energy", shell=True, check=True)
        ctk.CTkMessageBox(title="성공", message="사용시간 분석 리포트가 생성되었습니다. (사용자 폴더에 저장됨)")
    except subprocess.CalledProcessError as e:
        ctk.CTkMessageBox(title="오류", message=f"사용시간 분석 리포트 생성 중 오류 발생: {e}")

    

        