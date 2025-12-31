from playwright.sync_api import sync_playwright
from conftest import *
import pytest
import os

@pytest.mark.login
def test_save_login_state():
   
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://app.apptest.ai")
        input("로그인을 완료한 뒤 Enter를 누르세요: ")

        context.storage_state(path=STORAGE_STATE_PATH)
        browser.close()

        print(f"로그인 세션 저장 완료: {STORAGE_STATE_PATH}")