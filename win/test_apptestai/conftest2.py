import os
import pytest
import gspread
from common_utils import *
from google.oauth2.service_account import Credentials
from playwright.sync_api import sync_playwright


checklist_sheet = "[자동화] App_Regression_결과확인_v1.4"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STORAGE_STATE_PATH = os.path.join(PROJECT_ROOT, ".vscode", "storageState.json")
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
        raise RuntimeError("로그인 세션 파일이 없습니다")
    return STORAGE_STATE_PATH

@pytest.fixture(scope="function")
def main_homepage(storage_state_file):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state=storage_state_file)
        page = context.new_page()

        yield page

        context.close()
        browser.close()

    # if os.path.exists(storage_state_file):
    #     os.remove(storage_state_file)


@pytest.fixture(scope="module")
def aos_flag():
    return {"run": True}

@pytest.fixture(scope="module")
def ios_flag():
    return {"run": True}

@pytest.fixture(scope="session")
def gsheet_client():
    client = gspread.authorize(creds)
    return client

@pytest.fixture
def sheet(gsheet_client):

    spreadsheet_key = "1hbO4IdYUbihO0tn_YwmOf4Zc-p8C2_KYWbHhM0kBltg"
    spreadsheet = gsheet_client.open_by_key(spreadsheet_key)
    
    sheet_name = checklist_sheet
    return spreadsheet.worksheet(sheet_name)

@pytest.fixture
def write_result(sheet):
    def _write(cell: str, status: str):
        write_to_sheet(sheet, cell, status)
    return _write