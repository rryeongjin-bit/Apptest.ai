import os
import pytest
import gspread
from common_utils import *
from google.oauth2.service_account import Credentials
from playwright.sync_api import sync_playwright


# App_Regression_checklist
CHECKLIST_VERSION = "v4.6"
checklist_sheet = "[자동화] App_Regression_결과확인_v1.3"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# conftest.py 기준 프로젝트 루트
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# storageState.json 절대경로
STORAGE_STATE_PATH = os.path.join(PROJECT_ROOT, ".vscode", "storageState.json")

# conftest.py 위치 기준
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
creds_path = os.path.join(BASE_DIR, ".vscode", "credentials.json")

creds = Credentials.from_service_account_file(
    creds_path,
    scopes=SCOPES
)
client = gspread.authorize(creds)

@pytest.fixture(scope="session")
def storage_state_file():
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

# 구글계정 인증
@pytest.fixture(scope="session")
def gsheet_client():
    client = gspread.authorize(creds)
    return client

# 자동화 결과확인 시트
@pytest.fixture
def sheet(gsheet_client):

    spreadsheet_key = "1lMbpJ8P9sXUNkmICPNT9cbDzAXjfruBVUjGbopj2O64"
    spreadsheet = gsheet_client.open_by_key(spreadsheet_key)
    
    sheet_name = checklist_sheet
    return spreadsheet.worksheet(sheet_name)

# 테스트 진행 및 구글sheet 기록 wrapper fixture
@pytest.fixture
def write_result(sheet):
    # sheet 객체를 받아서 공통 함수 호출
    def _write(cell: str, status: str):
        write_to_sheet(sheet, cell, status)
    return _write