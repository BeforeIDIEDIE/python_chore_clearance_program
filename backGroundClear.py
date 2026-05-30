import os
import shutil

def ClearBackGround():
    # 바탕화면 경로지정
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    # 폴더가 없다면 생성
    organized_folder = os.path.join(desktop_path, "짬통")
    os.makedirs(organized_folder, exist_ok=True)
    
    # 2. 바탕화면 파일 탐색 및 이동
    for item in os.listdir(desktop_path):   
        item_path = os.path.join(desktop_path, item)#바탕화면의 해당 아이템의 경로(절대)를 얻는다.
        if item == "짬통": #짬통 폴더는 건드리지않는다.
            continue
        
        if os.path.isfile(item_path):#폴더가 아닌 파일만 건든다.
            #확장자가 lnk인 바로가기 파일의 경우 예외처리에서 걸러지는 문제가 있으나........ 이게더 낫다고 생각해서 수정안함...
            # 파일명과 확장자 분리
            name, ext = os.path.splitext(item)
            ext = ext.lstrip('.').lower() # '.' 제거 및 소문자 변환
            
            # 확장자가 없는 파일인 경우 'no_ext' 폴더로 분류
            if not ext:
                ext = "no_ext"
                
            # 대상 확장자 폴더 생성
            target_dir = os.path.join(organized_folder, ext)
            os.makedirs(target_dir, exist_ok=True)
            
            # 3. 이름 중복 방지 기능 - 동일이름 존재시 파일명에 숫자마스킹
            target_path = os.path.join(target_dir, item)
            count = 1

            while os.path.exists(target_path):
                new_name = f"{name} ({count}).{ext}" if ext != "no_ext" else f"{name} ({count})"
                target_path = os.path.join(target_dir, new_name)
                count += 1
                
            # 4. 안전하게 파일 이동 (os.rename 대신 다른 드라이브간 이동도 지원하는 shutil.move 사용)
            try:
                shutil.move(item_path, target_path)
            except PermissionError:
                print(f"⚠️ 파일이 사용 중입니다: {item} (스킵됨)")
            except Exception as e:
                print(f"❌ {item} 이동 중 오류 발생: {e}")
