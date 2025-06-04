import time
import threading ## 검색 실행을 별도 쓰레드로 처리해서 gui가 멈추지 않게함
import tkinter as tk 
from tkinter import messagebox ## tkinter 팝업 알림
## 이하 셀레니움 관련 모듈 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_experimental_option("detach", True)
## 그냥 사용자가 감정을 입력하면 거기에 맞는 키워드로 변환케 하는 딕셔ㅕ너리
emotion_map = {
    "우울": "이별 노래",
    "슬픔": "눈물 나는 발라드",
    "행복": "기분 좋은 노래",
    "설렘": "설레는 노래",
    "신남": "신나는 음악",
    "짜증": "화 풀리는 노래",
    "지침": "힐링 음악",
    "외로움": "외로운 밤 음악",
    "사랑": "사랑 노래 모음",
}

def search_and_scrape(song_name):
    try:
        browser = webdriver.Chrome(options=options)
        browser.get('https://www.youtube.com/')
        time.sleep(2)

        try:
            search_box = browser.find_element(By.NAME, 'search_query')
            search_box.clear()
            search_box.send_keys(song_name)
            search_box.send_keys(Keys.ENTER)
        except NoSuchElementException:
            print("검색창을 찾을 수 없습니다.")
            browser.quit()
            return

        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, 'video-title'))
        )

        videos = browser.find_elements(By.ID, 'video-title')
        for video in videos:
            href = video.get_attribute('href')
            title = video.get_attribute('title')
            if href and title:
                try:
                    video.click()
                    break
                except ElementClickInterceptedException:
                    print("영상 클릭이 차단됨.")
                    continue

        time.sleep(5)
        skip_btns = browser.find_elements(By.CLASS_NAME, 'ytp-ad-skip-button')
        if skip_btns:
            try:
                skip_btns[0].click()
                print("광고 건너뛰기 클릭")
            except:
                print("광고 건너뛰기 실패")

        time.sleep(2)
        browser.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(3)

        comment_elements = browser.find_elements(By.CSS_SELECTOR, "ytd-comment-thread-renderer #content")
        comments = [el.text for el in comment_elements[:10]]  # 상위 10개만 출력
        print("\n".join(comments))

        def update_ui():
            result_box.delete(1.0, tk.END)
            result_box.insert(tk.END, f"검색어: {song_name}\n\n")
            for i, comment in enumerate(comments, 1):
                result_box.insert(tk.END, f"[{i}] {comment}\n\n")

        root.after(0, update_ui)

    except Exception as e:
        print(f"에러 발생: {e}")
        messagebox.showerror("오류", f"에러 발생: {e}")

def on_search():
    keyword = entry.get().strip()
    if not keyword:
        messagebox.showwarning("입력 오류", "감정 또는 검색어를 입력하세요.")
        return

    search_term = emotion_map.get(keyword, keyword + ' 플레이 리스트')
    ## gui 멈춤 방지를 위해 백그라운드 스레드 에서 실행 
    threading.Thread(target=search_and_scrape, args=(search_term,), daemon=True).start()


root = tk.Tk()
root.title("유튜브 플리")

entry = tk.Entry(root, width=40)
entry.pack(pady=10)

search_btn = tk.Button(root, text="검색", command=on_search)
search_btn.pack(pady=5)

result_box = tk.Text(root, height=20, width=60)
result_box.pack(pady=10)

root.mainloop()
