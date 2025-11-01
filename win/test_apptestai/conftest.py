import os
import pytest
import gspread
from common_utils import *
from google.oauth2.service_account import Credentials
from playwright.sync_api import sync_playwright

STORAGE_STATE_PATH = ".vscode/storageState.json"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    ".vscode/credentials.json",
    scopes=SCOPES
)
client = gspread.authorize(creds)

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

    # # 테스트 종료 후 30초 대기
    # page.wait_for_timeout(30000)

    # context.close()
    # browser.close()
    # p.stop()

    # # 세션파일 자동삭제
    #     # 세션 파일 자동 삭제
    # if os.path.exists(storage_state_file):
    #     os.remove(storage_state_file)
    #     print(f"✅ 로그인 세션 파일 삭제 완료: {storage_state_file}")
    # else:
    #     print("⚠️ 삭제할 세션 파일이 존재하지 않습니다.")


@pytest.fixture(scope="module")
def aos_flag():
    return {"run": True}

@pytest.fixture(scope="module")
def ios_flag():
    return {"run": True}

# 구글계정 > 세션 단위로 인증, 시트 클라이언트 생성
@pytest.fixture(scope="session")
def gsheet_client():
    client = gspread.authorize(creds)
    return client

# 자동화 결과확인 시트 객체를 fixture로 제공
@pytest.fixture
def sheet(gsheet_client):

    spreadsheet_key = "1NpZVVopxJCrQXqv9c-A83PozWufznzr9mbT4NTpFKOc"
    spreadsheet = gsheet_client.open_by_key(spreadsheet_key)
    
    sheet_name = "[자동화] App_Regression_결과확인_v1.0"
    return spreadsheet.worksheet(sheet_name)

# 테스트 진행 및 구글sheet 기록 wrapper fixture
@pytest.fixture
def write_result(sheet):
    # sheet 객체를 받아서 공통 함수 호출
    def _write(cell: str, status: str):
        write_to_sheet(sheet, cell, status)
    return _write