import pytest
import re
from element_total import *
from common_utils import *
from conftest import *

TCID = [ "App_CheckList_129", "App_CheckList_130", "App_CheckList_131", "App_CheckList_132", 
        "App_CheckList_133", "App_CheckList_134", "App_CheckList_135", "App_CheckList_136",
        "App_CheckList_137", "App_CheckList_138", "App_CheckList_139", "App_CheckList_140",
        "App_CheckList_141", "App_CheckList_142", "App_CheckList_143", "App_CheckList_144", "App_CheckList_145" ]

def test_001_login_enter_project(main_homepage):
    page = main_homepage
    login_and_select_project(page)

def test_002_project_genrehome(main_homepage):
    page = main_homepage
    page.click(onestore_genrehome)

    target_project = page.locator(project_title).get_by_text("[완전판] 장르홈")
    try:
        target_project.wait_for(state="visible", timeout=5000)
    except TimeoutError:
        assert False, f"❌ {onestore_genrehome} 폴더 진입 실패"

    assert target_project.is_visible(), f"❌ {onestore_genrehome} 폴더 진입 실패"

def test_003_checkresult(main_homepage):
    page = main_homepage
    targets = [
            (title_recent_result, "Recent Test Runs"),
        ]

    click_and_verify(page, btn_test_run, targets)
    select_rows(page)

"""
📍 장르홈_웹소설
"""    
def test_004_checkresult_AOS(main_homepage):
    page = main_homepage
    apply_filter_checkbox_AOS(page)

def test_005_testrun_info_AOS(main_homepage, aos_flag, sheet):
    page = main_homepage
    AOS_testrun_webnovel = page.locator(testrun_first).filter(
        has_text=re.compile(r"장르홈_웹소설", re.IGNORECASE) 
    ).first

    try:
        AOS_testrun_webnovel.wait_for(state="attached", timeout=5000)
        AOS_testrun_webnovel.scroll_into_view_if_needed()
        AOS_testrun_webnovel.wait_for(state="visible", timeout=5000)
        AOS_testrun_webnovel.click()

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
    App_CheckList_129_AOS = get_testrun_status_AOS(page, testrun_status)
    write_result_by_key(sheet, TCID, App_CheckList_129_AOS, column="Q")

def test_007_back_testrun_list_AOS(main_homepage, aos_flag):
    back_and_or_reset_AOS(main_homepage, aos_flag.get("run", False))
