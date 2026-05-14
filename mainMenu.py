import customtkinter as ctk
import sendingNotification

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("허드렛일 프로그램")
        self.geometry("800x400")

        # 1. 텍스트 라벨
        self.label = ctk.CTkLabel(self, text="허드렛일 목록", font=("Pretendard", 30))
        self.label.pack(pady=20)

        # 2. 버튼
        self.button = ctk.CTkButton(self, text="1. 알림 설정", command=self.button_callback)
        self.button.pack(pady=15)
        self.button = ctk.CTkButton(self, text="2. 꺼짐 설정", command=self.button_callback)
        self.button.pack(pady=15)
        self.button = ctk.CTkButton(self, text="3. 다운로드 파일 정리", command=self.button_callback)
        self.button.pack(pady=15)
        self.button = ctk.CTkButton(self, text="4. 바탕화면 정리", command=self.button_callback)
        self.button.pack(pady=15)

        # 3. 입력창
        #self.entry = ctk.CTkEntry(self, placeholder_text="여기에 입력하세요...")
        #self.entry.pack(pady=10)

        

    def button_callback(self):
        user_input = self.entry.get()
        self.label.configure(text=f"입력값: {user_input}")

app = App()
app.mainloop()
def MainMenu():
    while True : 
        print("\n" + "="*15 + " MENU " + "="*15)
        print("\n 1. 알림 설정 ")
        print("\n 2. 꺼짐 설정 ")
        print("\n 3. 바탕화면 정리 ")
        print("\n 4. 다운로드 정리 ")
