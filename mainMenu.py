import customtkinter as ctk
import sendingNotification #알림기능용 파일

#할일 리스트
#바탕화면 정리
#다운로드 화면 정리
#셋업 알림 리스트 만들어 보여주기-> 만드는 건 어렵진 않은데 어떻게 보여줘야 깔끔할지 모르겠음

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("허드렛일 프로그램")
        self.geometry("600x500") # 입력창 배치를 위해 크기 살짝 조정

        # --- 1. 메인 메뉴 프레임 ---
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True)
        self.create_main_menu()

        # --- 2. 알림 설정 프레임  ---
        self.setup_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.create_setup_screen()

        # --- 3. 꺼짐 프레임 ---

    def create_main_menu(self):
        """메인 메뉴 화면 구성"""
        self.label = ctk.CTkLabel(self.main_frame, text="허드렛일 목록", font=("Pretendard", 30))
        self.label.pack(pady=30)

        # 각 버튼을 고유 변수로 지정하여 겹치지 않게 처리
        self.btn1 = ctk.CTkButton(self.main_frame, text="1. 알림 설정", command=self.show_setup_screen)
        self.btn1.pack(pady=15)

        #람다는 한줄짜리 익명함수임        
        self.btn2 = ctk.CTkButton(self.main_frame, text="2. 꺼짐 설정", command=lambda: print("꺼짐 설정"))
        self.btn2.pack(pady=15)
        
        self.btn3 = ctk.CTkButton(self.main_frame, text="3. 다운로드 파일 정리", command=lambda: print("다운로드 정리"))
        self.btn3.pack(pady=15)
        
        self.btn4 = ctk.CTkButton(self.main_frame, text="4. 바탕화면 정리", command=lambda: print("바탕화면 정리"))
        self.btn4.pack(pady=15)

    def create_setup_screen(self):
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
        self.btn_save = ctk.CTkButton(self.setup_frame, text="예약 완료", fg_color="#2ecc71", hover_color="#27ae60", command=self.confirm_alarm)
        self.btn_save.pack(pady=15)

        self.btn_back = ctk.CTkButton(self.setup_frame, text="메인으로 돌아가기", fg_color="#e74c3c", hover_color="#c0392b", command=self.show_main_menu)
        self.btn_back.pack(pady=5)

    def create_shutDown_screen(self):#작업중 끝남...................
        """꺼짐 화면 구성"""
        self.setup_label = ctk.CTkLabel(self.setup_frame, text="꺼짐 시간 입력", font=("Pretendard", 24))
        self.setup_label.pack(pady=20)

        # 시간 입력 레이아웃 (분/초 나란히 배치)
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
        self.btn_save = ctk.CTkButton(self.setup_frame, text="예약 완료", fg_color="#2ecc71", hover_color="#27ae60", command=self.confirm_alarm)
        self.btn_save.pack(pady=15)

        self.btn_back = ctk.CTkButton(self.setup_frame, text="메인으로 돌아가기", fg_color="#e74c3c", hover_color="#c0392b", command=self.show_main_menu)
        self.btn_back.pack(pady=5)

    def show_setup_screen(self):
        """메인 메뉴 숨기고 설정창 열기"""
        self.status_label.configure(text="") # 상태창 초기화
        self.main_frame.pack_forget()
        self.setup_frame.pack(fill="both", expand=True)

    def show_main_menu(self):
        """설정창 숨기고 메인 메뉴 열기"""
        self.setup_frame.pack_forget()
        self.main_frame.pack(fill="both", expand=True)

    def confirm_alarm(self):
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
        sendingNotification.reserve_notification(msg, total_sec)
        
        # 입력칸 청소 및 메인 복귀
        self.msg_entry.delete(0, 'end')
        self.min_entry.delete(0, 'end')
        self.sec_entry.delete(0, 'end')
        
        self.show_main_menu()

if __name__ == "__main__":
    app = App()
    app.mainloop()
