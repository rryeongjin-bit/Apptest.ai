import pytest
import re
from element_total import *
from common_utils import *
from conftest import *

# -------------------------------
# 로그인&계정전환 + 프로젝트 폴더 진입
# -------------------------------
@pytest.mark.order(1)
@pytest.mark.prod_usersfile
@pytest.mark.stg_usersfile
def test_login_enter_project(main_homepage):
    page = main_homepage
    login_and_select_project(page)

# -------------------------------
# [Prod] 사용자파일 프로젝트
# -------------------------------
TCID1 = ["App_CheckList_412", "App_CheckList_413" ]
TCID2 = ["App_CheckList_414"]

@pytest.mark.order(2)
@pytest.mark.prod_usersfile
def test_project_usersfile(main_homepage):
    page = main_homepage
    page.click(prod_usersfile)

    target_project = page.locator(project_title).get_by_text("[Prod] 사용자파일")
    try:
        target_project.wait_for(state="visible", timeout=5000)
    except TimeoutError:
        assert False, f"❌ {prod_usersfile} 폴더 진입 실패"

    assert target_project.is_visible(), f"❌ {prod_usersfile} 폴더 진입 실패"

@pytest.mark.order(3)
@pytest.mark.prod_usersfile
def test_checkresult(main_homepage):
    page = main_homepage
    targets = [
            (title_recent_result, "Recent Test Runs"),
        ]

    click_and_verify(page, btn_test_run, targets)
    select_rows(page)

"""
📍[사용자파일] PDF_상단 컨트롤러/본문
"""
@pytest.mark.order(4)
@pytest.mark.prod_usersfile
def test_checkresult_AOS_PDF1(main_homepage):
    page = main_homepage
    apply_filter_checkbox_AOS(page)


@pytest.mark.order(5)
@pytest.mark.prod_usersfile
def test_testrun_info_AOS_PDF1(main_homepage, aos_flag, sheet):
    page = main_homepage
    AOS_testrun_usersfile_PDF1 = page.locator(testrun_first).filter(
        has_text=re.compile(r"PDF_상단\s*컨트롤러", re.IGNORECASE)
    ).first

    try:
        AOS_testrun_usersfile_PDF1.wait_for(state="attached", timeout=5000)
        AOS_testrun_usersfile_PDF1.scroll_into_view_if_needed()
        AOS_testrun_usersfile_PDF1.wait_for(state="visible", timeout=5000)
        AOS_testrun_usersfile_PDF1.click()

        AOS_testrun_info = get_testrun_info(page, testrun_id_section)
        write_result_by_key(sheet, TCID1, AOS_testrun_info, column="S")

    except Exception as e:
        write_result_by_key(sheet, TCID1, "No Info", column="S")
        aos_flag["run"] = False
        pytest.skip("⚠️ AOS 테스트 결과 없음 - 테스트 정보 확인 skip")

@pytest.mark.order(6)
@pytest.mark.prod_usersfile
def test_check_testresult_AOS_PDF1(main_homepage, aos_flag, sheet):
    if not aos_flag["run"]:
        write_result_by_key(sheet, TCID1, "N/T", column="P")
        pytest.skip("⚠️ AOS 테스트 결과 없음 - 결과 확인 skip")

    page = main_homepage
    App_CheckList_412_AOS= get_testrun_status_AOS(page, testrun_status)
    write_result_by_key(sheet, TCID1, App_CheckList_412_AOS, column="P")

@pytest.mark.order(7)
@pytest.mark.prod_usersfile
def test_back_testrun_list_AOS_PDF1(main_homepage, aos_flag):
    back_and_or_reset_AOS(main_homepage, aos_flag.get("run", False))

@pytest.mark.order(8)
@pytest.mark.prod_usersfile
def test_checkresult_IOS_PDF1(main_homepage):
    page = main_homepage
    apply_filter_checkbox_iOS(page)

@pytest.mark.order(9)
@pytest.mark.prod_usersfile
def test_testrun_info_IOS_PDF1(main_homepage, ios_flag, sheet):
    page = main_homepage
    IOS_testrun_usersfile_PDF1= page.locator(testrun_first).filter(
        has_text=re.compile(r"PDF_상단\s*컨트롤러", re.IGNORECASE)
    ).first

    try:
        IOS_testrun_usersfile_PDF1.wait_for(state="attached", timeout=5000)
        IOS_testrun_usersfile_PDF1.scroll_into_view_if_needed()
        IOS_testrun_usersfile_PDF1.wait_for(state="visible", timeout=5000)
        IOS_testrun_usersfile_PDF1.click()
    
        IOS_testrun_info = get_testrun_info(page, testrun_id_section)
        write_result_by_key(sheet, TCID1, IOS_testrun_info, column="T")

    except Exception as e:
        write_result_by_key(sheet, TCID1, "No Info", column="T")
        ios_flag["run"] = False
        pytest.skip("⚠️ IOS 테스트 결과 없음 - 테스트 정보 확인 skip")

@pytest.mark.order(10)
@pytest.mark.prod_usersfile
def test_check_testresult_PDF1(main_homepage, ios_flag, sheet):
    if not ios_flag["run"]:
        write_result_by_key(sheet, TCID1, "N/T", column="R")
        pytest.skip("⚠️ IOS 테스트 결과 없음 - 결과 확인 skip")

    page = main_homepage
    App_CheckList_412_iOS = get_testrun_status_IOS(page, testrun_status)
    write_result_by_key(sheet,TCID1, App_CheckList_412_iOS, column="R")

@pytest.mark.order(11)
@pytest.mark.prod_usersfile
def test_back_testrun_list_IOS_PDF1(main_homepage, ios_flag):
    back_and_or_reset_IOS(main_homepage, ios_flag.get("run", False))

"""
📍[사용자파일] PDF_하단 컨트롤러
"""
@pytest.mark.order(12)
@pytest.mark.prod_usersfile
def test_checkresult_AOS_PDF2(main_homepage):
    page = main_homepage
    apply_filter_checkbox_AOS(page)

@pytest.mark.order(13)
@pytest.mark.prod_usersfile
def test_testrun_info_AOS_PDF2(main_homepage, aos_flag, sheet):
    page = main_homepage
    AOS_testrun_usersfile_PDF2 = page.locator(testrun_first).filter(
        has_text=re.compile(r"PDF_하단\s*컨트롤러", re.IGNORECASE)
    ).first

    try:
        AOS_testrun_usersfile_PDF2.wait_for(state="attached", timeout=5000)
        AOS_testrun_usersfile_PDF2.scroll_into_view_if_needed()
        AOS_testrun_usersfile_PDF2.wait_for(state="visible", timeout=5000)
        AOS_testrun_usersfile_PDF2.click()

        AOS_testrun_info = get_testrun_info(page, testrun_id_section)
        write_result_by_key(sheet, TCID2, AOS_testrun_info, column="S")

    except Exception as e:
        write_result_by_key(sheet, TCID2, "No Info", column="S")
        aos_flag["run"] = False
        pytest.skip("⚠️ AOS 테스트 결과 없음 - 테스트 정보 확인 skip")

@pytest.mark.order(14)
@pytest.mark.prod_usersfile
def test_check_testresult_AOS_PDF2(main_homepage, aos_flag, sheet):
    if not aos_flag["run"]:
        write_result("P482", "N/T")
        pytest.skip("⚠️ AOS 테스트 결과 없음 - 결과 확인 skip")

    page = main_homepage
    App_CheckList_414_AOS= get_testrun_status_AOS(page, testrun_status)
    write_result_by_key(sheet, TCID2, App_CheckList_414_AOS, column="P")

@pytest.mark.order(15)
@pytest.mark.prod_usersfile
def test_back_testrun_list_AOS_PDF2(main_homepage, aos_flag):
    back_and_or_reset_AOS(main_homepage, aos_flag.get("run", False))

@pytest.mark.order(16)
@pytest.mark.prod_usersfile
def test_checkresult_IOS_PDF2(main_homepage):
    page = main_homepage
    apply_filter_checkbox_iOS(page)

@pytest.mark.order(17)
@pytest.mark.prod_usersfile
def test_testrun_info_IOS_PDF2(main_homepage, ios_flag, sheet):
    page = main_homepage
    IOS_testrun_usersfile_PDF2 = page.locator(testrun_first).filter(
        has_text=re.compile(r"PDF_하단\s*컨트롤러", re.IGNORECASE)
    ).first

    try:
        IOS_testrun_usersfile_PDF2.wait_for(state="attached", timeout=5000)
        IOS_testrun_usersfile_PDF2.scroll_into_view_if_needed()
        IOS_testrun_usersfile_PDF2.wait_for(state="visible", timeout=5000)
        IOS_testrun_usersfile_PDF2.click()
    
        IOS_testrun_info = get_testrun_info(page, testrun_id_section)
        write_result_by_key(sheet, TCID2, IOS_testrun_info, column="T")

    except Exception as e:
        write_result_by_key(sheet, TCID2, "No Info", column="T")
        ios_flag["run"] = False
        pytest.skip("⚠️ IOS 테스트 결과 없음 - 테스트 정보 확인 skip")

@pytest.mark.order(18)
@pytest.mark.prod_usersfile
def test_check_testresult_IOS_PDF2(main_homepage, ios_flag, sheet):
    if not ios_flag["run"]:
        write_result_by_key(sheet, TCID2, "N/T", column="R")
        pytest.skip("⚠️ IOS 테스트 결과 없음 - 결과 확인 skip")

    page = main_homepage
    App_CheckList_414_iOS = get_testrun_status_IOS(page, testrun_status)
    write_result_by_key(sheet, TCID2, App_CheckList_414_iOS, column="R")

@pytest.mark.order(19)
@pytest.mark.prod_usersfile
def test_back_testrun_list_IOS_PDF2(main_homepage, ios_flag):
    back_and_or_reset_IOS(main_homepage, ios_flag.get("run", False))

# -------------------------------
# ⌛ [Stage] 사용자파일 프로젝트 ⌛
# ------------------------------


# -------------------------------
# 자동화 테스트 결과 비교
# -------------------------------

# 비교할 key 값 리스트
keys_to_copy = ["App_CheckList_412", "App_CheckList_413", "App_CheckList_414"]

@pytest.mark.prod_usersfile
@pytest.mark.stg_usersfile
@pytest.mark.order(12)
def test_copy_cell_if_match(sheet):
    sheet1 = sheet
    sheet2 = sheet.spreadsheet.worksheet(f"App_Regression_Checklist {CHECKLIST_VERSION}")

    # 특정 key 값만 비교/복사
    for key in keys_to_copy:
        copy_if_match_by_key(
            sheet1,
            sheet2,
            key_col1="E",
            key_col2="B",
            copy_map={
                "P": "J",
                "Q": "K",
                "R": "L",
            },
            key_value=key
        )

