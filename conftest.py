import os
import pytest
from playwright.sync_api import sync_playwright

STORAGE_STATE_PATH = ".vscode/storageState.json"

@pytest.fixture(scope="session")
def storage_state_file():
    """
    수동 로그인 후 로그인 세션 저장.
    저장된 세션이 있으면 바로 사용.
    """
    if not os.path.exists(STORAGE_STATE_PATH):
        print(">>> 로그인 세션 파일이 없습니다. 수동 로그인 필요 <<<")
        p = sync_playwright().start()
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # 로그인 페이지 열기
        page.goto("https://app.apptest.ai")
        page.click("#gray") 

        # 수동 로그인 대기
        print("\n>>> 구글 로그인 창에서 로그인 완료 후 Enter를 눌러 계속하세요...")
        input("로그인 완료 후 Enter: ")

        # 로그인 세션 저장
        context.storage_state(path=STORAGE_STATE_PATH)
        print(f"✅ 로그인 세션 저장 완료: {STORAGE_STATE_PATH}")

        browser.close()
        p.stop()
    else:
        print(f"✅ 로그인 세션 사용: {STORAGE_STATE_PATH}")

    return STORAGE_STATE_PATH


@pytest.fixture(scope="session")
def main_homepage(storage_state_file):
    """
    저장된 로그인 세션을 사용하여 새로운 브라우저 페이지 생성.
    테스트 함수 간 같은 브라우저 페이지 공유.
    """
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(storage_state=storage_state_file)
    page = context.new_page()

    yield page  # 여기서 테스트 함수들이 page 객체 사용

    # 테스트 종료 후 30초 대기
    page.wait_for_timeout(30000)

    context.close()
    browser.close()
    p.stop()