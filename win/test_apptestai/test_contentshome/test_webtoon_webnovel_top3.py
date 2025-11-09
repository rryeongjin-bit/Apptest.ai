import pytest
import re
from element_total import *
from common_utils import *
from conftest import *

# -------------------------------
# 로그인&계정전환 + 프로젝트 폴더 진입
# -------------------------------
@pytest.mark.order(1)
@pytest.mark.prod_contentshome
@pytest.mark.stg_contentshome
def test_login_enter_project(main_homepage):
    page = main_homepage
    login_and_select_project(page)

# -------------------------------
# [Prod] 작품홈 프로젝트
# -------------------------------

@pytest.mark.order(2)
@pytest.mark.prod_contentshome
def test_project_contentshome(main_homepage):
    page = main_homepage
    page.click(prod_contentshome)

    target_project = page.locator(project_title).get_by_text("[Prod] 장르홈")
    try:
        target_project.wait_for(state="visible", timeout=5000)
    except TimeoutError:
        assert False, f"❌ {prod_contentshome} 폴더 진입 실패"

    assert target_project.is_visible(), f"❌ {prod_contentshome} 폴더 진입 실패"

@pytest.mark.order(3)
@pytest.mark.prod_contentshome
def test_checkresult(main_homepage):
    page = main_homepage
    targets = [
            (title_recent_result, "Recent Test Runs"),
        ]

    click_and_verify(page, btn_test_run, targets)
    select_rows(page)

"""
📍 작품 홈_webtoon-webnovel_상단 영역_무료이용권
"""    
@pytest.mark.order(4)
@pytest.mark.prod_contentshome
def test_checkresult_AOS(main_homepage):
    page = main_homepage
    apply_filter_checkbox_AOS(page)

@pytest.mark.order(5)
@pytest.mark.prod_contentshome
def test_testrun_info_AOS(main_homepage, write_result,aos_flag):
    page = main_homepage
    AOS_testrun_webtoon_webnovel = page.locator(testrun_first).filter(
        has_text=re.compile(r"작품 홈_webtoon-webnovel_상단 영역_무료이용권", re.IGNORECASE) 
    ).first

    try:
        AOS_testrun_webtoon_webnovel.wait_for(state="visible", timeout=10000)
        AOS_testrun_webtoon_webnovel.scroll_into_view_if_needed()
        AOS_testrun_webtoon_webnovel.click()

        AOS_testrun_info = get_testrun_info(page, testrun_id_section)
        write_result("S182", AOS_testrun_info)

    except Exception as e:
        write_result("S182", "No Info")
        aos_flag["run"] = False
        pytest.skip("⚠️ AOS 테스트 결과 없음 - 테스트 정보 확인 skip")

@pytest.mark.order(6)
@pytest.mark.prod_contentshome
def test_check_testresult_AOS(main_homepage, write_result, aos_flag):
    if not aos_flag["run"]:
        write_result("P182", "N/T")
        pytest.skip("⚠️ AOS 테스트 결과 없음 - 결과 확인 skip")

    page = main_homepage
    App_CheckList_coupon_AOS = get_testrun_status_AOS(page, testrun_status)
    write_result("P182", App_CheckList_coupon_AOS)

@pytest.mark.order(7)
@pytest.mark.prod_contentshome
def test_back_testrun_list_AOS(main_homepage, aos_flag):
    back_and_or_reset_AOS(main_homepage, aos_flag.get("run", False))

@pytest.mark.order(8)
@pytest.mark.prod_contentshome
def test_checkresult_IOS(main_homepage):
    page = main_homepage
    apply_filter_checkbox_iOS(page)

@pytest.mark.order(9)
@pytest.mark.prod_contentshome
def test_testrun_info_IOS(main_homepage,write_result, ios_flag):
    page = main_homepage
    IOS_testrun_webtoon_webnovel= page.locator(testrun_first).filter(
        has_text=re.compile(r"작품 홈_webtoon-webnovel_상단 영역_무료이용권", re.IGNORECASE) 
    ).first

    try:
        IOS_testrun_webtoon_webnovel.wait_for(state="visible", timeout=10000)
        IOS_testrun_webtoon_webnovel.scroll_into_view_if_needed()
        IOS_testrun_webtoon_webnovel.click()
    
        IOS_testrun_info = get_testrun_info(page, testrun_id_section)
        write_result("T182", IOS_testrun_info)

    except Exception as e:
        write_result("T182", "No Info")
        ios_flag["run"] = False
        pytest.skip("⚠️ IOS 테스트 결과 없음 - 테스트 정보 확인 skip")

@pytest.mark.order(10)
@pytest.mark.prod_contentshome
def test_check_testresult_IOS(main_homepage, write_result,ios_flag):
    if not ios_flag["run"]:
        write_result("R182", "N/T")
        pytest.skip("⚠️ AOS 테스트 결과 없음 - 결과 확인 skip")

    page = main_homepage
    App_CheckList_coupon_iOS = get_testrun_status_IOS(page, testrun_status)
    write_result("R182", App_CheckList_coupon_iOS)

@pytest.mark.order(11)
@pytest.mark.prod_contentshome
def test_back_testrun_list_IOS(main_homepage, ios_flag):
    back_and_or_reset_IOS(main_homepage, ios_flag.get("run", False))

"""
📍 작품 홈_webtoon-webnovel_상단 영역_리다무
"""    
@pytest.mark.order(12)
@pytest.mark.prod_contentshome
def test_checkresult_AOS(main_homepage):
    page = main_homepage
    apply_filter_checkbox_AOS(page)

@pytest.mark.order(13)
@pytest.mark.prod_contentshome
def test_testrun_info_AOS(main_homepage, write_result,aos_flag):
    page = main_homepage
    AOS_testrun_webtoon_webnovel = page.locator(testrun_first).filter(
        has_text=re.compile(r"작품 홈_webtoon-webnovel_상단 영역_리다무", re.IGNORECASE) 
    ).first

    try:
        AOS_testrun_webtoon_webnovel.wait_for(state="visible", timeout=10000)
        AOS_testrun_webtoon_webnovel.scroll_into_view_if_needed()
        AOS_testrun_webtoon_webnovel.click()

        AOS_testrun_info = get_testrun_info(page, testrun_id_section)
        write_result("S183", AOS_testrun_info)

    except Exception as e:
        write_result("S183", "No Info")
        aos_flag["run"] = False
        pytest.skip("⚠️ AOS 테스트 결과 없음 - 테스트 정보 확인 skip")

@pytest.mark.order(14)
@pytest.mark.prod_contentshome
def test_check_testresult_AOS(main_homepage, write_result, aos_flag):
    if not aos_flag["run"]:
        write_result("P183", "N/T")
        pytest.skip("⚠️ AOS 테스트 결과 없음 - 결과 확인 skip")

    page = main_homepage
    App_CheckList_174_AOS = get_testrun_status_AOS(page, testrun_status)
    write_result("P183", App_CheckList_174_AOS)

@pytest.mark.order(15)
@pytest.mark.prod_contentshome
def test_back_testrun_list_AOS(main_homepage, aos_flag):
    back_and_or_reset_AOS(main_homepage, aos_flag.get("run", False))

@pytest.mark.order(16)
@pytest.mark.prod_contentshome
def test_checkresult_IOS(main_homepage):
    page = main_homepage
    apply_filter_checkbox_iOS(page)

@pytest.mark.order(17)
@pytest.mark.prod_contentshome
def test_testrun_info_IOS(main_homepage, write_result,ios_flag):
    page = main_homepage
    IOS_testrun_webtoon_webnovel = page.locator(testrun_first).filter(
        has_text=re.compile(r"작품 홈_webtoon-webnovel_상단 영역_리다무", re.IGNORECASE) 
    ).first

    try:
        IOS_testrun_webtoon_webnovel.wait_for(state="visible", timeout=10000)
        IOS_testrun_webtoon_webnovel.scroll_into_view_if_needed()
        IOS_testrun_webtoon_webnovel.click()

        IOS_testrun_info = get_testrun_info(page, testrun_id_section)
        write_result("T183", IOS_testrun_info)

    except Exception as e:
        write_result("T183", "No Info")
        ios_flag["run"] = False
        pytest.skip("⚠️ IOS 테스트 결과 없음 - 테스트 정보 확인 skip")

@pytest.mark.order(18)
@pytest.mark.prod_contentshome
def test_check_testresult_IOS(main_homepage, write_result, ios_flag):
    if not ios_flag["run"]:
        write_result("R183", "N/T")
        pytest.skip("⚠️ IOS 테스트 결과 없음 - 결과 확인 skip")

    page = main_homepage
    App_CheckList_174_IOS = get_testrun_status_IOS(page, testrun_status)
    write_result("R183", App_CheckList_174_IOS)

@pytest.mark.order(19)
@pytest.mark.prod_contentshome
def test_back_testrun_list_IOS(main_homepage, ios_flag):
    back_and_or_reset_IOS(main_homepage, ios_flag.get("run", False))


# -------------------------------
# ⌛ [Stage] 작품홈 프로젝트 ⌛
# ------------------------------


# -------------------------------
# 자동화 테스트 결과 비교
# -------------------------------

# # 비교 (1번시트 row, 2번시트 row)
row_pairs = [
    (183, 194)
]

# 열 매핑 및 비교 열
col1 = "E"  # 1번시트 비교 열
col2 = "B"  # 2번시트 비교 열
copy_map = {
    "P": "J",
    "Q": "K",
    "R": "L",
}

@pytest.mark.prod_contentshome
@pytest.mark.stg_contentshome
@pytest.mark.order(20)
@pytest.mark.parametrize("row1,row2", row_pairs)
def test_copy_cell_if_match(sheet, row1, row2):
    sheet1 = sheet
    sheet2 = sheet.spreadsheet.worksheet("App_Regression_Checklist v4.5")
    copy_if_match(sheet1, sheet2, row1, row2, col1, col2, copy_map)
