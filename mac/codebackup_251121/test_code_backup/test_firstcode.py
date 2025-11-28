import os
import pytest
from playwright.sync_api import sync_playwright

STORAGE_STATE_PATH = ".vscode/storageState.json"

@pytest.fixture(scope="session")
def storage_state_file():
    """
    세션(scope='session')단위로 한 번만 로그인 상태 저장.
    로그인 세션이 저장된 파일이 없으면 직접 로그인하도록 실행.
    """
    if not os.path.exists(STORAGE_STATE_PATH):
        print(">>> 로그인 세션 파일이 없습니다. 로그인 수동 진행 필요 <<<")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()
            
            # 로그인 페이지 접속 및 로그인 버튼 클릭
            page.goto("https://app.apptest.ai")
            page.click("#gray")
            
            # 수동 로그인
            print("구글 로그인 창에서 로그인 완료 후 엔터를 눌러 계속하세요...")
            input()
            
            # 로그인 세션 저장
            context.storage_state(path=STORAGE_STATE_PATH)
            browser.close()
            print(f"로그인 세션이 '{STORAGE_STATE_PATH}'에 저장되었습니다.")
    else:
        print(f"로그인 세션 파일 '{STORAGE_STATE_PATH}'를 사용합니다.")
    
    return STORAGE_STATE_PATH

@pytest.fixture(scope="function")
def logged_in_context(storage_state_file):
    """
    저장된 로그인 세션 파일을 로드해서 로그인된 컨텍스트를 반환.
    각 테스트 함수별로 새로운 컨텍스트를 생성해서 독립성 보장.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state=storage_state_file)
        yield context

         # 테스트 종료 후 브라우저 1분 유지
        if context.pages:
            context.pages[0].wait_for_timeout(60000)  # 60초 = 1분
        
        context.close()
        browser.close()

def test_complete_login(logged_in_context):
    page = logged_in_context.new_page()
    page.goto("https://app.apptest.ai")
    assert "Dashboard" in page.inner_text("body")