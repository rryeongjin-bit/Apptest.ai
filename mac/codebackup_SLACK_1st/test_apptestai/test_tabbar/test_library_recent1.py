import pytest
import re
from element_total import *
from common_utils import *
from conftest import *

# -------------------------------
# 로그인&계정전환 + 프로젝트 폴더 진입
# -------------------------------
@pytest.mark.order(1)
@pytest.mark.prod_tabbar
@pytest.mark.stg_tabbar
def test_login_enter_project(main_homepage):
    page = main_homepage
    login_and_select_project(page)

# -------------------------------
# [Prod] Tab bar 프로젝트
# -------------------------------
TCID = ["App_CheckList_006","App_CheckList_007","App_CheckList_008",
        "App_CheckList_010","App_CheckList_011","App_CheckList_012",
        "App_CheckList_013","App_CheckList_014","App_CheckList_015",
        "App_CheckList_016","App_CheckList_019","App_CheckList_027","App_CheckList_032"]

@pytest.mark.order(2)
@pytest.mark.prod_tabbar
def test_project_tabbar(main_homepage):
    page = main_homepage
    page.click(prod_tabbar)

    target_project = page.locator(project_title).get_by_text("[Prod] Tab Bar")
    try:
        target_project.wait_for(state="visible", timeout=5000)
    except TimeoutError:
        assert False, f"❌ {prod_tabbar} 폴더 진입 실패"

    assert target_project.is_visible(), f"❌ {prod_tabbar} 폴더 진입 실패"

@pytest.mark.order(3)
@pytest.mark.prod_tabbar
def test_checkresult(main_homepage):
    page = main_homepage
    targets = [
            (title_recent_result, "Recent Test Runs"),
        ]

    click_and_verify(page, btn_test_run, targets)
    select_rows(page)

"""
📍내 서재_최근 본/내 서재_뷰어 이동
"""
@pytest.mark.order(4)
@pytest.mark.prod_tabbar
def test_checkresult_AOS(main_homepage):
    page = main_homepage
    apply_filter_checkbox_AOS(page)

@pytest.mark.order(5)
@pytest.mark.prod_tabbar
def test_testrun_info_AOS(main_homepage, aos_flag, sheet):
    page = main_homepage
    AOS_testrun_recent1 = page.locator(testrun_first).filter(
        has_text=re.compile(r"^내 서재_최근 본/내 서재_뷰어 이동_AOS$", re.IGNORECASE)
    ).first

    try:
        AOS_testrun_recent1.wait_for(state="attached", timeout=5000)
        AOS_testrun_recent1.scroll_into_view_if_needed()
        AOS_testrun_recent1.wait_for(state="visible", timeout=5000)
        AOS_testrun_recent1.click()

        AOS_testrun_info = get_testrun_info(page, testrun_id_section)
        write_result_by_key(sheet, TCID, AOS_testrun_info, column="S")

    except Exception as e:
        write_result_by_key(sheet, TCID, "No Info", column="S")
        aos_flag["run"] = False
        pytest.skip("⚠️ AOS 테스트 결과 없음 - 테스트 정보 확인 skip")

@pytest.mark.order(6)
@pytest.mark.prod_tabbar
def test_check_testresult_AOS(main_homepage, aos_flag, sheet):
    if not aos_flag["run"]:
        write_result_by_key(sheet, TCID, "N/T", column="P")
        pytest.skip("⚠️ AOS 테스트 결과 없음 - 결과 확인 skip")

    page = main_homepage
    App_CheckList_006_AOS= get_testrun_status_AOS(page, testrun_status)
    write_result_by_key(sheet, TCID, App_CheckList_006_AOS, column="P")

@pytest.mark.order(7)
@pytest.mark.prod_tabbar
def test_back_testrun_list_AOS(main_homepage, aos_flag):
    back_and_or_reset_AOS(main_homepage, aos_flag.get("run", False))

@pytest.mark.order(8)
@pytest.mark.prod_tabbar
def test_checkresult_IOS(main_homepage):
    page = main_homepage
    apply_filter_checkbox_iOS(page)

@pytest.mark.order(9)
@pytest.mark.prod_tabbar
def test_testrun_info_IOS(main_homepage, ios_flag, sheet):
    page = main_homepage
    IOS_testrun_recent1 = page.locator(testrun_first).filter(
        has_text=re.compile(r"^내 서재_최근 본/내 서재_뷰어 이동_iOS$", re.IGNORECASE)
    ).first

    try:
        IOS_testrun_recent1.wait_for(state="attached", timeout=5000)
        IOS_testrun_recent1.scroll_into_view_if_needed()
        IOS_testrun_recent1.wait_for(state="visible", timeout=5000)
        IOS_testrun_recent1.click()
    
        IOS_testrun_info = get_testrun_info(page, testrun_id_section)
        write_result_by_key(sheet, TCID, IOS_testrun_info, column="T")

    except Exception as e:
        write_result_by_key(sheet, TCID, "No Info", column="T")
        ios_flag["run"] = False
        pytest.skip("⚠️ IOS 테스트 결과 없음 - 테스트 정보 확인 skip")

@pytest.mark.order(10)
@pytest.mark.prod_tabbar
def test_check_testresult_IOS(main_homepage, ios_flag, sheet):
    if not ios_flag["run"]:
        write_result_by_key(sheet, TCID, "N/T", column="R")
        pytest.skip("⚠️ IOS 테스트 결과 없음 - 결과 확인 skip")

    page = main_homepage
    App_CheckList_006_iOS = get_testrun_status_IOS(page, testrun_status)
    write_result_by_key(sheet,TCID, App_CheckList_006_iOS, column="R")

@pytest.mark.order(11)
@pytest.mark.prod_tabbar
def test_back_testrun_list_IOS(main_homepage, ios_flag):
    back_and_or_reset_IOS(main_homepage, ios_flag.get("run", False))

# -------------------------------
# ⌛ [Stage] Tab bar 프로젝트 ⌛
# ------------------------------

