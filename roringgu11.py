##일단 고정댓글 크롤링해서 노래 리스트 ui에 띄우기 걍 ui에 날짜와 들은 노래 리스트 저장하자
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import tkinter as tk
options = Options()
options.add_experimental_option("detach", True)

eemotion_map = {
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

def backdochan(song_name):
    browser = webdriver.Chrome(options=options)
    browser.get('https://www.youtube.com/')
    time.sleep(2)

    elem = browser.find_element(By.NAME, 'search_query')
    elem.clear()
    elem.send_keys(song_name)
    elem.send_keys(Keys.ENTER)

    time.sleep(2)
    videos = browser.find_elements(By.ID,'video-title')

    for video in videos:
        href = video.get_attribute('href')
        title = video.get_attribute('title')

        if href and title:
            video.click()
            break

    time.sleep(5)
    try:
        skip_btn = browser.find_element(By.CLASS_NAME, 'ytp-ad-skip-button')
        skip_btn.click()
        print("광고 건너뛰기 버튼 클릭됨")
    except:
        print("광고 없음 또는 건너뛰기 불가")

    last_height = browser.execute_script("return document.documentElement.scrollHeight")

    browser.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(3)

    # 4. 댓글 추출
    comment_elements = browser.find_elements(By.CSS_SELECTOR, "ytd-comment-thread-renderer #content")

    for el in comment_elements:
        print(el.text)  # 댓글 출력
def on_search():
    search = entry.get().strip() + '플레이 리스트'
    backdochan(search)

root = tk.Tk()
root.title("유튜브 플레이리스트 검색기")

entry = tk.Entry(root, width=40)
entry.pack(pady=10)

search_btn = tk.Button(root, text="검색", command=on_search)
search_btn.pack(pady=5)

root.mainloop()
