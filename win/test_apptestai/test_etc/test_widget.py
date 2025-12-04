import pytest
import re
from element_total import *
from common_utils import *
from conftest import *

# -------------------------------
# 로그인&계정전환 + 프로젝트 폴더 진입
# -------------------------------
@pytest.mark.order(1)
@pytest.mark.prod_widget
@pytest.mark.stg_widget
def test_login_enter_project(main_homepage):
    page = main_homepage
    login_and_select_project(page)

# -------------------------------
# [Prod] 위젯 프로젝트
# -------------------------------
AOS_TCID = [ "App_CheckList_419", "App_CheckList_421"]
IOS_TCID = [ "App_CheckList_419", "App_CheckList_422"]

@pytest.mark.order(2)
@pytest.mark.prod_widget
def test_project_widget(main_homepage):
    page = main_homepage
    page.click(prod_widget)

    target_project = page.locator(project_title).get_by_text("[Prod] 위젯")
    try:
        target_project.wait_for(state="visible", timeout=5000)
    except TimeoutError:
        assert False, f"❌ {prod_widget} 폴더 진입 실패"

    assert target_project.is_visible(), f"❌ {prod_widget} 폴더 진입 실패"
    
@pytest.mark.order(3)
@pytest.mark.prod_widget
def test_checkresult(main_homepage):
    page = main_homepage
    targets = [
            (title_recent_result, "Recent Test Runs"),
        ]

    click_and_verify(page, btn_test_run, targets)
    select_rows(page)
    
@pytest.mark.order(4)
@pytest.mark.prod_widget
def test_checkresult_AOS(main_homepage):
    page = main_homepage
    apply_filter_checkbox_AOS(page)

@pytest.mark.order(5)
@pytest.mark.prod_widget
def test_testrun_info_AOS(main_homepage, aos_flag, sheet):
    page = main_homepage
    AOS_testrun_widget = page.locator(testrun_first).filter(
        has_text=re.compile(r"숏컷_위젯", re.IGNORECASE)
    ).first

    try:
        AOS_testrun_widget.wait_for(state="attached", timeout=5000)
        AOS_testrun_widget.scroll_into_view_if_needed()
        AOS_testrun_widget.wait_for(state="visible", timeout=5000)
        AOS_testrun_widget.click()

        AOS_testrun_info = get_testrun_info(page, testrun_id_section)
        write_result_by_key(sheet, AOS_TCID, AOS_testrun_info, column="S")

    except Exception as e:
        write_result_by_key(sheet, AOS_TCID, "No Info", column="S")
        aos_flag["run"] = False
        pytest.skip("⚠️ AOS 테스트 결과 없음 - 테스트 정보 확인 skip")

@pytest.mark.order(6)
@pytest.mark.prod_widget
def test_check_testresult_AOS(main_homepage, aos_flag, sheet):
    if not aos_flag["run"]:
        write_result_by_key(sheet, AOS_TCID, "N/T", column="P")
        pytest.skip("⚠️ AOS 테스트 결과 없음 - 결과 확인 skip")

    page = main_homepage
    App_CheckList_421_AOS= get_testrun_status_AOS(page, testrun_status)
    write_result_by_key(sheet,AOS_TCID, App_CheckList_421_AOS, column="P")

@pytest.mark.order(7)
@pytest.mark.prod_widget
def test_back_testrun_list_AOS(main_homepage, aos_flag):
    back_and_or_reset_AOS(main_homepage, aos_flag.get("run", False))

@pytest.mark.order(8)
@pytest.mark.prod_widget
def test_checkresult_IOS(main_homepage):
    page = main_homepage
    apply_filter_checkbox_iOS(page)

@pytest.mark.order(9)
@pytest.mark.prod_widget
def test_testrun_info_IOS(main_homepage, ios_flag, sheet):
    page = main_homepage
    IOS_testrun_widget = page.locator(testrun_first).filter(
        has_text=re.compile(r"숏컷_위젯", re.IGNORECASE)
    ).first

    try:
        IOS_testrun_widget.wait_for(state="attached", timeout=5000)
        IOS_testrun_widget.scroll_into_view_if_needed()
        IOS_testrun_widget.wait_for(state="visible", timeout=5000)
        IOS_testrun_widget.click()
    
        IOS_testrun_info = get_testrun_info(page, testrun_id_section)
        write_result_by_key(sheet, IOS_TCID, IOS_testrun_info, column="T")

    except Exception as e:
        write_result_by_key(sheet, IOS_TCID, "No Info", column="T")
        ios_flag["run"] = False
        pytest.skip("⚠️ IOS 테스트 결과 없음 - 테스트 정보 확인 skip")

@pytest.mark.order(10)
@pytest.mark.prod_widget
def test_check_testresult_IOS(main_homepage, ios_flag, sheet):
    if not ios_flag["run"]:
        write_result_by_key(sheet, IOS_TCID, "N/T", column="R")
        pytest.skip("⚠️ IOS 테스트 결과 없음 - 결과 확인 skip")

    page = main_homepage
    App_CheckList_422_iOS = get_testrun_status_IOS(page, testrun_status)
    write_result_by_key(sheet,IOS_TCID, App_CheckList_422_iOS, column="R")

@pytest.mark.order(11)
@pytest.mark.prod_widget
def test_back_testrun_list_IOS(main_homepage, ios_flag):
    back_and_or_reset_IOS(main_homepage, ios_flag.get("run", False))

# -------------------------------
# [Stage] 위젯 프로젝트
# ------------------------------
@pytest.mark.order(2)
@pytest.mark.stg_widget
def test_project_widget(main_homepage):
    page = main_homepage
    page.click(prod_widget)

    target_project = page.locator(project_title).get_by_text("[Stage] 위젯")
    try:
        target_project.wait_for(state="visible", timeout=5000)
    except TimeoutError:
        assert False, f"❌ {prod_widget} 폴더 진입 실패"

    assert target_project.is_visible(), f"❌ {prod_widget} 폴더 진입 실패"
    
@pytest.mark.order(3)
@pytest.mark.stg_widget
def test_checkresult(main_homepage):
    page = main_homepage
    targets = [
            (title_recent_result, "Recent Test Runs"),
        ]

    click_and_verify(page, btn_test_run, targets)
    select_rows(page)
    
@pytest.mark.order(4)
@pytest.mark.stg_widget
def test_checkresult_AOS(main_homepage):
    page = main_homepage
    apply_filter_checkbox_AOS(page)

@pytest.mark.order(5)
@pytest.mark.stg_widget
def test_testrun_info_AOS(main_homepage, aos_flag, sheet):
    page = main_homepage
    AOS_testrun_widget = page.locator(testrun_first).filter(
        has_text=re.compile(r"숏컷_위젯", re.IGNORECASE)
    ).first

    try:
        AOS_testrun_widget.wait_for(state="attached", timeout=5000)
        AOS_testrun_widget.scroll_into_view_if_needed()
        AOS_testrun_widget.wait_for(state="visible", timeout=5000)
        AOS_testrun_widget.click()

        AOS_testrun_info = get_testrun_info(page, testrun_id_section)
        write_result_by_key(sheet, AOS_TCID, AOS_testrun_info, column="S")

    except Exception as e:
        write_result_by_key(sheet, AOS_TCID, "No Info", column="S")
        aos_flag["run"] = False
        pytest.skip("⚠️ AOS 테스트 결과 없음 - 테스트 정보 확인 skip")

@pytest.mark.order(6)
@pytest.mark.stg_widget
def test_check_testresult_AOS(main_homepage, aos_flag, sheet):
    if not aos_flag["run"]:
        write_result_by_key(sheet, AOS_TCID, "N/T", column="P")
        pytest.skip("⚠️ AOS 테스트 결과 없음 - 결과 확인 skip")

    page = main_homepage
    App_CheckList_421_AOS= get_testrun_status_AOS(page, testrun_status)
    write_result_by_key(sheet,AOS_TCID, App_CheckList_421_AOS, column="P")

@pytest.mark.order(7)
@pytest.mark.stg_widget
def test_back_testrun_list_AOS(main_homepage, aos_flag):
    back_and_or_reset_AOS(main_homepage, aos_flag.get("run", False))

@pytest.mark.order(8)
@pytest.mark.stg_widget
def test_checkresult_IOS(main_homepage):
    page = main_homepage
    apply_filter_checkbox_iOS(page)

@pytest.mark.order(9)
@pytest.mark.stg_widget
def test_testrun_info_IOS(main_homepage, ios_flag, sheet):
    page = main_homepage
    IOS_testrun_widget = page.locator(testrun_first).filter(
        has_text=re.compile(r"숏컷_위젯", re.IGNORECASE)
    ).first

    try:
        IOS_testrun_widget.wait_for(state="attached", timeout=5000)
        IOS_testrun_widget.scroll_into_view_if_needed()
        IOS_testrun_widget.wait_for(state="visible", timeout=5000)
        IOS_testrun_widget.click()
    
        IOS_testrun_info = get_testrun_info(page, testrun_id_section)
        write_result_by_key(sheet, IOS_TCID, IOS_testrun_info, column="T")

    except Exception as e:
        write_result_by_key(sheet, IOS_TCID, "No Info", column="T")
        ios_flag["run"] = False
        pytest.skip("⚠️ IOS 테스트 결과 없음 - 테스트 정보 확인 skip")

@pytest.mark.order(10)
@pytest.mark.stg_widget
def test_check_testresult_IOS(main_homepage, ios_flag, sheet):
    if not ios_flag["run"]:
        write_result_by_key(sheet, IOS_TCID, "N/T", column="R")
        pytest.skip("⚠️ IOS 테스트 결과 없음 - 결과 확인 skip")

    page = main_homepage
    App_CheckList_422_iOS = get_testrun_status_IOS(page, testrun_status)
    write_result_by_key(sheet,IOS_TCID, App_CheckList_422_iOS, column="R")

@pytest.mark.order(11)
@pytest.mark.stg_widget
def test_back_testrun_list_IOS(main_homepage, ios_flag):
    back_and_or_reset_IOS(main_homepage, ios_flag.get("run", False))