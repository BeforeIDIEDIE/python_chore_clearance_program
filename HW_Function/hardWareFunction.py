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
    

def UsageAnalysis():
    #판다스 사용해서 주단위 사용시간 분석 리포트 만들예정
    #주단위 사용시간 보여줄거임
    try:
        subprocess.run("powercfg /energy", shell=True, check=True)
        ctk.CTkMessageBox(title="성공", message="사용시간 분석 리포트가 생성되었습니다. (사용자 폴더에 저장됨)")
    except subprocess.CalledProcessError as e:
        ctk.CTkMessageBox(title="오류", message=f"사용시간 분석 리포트 생성 중 오류 발생: {e}")

    

        