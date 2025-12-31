import pytest
import re
from element_total import *
from common_utils import *
from conftest import *

TCID = [ "App_CheckList_240", "App_CheckList_241" ]

def test_001_login_enter_project(main_homepage):
    page = main_homepage
    login_and_select_project(page)

def test_002_project_contentshome(main_homepage):
    page = main_homepage
    page.click(onestore_contentshome)

    target_project = page.locator(project_title).get_by_text("[완전판] 작품 홈")
    try:
        target_project.wait_for(state="visible", timeout=5000)
    except TimeoutError:
        assert False, f"❌ {onestore_contentshome} 폴더 진입 실패"

    assert target_project.is_visible(), f"❌ {onestore_contentshome} 폴더 진입 실패"

def test_003_checkresult(main_homepage):
    page = main_homepage
    targets = [
            (title_recent_result, "Recent Test Runs"),
        ]

    click_and_verify(page, btn_test_run, targets)
    select_rows(page)

"""
📍 작품 홈_default-ebook_상단 영역_세트작품/공유
"""    
def test_004_checkresult_AOS(main_homepage):
    page = main_homepage
    apply_filter_checkbox_AOS(page)

def test_005_testrun_info_AOS(main_homepage,aos_flag, sheet):
    page = main_homepage
    AOS_testrun_default_ebook_top = page.locator(testrun_first).filter(
        has_text=re.compile(r"작품 홈_default-ebook_상단 영역_세트작품/공유$", re.IGNORECASE) 
    ).first

    try:
        AOS_testrun_default_ebook_top.wait_for(state="attached", timeout=5000)
        AOS_testrun_default_ebook_top.scroll_into_view_if_needed()
        AOS_testrun_default_ebook_top.wait_for(state="visible", timeout=5000)
        AOS_testrun_default_ebook_top.click()

        AOS_testrun_info = get_testrun_info(page, testrun_id_section)
        write_result_by_key(sheet, TCID, AOS_testrun_info, column="T")

    except Exception as e:
        write_result_by_key(sheet, TCID, "No Info", column="T")
        aos_flag["run"] = False
        pytest.skip("⚠️ AOS 테스트 결과 없음 - 테스트 정보 확인 skip")

def test_006_check_testresult_AOS(main_homepage, aos_flag, sheet):
    if not aos_flag["run"]:
        write_result_by_key(sheet, TCID, "N/T", column="Q")
        pytest.skip("⚠️ AOS 테스트 결과 없음 - 결과 확인 skip")

    page = main_homepage
    App_CheckList_240_AOS = get_testrun_status_AOS(page, testrun_status)
    write_result_by_key(sheet, TCID, App_CheckList_240_AOS, column="Q")

def test_007_back_testrun_list_AOS(main_homepage, aos_flag):
    back_and_or_reset_AOS(main_homepage, aos_flag.get("run", False))
