import pytest
import re
from common_utils import *
from conftest import *

# -------------------------------
# 로그인&계정전환 + 프로젝트 폴더 진입
# -------------------------------
@pytest.mark.order(1)
@pytest.mark.prod_preview
@pytest.mark.stg_preview
def test_login_enter_project(main_homepage):
    page = main_homepage
    login_and_select_project(page)

# -------------------------------
# [Prod] 작품홈 미리보기 프로젝트
# -------------------------------
TCID_general = [ "App_CheckList_278", "App_CheckList_279"]
TCID_general_set = [ "App_CheckList_280"]


@pytest.mark.order(2)
@pytest.mark.prod_preview
def test_project_preview(main_homepage):
    page = main_homepage
    page.click(prod_preview)

    target_project = page.locator(project_title).get_by_text("[Prod] 작품 홈_미리보기")
    try:
        target_project.wait_for(state="visible", timeout=5000)
    except TimeoutError:
        assert False, f"❌ {prod_preview} 폴더 진입 실패"

    assert target_project.is_visible(), f"❌ {prod_preview} 폴더 진입 실패"

@pytest.mark.order(3)
@pytest.mark.prod_preview
def test_checkresult(main_homepage):
    page = main_homepage
    targets = [
            (title_recent_result, "Recent Test Runs"),
        ]

    click_and_verify(page, btn_test_run, targets)
    select_rows(page)

"""
📍 작품 홈_미리보기_default-ebook_일반도서_단권
"""    
@pytest.mark.order(4)
@pytest.mark.prod_preview
def test_checkresult_AOS(main_homepage):
    page = main_homepage
    apply_filter_checkbox_AOS(page)

@pytest.mark.order(5)
@pytest.mark.prod_preview
def test_testrun_info_AOS(main_homepage, aos_flag, sheet):
    page = main_homepage
    AOS_testrun_preview_default_general= page.locator(testrun_first).filter(
        has_text=re.compile(r"^작품 홈_미리보기_default-ebook_일반도서_단권$", re.IGNORECASE) 
    ).first

    try:
        AOS_testrun_preview_default_general.wait_for(state="attached", timeout=5000)
        AOS_testrun_preview_default_general.scroll_into_view_if_needed()
        AOS_testrun_preview_default_general.wait_for(state="visible", timeout=5000)
        AOS_testrun_preview_default_general.click()

        AOS_testrun_info = get_testrun_info(page, testrun_id_section)
        write_result_by_key(sheet, TCID_general, AOS_testrun_info, column="S")

    except Exception as e:
        write_result_by_key(sheet, TCID_general, "No Info", column="S")
        aos_flag["run"] = False
        pytest.skip("⚠️ AOS 테스트 결과 없음 - 테스트 정보 확인 skip")

@pytest.mark.order(6)
@pytest.mark.prod_preview
def test_check_testresult_AOS(main_homepage, aos_flag, sheet):
    if not aos_flag["run"]:
        write_result_by_key(sheet, TCID_general, "N/T", column="P")
        pytest.skip("⚠️ AOS 테스트 결과 없음 - 결과 확인 skip")

    page = main_homepage
    App_CheckList_278_AOS = get_testrun_status_AOS(page, testrun_status)
    write_result_by_key(sheet, TCID_general, App_CheckList_278_AOS, column="P")

@pytest.mark.order(7)
@pytest.mark.prod_preview
def test_back_testrun_list_AOS(main_homepage, aos_flag):
    back_and_or_reset_AOS(main_homepage, aos_flag.get("run", False))

@pytest.mark.order(8)
@pytest.mark.prod_preview
def test_checkresult_IOS(main_homepage):
    page = main_homepage
    apply_filter_checkbox_iOS(page)

@pytest.mark.order(9)
@pytest.mark.prod_preview
def test_testrun_info_IOS(main_homepage, ios_flag, sheet):
    page = main_homepage
    IOS_testrun_preview_default_general = page.locator(testrun_first).filter(
        has_text=re.compile(r"^작품 홈_미리보기_default-ebook_일반도서_단권$", re.IGNORECASE) 
    ).first

    try:
        IOS_testrun_preview_default_general.wait_for(state="attached", timeout=5000)
        IOS_testrun_preview_default_general.scroll_into_view_if_needed()
        IOS_testrun_preview_default_general.wait_for(state="visible", timeout=5000)
        IOS_testrun_preview_default_general.click()

        IOS_testrun_info = get_testrun_info(page, testrun_id_section)
        write_result_by_key(sheet, TCID_general, IOS_testrun_info, column="T")

    except Exception as e:
        write_result_by_key(sheet, TCID_general, "No Info", column="T")
        ios_flag["run"] = False
        pytest.skip("⚠️ IOS 테스트 결과 없음 - 테스트 정보 확인 skip")

@pytest.mark.order(10)
@pytest.mark.prod_preview
def test_check_testresult_IOS(main_homepage, ios_flag, sheet):
    if not ios_flag["run"]:
        write_result_by_key(sheet, TCID_general, "N/T", column="R")
        pytest.skip("⚠️ AOS 테스트 결과 없음 - 결과 확인 skip")

    page = main_homepage
    App_CheckList_278_iOS = get_testrun_status_IOS(page, testrun_status)
    write_result_by_key(sheet, TCID_general, App_CheckList_278_iOS, column="R")

@pytest.mark.order(11)
@pytest.mark.prod_preview
def test_back_testrun_list_IOS(main_homepage, ios_flag):
    back_and_or_reset_IOS(main_homepage, ios_flag.get("run", False))

"""
📍작품 홈_미리보기_default-ebook_일반도서_세트
"""    
@pytest.mark.order(12)
@pytest.mark.prod_preview
def test_checkresult_AOS(main_homepage):
    page = main_homepage
    apply_filter_checkbox_AOS(page)

@pytest.mark.order(13)
@pytest.mark.prod_preview
def test_testrun_info_AOS(main_homepage, aos_flag, sheet):
    page = main_homepage
    AOS_testrun_preview_default_general_set= page.locator(testrun_first).filter(
        has_text=re.compile(r"^작품 홈_미리보기_default-ebook_일반도서_세트$", re.IGNORECASE) 
    ).first

    try:
        AOS_testrun_preview_default_general_set.wait_for(state="attached", timeout=5000)
        AOS_testrun_preview_default_general_set.scroll_into_view_if_needed()
        AOS_testrun_preview_default_general_set.wait_for(state="visible", timeout=5000)
        AOS_testrun_preview_default_general_set.click()

        AOS_testrun_info = get_testrun_info(page, testrun_id_section)
        write_result_by_key(sheet, TCID_general_set, AOS_testrun_info, column="S")

    except Exception as e:
        write_result_by_key(sheet, TCID_general_set, "No Info", column="S")
        aos_flag["run"] = False
        pytest.skip("⚠️ AOS 테스트 결과 없음 - 테스트 정보 확인 skip")

@pytest.mark.order(14)
@pytest.mark.prod_preview
def test_check_testresult_AOS(main_homepage, aos_flag, sheet):
    if not aos_flag["run"]:
        write_result_by_key(sheet, TCID_general_set, "N/T", column="P")
        pytest.skip("⚠️ AOS 테스트 결과 없음 - 결과 확인 skip")

    page = main_homepage
    App_CheckList_280_AOS = get_testrun_status_AOS(page, testrun_status)
    write_result_by_key(sheet, TCID_general_set, App_CheckList_280_AOS, column="P")

@pytest.mark.order(15)
@pytest.mark.prod_preview
def test_back_testrun_list_AOS(main_homepage, aos_flag):
    back_and_or_reset_AOS(main_homepage, aos_flag.get("run", False))

@pytest.mark.order(16)
@pytest.mark.prod_preview
def test_checkresult_IOS(main_homepage):
    page = main_homepage
    apply_filter_checkbox_iOS(page)

@pytest.mark.order(17)
@pytest.mark.prod_preview
def test_testrun_info_IOS(main_homepage, ios_flag, sheet):
    page = main_homepage
    IOS_testrun_preview_default_general_set = page.locator(testrun_first).filter(
        has_text=re.compile(r"^작품 홈_미리보기_default-ebook_일반도서_세트$", re.IGNORECASE) 
    ).first

    try:
        IOS_testrun_preview_default_general_set.wait_for(state="attached", timeout=5000)
        IOS_testrun_preview_default_general_set.scroll_into_view_if_needed()
        IOS_testrun_preview_default_general_set.wait_for(state="visible", timeout=5000)
        IOS_testrun_preview_default_general_set.click()

        IOS_testrun_info = get_testrun_info(page, testrun_id_section)
        write_result_by_key(sheet, TCID_general_set, IOS_testrun_info, column="T")

    except Exception as e:
        write_result_by_key(sheet, TCID_general_set, "No Info", column="T")
        ios_flag["run"] = False
        pytest.skip("⚠️ IOS 테스트 결과 없음 - 테스트 정보 확인 skip")

@pytest.mark.order(18)
@pytest.mark.prod_preview
def test_check_testresult_IOS(main_homepage, ios_flag, sheet):
    if not ios_flag["run"]:
        write_result_by_key(sheet, TCID_general_set, "N/T", column="R")
        pytest.skip("⚠️ AOS 테스트 결과 없음 - 결과 확인 skip")

    page = main_homepage
    App_CheckList_280_iOS = get_testrun_status_IOS(page, testrun_status)
    write_result_by_key(sheet, TCID_general_set, App_CheckList_280_iOS, column="R")

@pytest.mark.order(19)
@pytest.mark.prod_preview
def test_back_testrun_list_IOS(main_homepage, ios_flag):
    back_and_or_reset_IOS(main_homepage, ios_flag.get("run", False))


# -------------------------------
# ⌛ [Stage] 작품홈_미리보기 프로젝트 ⌛
# ------------------------------


# -------------------------------
# 자동화 테스트 결과 비교
# -------------------------------
# 비교할 key 값 리스트
keys_to_copy = [ "App_CheckList_278", "App_CheckList_279", "App_CheckList_280"]

@pytest.mark.prod_preview
@pytest.mark.stg_preview
@pytest.mark.order(20)
def test_copy_cell_if_match(sheet):
    sheet1 = sheet
    sheet2 = sheet.spreadsheet.worksheet("App_Regression_Checklist v4.5")

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