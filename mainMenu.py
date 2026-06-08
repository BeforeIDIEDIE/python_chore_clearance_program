import customtkinter as ctk
from HW_Function import hardWareFunction as HWF # 하드웨어 기능제어파일 모둠
import sendingNotification #알림기능용 파일
import shuttingDown#꺼짐기능용 파일
import rubbishBinClear as RBC #휴지통 자동비우기 파일
import backGroundClear as BGC #바탕화면 정리 파일
#할일 리스트
#바탕화면 정리
#다운로드 화면 정리
#셋업 알림 리스트 만들어 보여주기-> 만드는 건 어렵진 않은데 어떻게 보여줘야 깔끔할지 모르겠음

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MainMenu(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("허드렛일 프로그램")
        self.geometry("600x500") # 입력창 배치를 위해 크기 살짝 조정

        self.remaining_shuttingDown_sec = 0 # 꺼짐예약이 몇초뒤에 실행되는지 보여줌

        # --- 1. 메인 메뉴 프레임 ---
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True)
        self.CreateMainMenu()

        # --- 2. 알림 설정 프레임  ---
        self.setup_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.CreateSetupScreen()

        # --- 3. 꺼짐 프레임 ---
        self.shuttingDown_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.CreateShuttingDownScreen()

        self.shuttingDownMessage = ctk.CTkLabel(self.main_frame, text="", font=("Pretendard", 30))
        self.shuttingDownMessage.pack(pady=20)

        # --- 4. 바탕화면 정리 프레임 ---
        self.backgroundClear_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.CreateBackgroundClearScreen()

        # --- 5. 하드웨어 기능 프레임 ---
        self.hardWare_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.CreateHardWareFunctionScreen()
        

#==============================================================================================================================================================================
        
    def CreateMainMenu(self):
        """메인 메뉴 화면 구성"""
        self.label = ctk.CTkLabel(self.main_frame, text="허드렛일 목록", font=("Pretendard", 30))
        self.label.pack(pady=30)

        # 각 버튼을 고유 변수로 지정하여 겹치지 않게 처리
        self.btn1 = ctk.CTkButton(self.main_frame, text="1. 알림 설정", command=self.ShowSetupScreen)
        self.btn1.pack(pady=15)

        #람다는 한줄짜리 익명함수임        
        self.btn2 = ctk.CTkButton(self.main_frame, text="2. 꺼짐 설정", command=self.ShowShuttingDownScreen)
        self.btn2.pack(pady=15)

        self.btn3 = ctk.CTkButton(self.main_frame, text="3. 바탕화면 정리", command=self.ShowBackgroundClearScreen)
        self.btn3.pack(pady=15)

        self.btn4 = ctk.CTkButton(self.main_frame, text="4. 하드웨어 관련", command=self.ShowHardWareFunctionScreen)
        self.btn4.pack(pady=15)
        
        #self.btn3 = ctk.CTkButton(
        #    self.main_frame,
        #    text="3. 휴지통 자동 비우기",
        #   command=self.ShowRubbishBinClearScreen,
        #)
        #self.btn3.pack(pady=15)

        
        #self.btn3 = ctk.CTkButton(self.main_frame, text="3. 다운로드 파일 정리", command=lambda: print("다운로드 정리"))
        #self.btn3.pack(pady=15)
        
        #self.btn4 = ctk.CTkButton(self.main_frame, text="4. 바탕화면 정리", command=lambda: print("바탕화면 정리"))
        #self.btn4.pack(pady=15)

    def ShowMainMenu(self):
        """기존 show_main_menu 수정 (모든 프레임을 언팩하도록 안전장치)"""
        self.setup_frame.pack_forget()
        self.shuttingDown_frame.pack_forget()
        self.backgroundClear_frame.pack_forget()
        #self.rubbishBinClear_frame.pack_forget()
        self.hardWare_frame.pack_forget()
        self.main_frame.pack(fill="both", expand=True)


#==============================================================================================================================================================================
        
    def CreateSetupScreen(self):
        """알림 설정 상세 화면 구성"""
        self.setup_label = ctk.CTkLabel(self.setup_frame, text="알림 세부 설정", font=("Pretendard", 24))
        self.setup_label.pack(pady=20)

        # 메시지 입력창 (20자 안내)
        ctk.CTkLabel(self.setup_frame, text="알림 메시지 (최대 20자)", font=("Pretendard", 14)).pack(pady=(10, 0))
        self.msg_entry = ctk.CTkEntry(self.setup_frame, width=350, placeholder_text="여따 입력")
        self.msg_entry.pack(pady=10)

        # 시간 입력 레이아웃 
        ctk.CTkLabel(self.setup_frame, text="예약 시간 설정", font=("Pretendard", 14)).pack(pady=(10, 0))
        
        time_frame = ctk.CTkFrame(self.setup_frame, fg_color="transparent")
        time_frame.pack(pady=10)

        self.min_entry = ctk.CTkEntry(time_frame, width=70, placeholder_text="0")
        self.min_entry.pack(side="left", padx=5)
        ctk.CTkLabel(time_frame, text="분", font=("Pretendard", 14)).pack(side="left", padx=(0, 15))

        self.sec_entry = ctk.CTkEntry(time_frame, width=70, placeholder_text="0")
        self.sec_entry.pack(side="left", padx=5)
        ctk.CTkLabel(time_frame, text="초", font=("Pretendard", 14)).pack(side="left")

        # 오류 및 상태 표시용 텍스트
        self.status_label = ctk.CTkLabel(self.setup_frame, text="", font=("Pretendard", 13))
        self.status_label.pack(pady=10)

        # 하단 버튼
        self.btn_save = ctk.CTkButton(self.setup_frame, text="예약 완료", fg_color="#2ecc71", hover_color="#27ae60", command=self.ConfirmAlarm)
        self.btn_save.pack(pady=15)

        self.btn_back = ctk.CTkButton(self.setup_frame, text="메인으로 돌아가기", fg_color="#e74c3c", hover_color="#c0392b", command=self.ShowMainMenu)
        self.btn_back.pack(pady=5)

    def ShowSetupScreen(self):
        """메인 메뉴 숨기고 설정창 열기"""
        self.status_label.configure(text="") # 상태창 초기화
        self.main_frame.pack_forget()
        self.setup_frame.pack(fill="both", expand=True)

    def ConfirmAlarm(self):
        """예약 완료 버튼을 눌렀을 때 검증 및 실행"""
        msg = self.msg_entry.get()
        min_str = self.min_entry.get() or "0"
        sec_str = self.sec_entry.get() or "0"

        # 1. 메시지 글자 수 체크 (20자 제한)
        if len(msg) > 20:
            self.status_label.configure(text="20글자 이하로만.....", text_color="#e74c3c")
            return
        if not msg.strip():
            self.status_label.configure(text="메시지 입력해줘.......", text_color="#e74c3c")
            return

        # 2. 시간 변환 및 검증
        try:
            minutes = float(min_str)
            seconds = float(sec_str)
            
            # 총 시간을 분 단위로 환산해서 독립 파일 함수에 전달
            total_sec = minutes*60 + seconds
             
            if total_sec <= 0:
                self.status_label.configure(text="0보단... 큰수로...", text_color="#e74c3c")
                return
                
        except ValueError:
            self.status_label.configure(text="시간엔 숫자만.......", text_color="#e74c3c")
            return

        # 3. 독립 파일(`sendingNotification.py`)의 예약 함수 호출
        sendingNotification.ReserveNotification(msg, total_sec)
        
        # 입력칸 청소 및 메인 복귀
        self.msg_entry.delete(0, 'end')
        self.min_entry.delete(0, 'end')
        self.sec_entry.delete(0, 'end')
        
        self.ShowMainMenu()
        
    def CreateShuttingDownScreen(self):
        """꺼짐 화면 구성 (self.shuttingDown_frame 사용)"""
        self.sd_label = ctk.CTkLabel(self.shuttingDown_frame, text="컴퓨터 꺼짐 예약", font=("Pretendard", 24))
        self.sd_label.pack(pady=20)

        ctk.CTkLabel(self.shuttingDown_frame, text="몇 분 몇 초 뒤에 끌지 입력하쇼", font=("Pretendard", 14)).pack(pady=(10, 0))
        
        time_frame = ctk.CTkFrame(self.shuttingDown_frame, fg_color="transparent")
        time_frame.pack(pady=10)

        self.min_entry_sd = ctk.CTkEntry(time_frame, width=70, placeholder_text="0")
        self.min_entry_sd.pack(side="left", padx=5)
        ctk.CTkLabel(time_frame, text="분", font=("Pretendard", 14)).pack(side="left", padx=(0, 15))

        self.sec_entry_sd = ctk.CTkEntry(time_frame, width=70, placeholder_text="0")
        self.sec_entry_sd.pack(side="left", padx=5)
        ctk.CTkLabel(time_frame, text="초", font=("Pretendard", 14)).pack(side="left")

        self.status_label_sd = ctk.CTkLabel(self.shuttingDown_frame, text="", font=("Pretendard", 13))
        self.status_label_sd.pack(pady=10)

        # 하단 버튼 구조
        self.btn_save_sd = ctk.CTkButton(self.shuttingDown_frame, text="종료 예약 완료", fg_color="#2ecc71", hover_color="#27ae60", command=self.ConfirmValidationShuttingDown)
        self.btn_save_sd.pack(pady=10)

        # 종료예약 취소버튼
        self.btn_cancel_sd = ctk.CTkButton(self.shuttingDown_frame, text="종료 예약 취소", fg_color="#f39c12", hover_color="#d35400", command=self.CancelShuttingDownJob)
        self.btn_cancel_sd.pack(pady=5)

        self.btn_back_sd = ctk.CTkButton(self.shuttingDown_frame, text="메인으로 돌아가기", fg_color="#e74c3c", hover_color="#c0392b", command=self.ShowMainMenu)
        self.btn_back_sd.pack(pady=5)

    def ShowShuttingDownScreen(self):
        """메인 메뉴 숨기고 꺼짐 설정창 열기"""
        self.status_label_sd.configure(text="") # 상태창 초기화
        self.main_frame.pack_forget()
        self.shuttingDown_frame.pack(fill="both", expand=True)

    def ConfirmValidationShuttingDown(self):
        """꺼짐 시간 검증 및 파일 호출"""
        min_str = self.min_entry_sd.get() or "0"
        sec_str = self.sec_entry_sd.get() or "0"
        
        try:     
            minutes = float(min_str)
            seconds = float(sec_str)
            total_sec = minutes * 60 + seconds

            if total_sec <= 0:
                self.status_label_sd.configure(text="0보단... 큰수로...", text_color="#e74c3c")
                return
                
        except ValueError:
            self.status_label_sd.configure(text="시간엔 숫자만.......", text_color="#e74c3c")
            return

        # shuttingDown.py 내부 함수 호출
        shuttingDown.ShuttingDown(int(total_sec))

        self.remaining_shuttingDown_sec = int(total_sec)
        self.UpdateShuttingDownTimer() 
        self.min_entry_sd.delete(0, 'end')
        self.sec_entry_sd.delete(0, 'end')
        self.ShowMainMenu()

    def CancelShuttingDownJob(self):
        """종료 취소 버튼 맵핑"""
        shuttingDown.CancelShuttingDown()
        self.remaining_shuttingDown_sec = 0
        self.shuttingDownMessage.configure(text="")
        self.ShowMainMenu()

    def UpdateShuttingDownTimer(self):
        if self.remaining_shuttingDown_sec > 0:
            m = self.remaining_shuttingDown_sec // 60 #파이썬에서 //은 나머지는 제외 몫만 남긴다
            s = self.remaining_shuttingDown_sec % 60
            
            # 메인 화면 텍스트 갱신
            self.shuttingDownMessage.configure(text=f"({m}분 {s}초 뒤 시스템 종료)")
            
            # 1초 감소
            self.remaining_shuttingDown_sec -= 1
            
            # 1000밀리초(1초) 뒤에 자기 자신(UpdateShuttingDownTimer)을 다시 호출
            self.after(1000, self.UpdateShuttingDownTimer)
        else:
            # 예약 시간이 끝나거나 취소되면 메인 제목 원상복구
            if self.remaining_shuttingDown_sec == 0:
                self.shuttingDownMessage.configure(text="")

#==============================================================================================================================================================================
    def CreateBackgroundClearScreen(self):
        self.bc_label = ctk.CTkLabel(self.backgroundClear_frame, text="바탕화면 정리", font=("Pretendard", 24))
        self.bc_label.pack(pady=20)

        self.btn_clear_bg = ctk.CTkButton(self.backgroundClear_frame, text="바탕화면 정리 실행", fg_color="#3498db", hover_color="#2980b9", command=self.ClearBackGround)
        self.btn_clear_bg.pack(pady=30)

        self.btn_back_bc = ctk.CTkButton(self.backgroundClear_frame, text="메인으로 돌아가기", fg_color="#e74c3c", hover_color="#c0392b", command=self.ShowMainMenu)
        self.btn_back_bc.pack(pady=30)

    def ShowBackgroundClearScreen(self):
        self.main_frame.pack_forget()
        self.backgroundClear_frame.pack(fill="both", expand=True)
    
    def ClearBackGround(self):
        BGC.ClearBackGround()#바탕화면 정리 함수 호출
        self.ShowMainMenu()

#==============================================================================================================================================================================
    #휴지통 자동 비우기 안쓰는 기능임 | 필요하면 나중에 추가할듯
    def CreateRubbishBinClearScreen(self):
        #각 버튼 토글 쓸거임 |기능 비활성화 | 10일 | 30일
        self.rb_label = ctk.CTkLabel(
            self.rubbishBinClear_frame,
            text="휴지통 자동 비우기 설정",
            font=("Pretendard", 24),
        )
        self.rb_label.pack(pady=20)

        self.current_period_label = ctk.CTkLabel(
            self.rubbishBinClear_frame,
            text="현재 설정된 주기: 불러오는 중...",
            font=("Pretendard", 15),
        )
        self.current_period_label.pack(pady=10)

        self.seg_button = ctk.CTkSegmentedButton(
            self.rubbishBinClear_frame,
            values=["기능 비활성화", "10일", "30일"],
            command=self.OnToggleChanged,
            font=("Pretendard", 14),
        )
        self.seg_button.pack(pady=20, padx=20)

        self.btn_back_rb = ctk.CTkButton(
            self.rubbishBinClear_frame,
            text="메인으로 돌아가기",
            fg_color="#e74c3c",
            hover_color="#c0392b",
            command=self.ShowMainMenu,
        )
        self.btn_back_rb.pack(pady=30)

    def ShowRubbishBinClearScreen(self):
        current_setting, next_clear_date = RBC.LoadInfo()

        if current_setting == 0:
            self.current_period_label.configure(
                text="현재 설정: 자동 비우기가 꺼져 있습니다."
            )
            self.seg_button.set("기능 비활성화")
        else:
            self.current_period_label.configure(
                text=f"현재 설정: {current_setting}일 마다 비우기\n(다음 비우기 날짜: {next_clear_date})"
            )
            self.seg_button.set(f"{current_setting}일")

        self.main_frame.pack_forget()
        self.rubbishBinClear_frame.pack(fill="both", expand=True)

    def OnToggleChanged(self, value):
        #파이썬에서 if문 내부 스코프에서 변수를 생성하고 if문 내부에서 변수를 사용시 에러가 일어나지 않는다!!!같은 모듈내부라면 별도의 스코프 존재하지 않
        if value == "기능 비활성화":
            days = 0
        elif value == "10일":
            days = 10
        elif value == "30일":
            days = 30

        next_date = RBC.SetRubbishBinClearDate(days)

        if days == 0:
            self.current_period_label.configure(
                text="설정이 변경되었습니다: 자동 비우기 해제"
            )
        else:
            self.current_period_label.configure(
                text=f"설정이 변경되었습니다: {days}일 주기\n(다음 비우기 날짜: {next_date})"
            )
#==============================================================================================================================================================================
    def CreateHardWareFunctionScreen(self):
        self.label = ctk.CTkLabel(self.hardWare_frame, text="하드웨어 관련 기능", font=("Pretendard", 30))
        self.label.pack(pady=30)

        self.btn1 = ctk.CTkButton(self.hardWare_frame, text="1. 배터리 리포트", command=self.ShowBatteryReport)
        self.btn1.pack(pady=15)

        self.btn2 = ctk.CTkButton(self.hardWare_frame, text="2. 사용시간 분석", command=self.ShowUsageAnalysis)
        self.btn2.pack(pady=15)

        self.btn_back = ctk.CTkButton(self.hardWare_frame, text="메인으로 돌아가기", fg_color="#e74c3c", hover_color="#c0392b", command=self.ShowMainMenu)
        self.btn_back.pack(pady=30)

    def ShowHardWareFunctionScreen(self):
        self.main_frame.pack_forget()
        self.hardWare_frame.pack(fill="both", expand=True)

    def ShowBatteryReport(self):
        result = HWF.BatteryReport()
        # 해당부분에 결과를 보여주는 창 띄우는 코드 추가해야됨
    def ShowUsageAnalysis(self):
        HWF.UsageAnalysis()
        
if __name__ == "__main__":
    app = MainMenu()
    app.mainloop()
