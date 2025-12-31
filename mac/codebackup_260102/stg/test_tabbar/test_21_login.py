import pytest
import re
from element_total import *
from common_utils import *
from conftest import *

TCID = [ "App_CheckList_478", "App_CheckList_479" ]

def test_001_login_enter_project(main_homepage):
    page = main_homepage
    login_and_select_project(page)

def test_002_project_tabbar(main_homepage):
    page = main_homepage
    page.click(stg_tabbar)

    target_project = page.locator(project_title).get_by_text("[Stage] Tab Bar")
    try:
        target_project.wait_for(state="visible", timeout=5000)
    except TimeoutError:
        assert False, f"❌ {stg_tabbar} 폴더 진입 실패"

    assert target_project.is_visible(), f"❌ {stg_tabbar} 폴더 진입 실패"

def test_003_checkresult(main_homepage):
    page = main_homepage
    targets = [
            (title_recent_result, "Recent Test Runs"),
        ]

    click_and_verify(page, btn_test_run, targets)
    select_rows(page)

"""
📍Tab bar_마이리디_가입온보딩개선1차
"""
def test_004_checkresult_AOS(main_homepage):
    page = main_homepage
    apply_filter_checkbox_AOS(page)

def test_005_testrun_info_AOS(main_homepage, aos_flag, sheet):
    page = main_homepage
    AOS_testrun_loginbanner = page.locator(testrun_first).filter(
        has_text=re.compile(r"^Tab bar_마이리디_가입온보딩개선1차$", re.IGNORECASE)
    ).first

    try:
        AOS_testrun_loginbanner.wait_for(state="attached", timeout=5000)
        AOS_testrun_loginbanner.scroll_into_view_if_needed()
        AOS_testrun_loginbanner.wait_for(state="visible", timeout=5000)
        AOS_testrun_loginbanner.click()

        AOS_testrun_info = get_testrun_info(page, testrun_id_section)
        write_result_by_key(sheet, TCID, AOS_testrun_info, column="S")

    except Exception as e:
        write_result_by_key(sheet, TCID, "No Info", column="S")
        aos_flag["run"] = False
        pytest.skip("⚠️ AOS 테스트 결과 없음 - 테스트 정보 확인 skip")

def test_006_check_testresult_AOS(main_homepage, aos_flag, sheet):
    if not aos_flag["run"]:
        write_result_by_key(sheet, TCID, "N/T", column="P")
        pytest.skip("⚠️ AOS 테스트 결과 없음 - 결과 확인 skip")

    page = main_homepage
    App_CheckList_478_AOS= get_testrun_status_AOS(page, testrun_status)
    write_result_by_key(sheet, TCID, App_CheckList_478_AOS, column="P")

def test_007_back_testrun_list_AOS(main_homepage, aos_flag):
    back_and_or_reset_AOS(main_homepage, aos_flag.get("run", False))

def test_008_checkresult_IOS(main_homepage):
    page = main_homepage
    apply_filter_checkbox_iOS(page)

def test_009_testrun_info_IOS(main_homepage, ios_flag, sheet):
    page = main_homepage
    IOS_testrun_loginbanner= page.locator(testrun_first).filter(
        has_text=re.compile(r"^Tab bar_마이리디_가입온보딩개선1차$", re.IGNORECASE)
    ).first

    try:
        IOS_testrun_loginbanner.wait_for(state="attached", timeout=5000)
        IOS_testrun_loginbanner.scroll_into_view_if_needed()
        IOS_testrun_loginbanner.wait_for(state="visible", timeout=5000)
        IOS_testrun_loginbanner.click()
    
        IOS_testrun_info = get_testrun_info(page, testrun_id_section)
        write_result_by_key(sheet, TCID, IOS_testrun_info, column="U")

    except Exception as e:
        write_result_by_key(sheet, TCID, "No Info", column="U")
        ios_flag["run"] = False
        pytest.skip("⚠️ IOS 테스트 결과 없음 - 테스트 정보 확인 skip")

def test_010_check_testresult_IOS(main_homepage, ios_flag, sheet):
    if not ios_flag["run"]:
        write_result_by_key(sheet, TCID, "N/T", column="R")
        pytest.skip("⚠️ IOS 테스트 결과 없음 - 결과 확인 skip")

    page = main_homepage
    App_CheckList_478_iOS = get_testrun_status_IOS(page, testrun_status)
    write_result_by_key(sheet,TCID, App_CheckList_478_iOS, column="R")

def test_011_back_testrun_list_IOS(main_homepage, ios_flag):
    back_and_or_reset_IOS(main_homepage, ios_flag.get("run", False))
