import os
import json
import ctypes
from datetime import datetime, timedelta

INFO_FILE = "manage_chore_program.json"

#컴퓨터가 꺼질때 지우는 날짜라면 혹은 지났다면 지우기
def LoadInfo():
    if not os.path.exists(INFO_FILE):#없다면....
        default_data = {"rubbish_bin_period": 0, "next_clear_date": "None"}
        with open(INFO_FILE, "w", encoding="utf-8") as f:
            json.dump(default_data, f, indent=4)
        return 0, "None"

    try:
        with open(INFO_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("rubbish_bin_period", 0), data.get(
                "next_clear_date", "None"
            )
    except Exception:
        return 0, "None"


def SetRubbishBinClearDate(days):
    """주기를 변경하고 새로운 다음 예약일을 계산하여 JSON에 씁니다."""
    if days == 0:
        next_date_str = "None"
    else:
        next_date = datetime.now() + timedelta(days=days)
        next_date_str = next_date.strftime("%Y-%m-%d %H:%M:%S")

    if os.path.exists(INFO_FILE):
        with open(INFO_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except Exception:
                data = {}
    else:
        data = {}

    data["rubbish_bin_period"] = days
    data["next_clear_date"] = next_date_str

    with open(INFO_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return next_date_str


def GetRubbishBinClearDate():
    """다음 휴지통을 비워야 하는 타겟 날짜 스트링을 반환합니다."""
    _, next_clear_date = LoadInfo()
    return next_clear_date


def ActionRubbishBinClear():
    """Windows API를 호출하여 백그라운드에서 조용히 휴지통을 비웁니다."""
    try:
        # Flags 7: 소리 없음, 진행창 없음, 확인창 요청 없음
        result = ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 7)
        if result == 0:
            print("휴지통을 성공적으로 비웠습니다.")
            return True
        else:
            print("휴지통이 이미 비어있거나 처리할 항목이 없습니다.")
            return False
    except Exception as e:
        print(f"휴지통 비우기 실행 실패: {e}")
        return False
