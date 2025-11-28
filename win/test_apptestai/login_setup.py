from playwright.sync_api import sync_playwright
from conftest import *
import os

def login():
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://app.apptest.ai")
    # 필요 시 로그인 버튼 클릭
    input("로그인 완료 후 Enter: ")

    context.storage_state(path=STORAGE_STATE_PATH)
    browser.close()
    p.stop()
    print(f"로그인 세션 저장 완료: {STORAGE_STATE_PATH}")

if __name__ == "__main__":
    login()
