import pytest
import re
from element_total import *
from common_utils import *
from conftest import *

TCID = [ "App_CheckList_420"]

@pytest.mark.order(1)
@pytest.mark.prod_shortcut
def test_login_enter_project(main_homepage):
    page = main_homepage
    login_and_select_project(page)


@pytest.mark.order(2)
@pytest.mark.prod_shortcut
def test_project_shorcut(main_homepage):
    page = main_homepage
    page.click(prod_shortcut)

    target_project = page.locator(project_title).get_by_text("[Prod] 숏컷")
    try:
        target_project.wait_for(state="visible", timeout=5000)
    except TimeoutError:
        assert False, f"❌ {prod_shortcut} 폴더 진입 실패"

    assert target_project.is_visible(), f"❌ {prod_shortcut} 폴더 진입 실패"

@pytest.mark.order(3)
@pytest.mark.prod_shortcut
def test_checkresult(main_homepage):
    page = main_homepage
    targets = [
            (title_recent_result, "Recent Test Runs"),
        ]

    click_and_verify(page, btn_test_run, targets)
    select_rows(page)

@pytest.mark.order(4)
@pytest.mark.prod_shortcut
def test_checkresult_AOS(main_homepage):
    page = main_homepage
    apply_filter_checkbox_AOS(page)

@pytest.mark.order(5)
@pytest.mark.prod_shortcut
def test_testrun_info_AOS(main_homepage, aos_flag, sheet):
    page = main_homepage
    AOS_testrun_shortcut = page.locator(testrun_first).filter(
        has_text=re.compile(r"리디웹\s*바로가기", re.IGNORECASE)
    ).first

    try:
        AOS_testrun_shortcut.wait_for(state="attached", timeout=5000)
        AOS_testrun_shortcut.scroll_into_view_if_needed()
        AOS_testrun_shortcut.wait_for(state="visible", timeout=5000)
        AOS_testrun_shortcut.click()

        AOS_testrun_info = get_testrun_info(page, testrun_id_section)
        write_result_by_key(sheet, TCID, AOS_testrun_info, column="S")

    except Exception as e:
        write_result_by_key(sheet, TCID, "No Info", column="S")
        aos_flag["run"] = False
        pytest.skip("⚠️ AOS 테스트 결과 없음 - 테스트 정보 확인 skip")

@pytest.mark.order(6)
@pytest.mark.prod_shortcut
def test_check_testresult_AOS(main_homepage, aos_flag, sheet):
    if not aos_flag["run"]:
        write_result_by_key(sheet, TCID, "N/T", column="Q")
        pytest.skip("⚠️ AOS 테스트 결과 없음 - 결과 확인 skip")

    page = main_homepage
    App_CheckList_420_AOS= get_testrun_status_AOS(page, testrun_status)
    write_result_by_key(sheet,TCID, App_CheckList_420_AOS, column="Q")

@pytest.mark.order(7)
@pytest.mark.prod_shortcut
def test_back_testrun_list_AOS(main_homepage, aos_flag):
    back_and_or_reset_AOS(main_homepage, aos_flag.get("run", False))

