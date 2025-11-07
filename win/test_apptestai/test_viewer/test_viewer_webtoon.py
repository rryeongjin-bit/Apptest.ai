import pytest
import re
from common_utils import *
from conftest import *

# -------------------------------
# 로그인&계정전환 + 프로젝트 폴더 진입
# -------------------------------
@pytest.mark.order(1)
@pytest.mark.prod_viewer
@pytest.mark.stg_genrehome
def test_login_enter_project(main_homepage):
    page = main_homepage
    login_and_select_project(page)

# -------------------------------
# [Prod] 뷰어 프로젝트
# -------------------------------

@pytest.mark.order(2)
@pytest.mark.prod_viewer
def test_project_genrehome(main_homepage):
    page = main_homepage
    page.click(prod_viewer)

    target_project = page.locator(project_title).get_by_text("[Prod] 뷰어")
    try:
        target_project.wait_for(state="visible", timeout=5000)
    except TimeoutError:
        assert False, f"❌ {prod_viewer} 폴더 진입 실패"

    assert target_project.is_visible(), f"❌ {prod_viewer} 폴더 진입 실패"

@pytest.mark.order(3)
@pytest.mark.prod_viewer
def test_checkresult(main_homepage):
    page = main_homepage
    targets = [
            (title_recent_result, "Recent Test Runs"),
        ]

    click_and_verify(page, btn_test_run, targets)
    select_rows(page)

"""
📍 뷰어_webtoon_상단 컨트롤러/본문
"""    
@pytest.mark.order(4)
@pytest.mark.prod_viewer
def test_checkresult_AOS(main_homepage):
    page = main_homepage
    apply_filter_checkbox_AOS(page)

@pytest.mark.order(5)
@pytest.mark.prod_viewer
def test_testrun_info_AOS(main_homepage, write_result,aos_flag):
    page = main_homepage
    AOS_testrun_webtoon_top = page.locator(testrun_first).filter(
        has_text=re.compile(r"Webtoon_상단\s*컨트롤러", re.IGNORECASE) 
    ).first

    try:
        AOS_testrun_webtoon_top.wait_for(state="visible", timeout=10000)
        AOS_testrun_webtoon_top.scroll_into_view_if_needed()
        AOS_testrun_webtoon_top.click()

        AOS_testrun_info = get_testrun_info(page, testrun_id_section)
        for step in ["S429","S430","S431","S432","S433"]:
            write_result(step, AOS_testrun_info)

    except Exception as e:
        for step in ["S429","S430","S431","S432","S433"]:
            write_result(step, "No Info")
        aos_flag["run"] = False
        pytest.skip("⚠️ AOS 테스트 결과 없음 - 테스트 정보 확인 skip")

@pytest.mark.order(6)
@pytest.mark.prod_viewer
def test_check_testresult_AOS(main_homepage, write_result, aos_flag):
    if not aos_flag["run"]:
        for step in ["P429","P430","P431","P432","P433"]:
            write_result(step, "N/T")
        pytest.skip("⚠️ AOS 테스트 결과 없음 - 결과 확인 skip")

    page = main_homepage
    App_CheckList_383_AOS = get_testrun_status_AOS(page, testrun_status)
    
    for step in ["P429","P430","P431","P432","P433"]:
        write_result(step, App_CheckList_383_AOS)

@pytest.mark.order(7)
@pytest.mark.prod_viewer
def test_back_testrun_list_AOS(main_homepage, aos_flag):
    back_and_or_reset_AOS(main_homepage, aos_flag.get("run", False))

@pytest.mark.order(8)
@pytest.mark.prod_viewer
def test_checkresult_IOS(main_homepage):
    page = main_homepage
    apply_filter_checkbox_iOS(page)

@pytest.mark.order(9)
@pytest.mark.prod_viewer
def test_testrun_info_IOS(main_homepage,write_result, ios_flag):
    page = main_homepage
    IOS_testrun_webtoon_top = page.locator(testrun_first).filter(
        has_text=re.compile(r"Webtoon_상단\s*컨트롤러", re.IGNORECASE) 
    ).first

    try:
        IOS_testrun_webtoon_top.wait_for(state="visible", timeout=10000)
        IOS_testrun_webtoon_top.scroll_into_view_if_needed()
        IOS_testrun_webtoon_top.click()
    
        IOS_testrun_info = get_testrun_info(page, testrun_id_section)
        for step in ["T429","T430","T431","T432","T433"]:
            write_result(step, IOS_testrun_info)

    except Exception as e:
        for step in ["T429","T430","T431","T432","T433"]:
            write_result(step, "No Info")
        ios_flag["run"] = False
        pytest.skip("⚠️ IOS 테스트 결과 없음 - 테스트 정보 확인 skip")

@pytest.mark.order(10)
@pytest.mark.prod_viewer
def test_check_testresult_IOS(main_homepage, write_result,ios_flag):
    if not ios_flag["run"]:
        for step in ["R429","R430","R431","R432","R433"]:
            write_result(step, "N/T")
        pytest.skip("⚠️ AOS 테스트 결과 없음 - 결과 확인 skip")

    page = main_homepage
    App_CheckList_383_iOS = get_testrun_status_IOS(page, testrun_status)
   
    for step in ["R429","R430","R431","R432","R433"]:
        write_result(step, App_CheckList_383_iOS)

@pytest.mark.order(11)
@pytest.mark.prod_viewer
def test_back_testrun_list_IOS(main_homepage, ios_flag):
    back_and_or_reset_IOS(main_homepage, ios_flag.get("run", False))

"""
📍 뷰어_webtoon_하단 컨트롤러
"""    
@pytest.mark.order(12)
@pytest.mark.prod_viewer
def test_checkresult_AOS(main_homepage):
    page = main_homepage
    apply_filter_checkbox_AOS(page)

@pytest.mark.order(13)
@pytest.mark.prod_viewer
def test_testrun_info_AOS(main_homepage, write_result,aos_flag):
    page = main_homepage
    AOS_testrun_webtoon_bottom = page.locator(testrun_first).filter(
        has_text=re.compile(r"Webtoon_하단\s*컨트롤러$", re.IGNORECASE) 
    ).first

    try:
        AOS_testrun_webtoon_bottom.wait_for(state="visible", timeout=10000)
        AOS_testrun_webtoon_bottom.scroll_into_view_if_needed()
        AOS_testrun_webtoon_bottom.click()

        AOS_testrun_info = get_testrun_info(page, testrun_id_section)
        for step in ["S434","S435","S438","S439","S440"]:
            write_result(step, AOS_testrun_info)

    except Exception as e:
        for step in ["S434","S435","S438","S439","S440"]:
            write_result(step, "No Info")
        aos_flag["run"] = False
        pytest.skip("⚠️ AOS 테스트 결과 없음 - 테스트 정보 확인 skip")

@pytest.mark.order(14)
@pytest.mark.prod_viewer
def test_check_testresult_AOS(main_homepage, write_result, aos_flag):
    if not aos_flag["run"]:
        for step in ["P434","P435","P438","P439","P440"]:
            write_result(step, "N/T")
        pytest.skip("⚠️ AOS 테스트 결과 없음 - 결과 확인 skip")

    page = main_homepage
    App_CheckList_388_AOS = get_testrun_status_AOS(page, testrun_status)
    
    for step in ["P434","P435","P438","P439","P440"]:
        write_result(step, App_CheckList_388_AOS)

@pytest.mark.order(15)
@pytest.mark.prod_viewer
def test_back_testrun_list_AOS(main_homepage, aos_flag):
    back_and_or_reset_AOS(main_homepage, aos_flag.get("run", False))

@pytest.mark.order(16)
@pytest.mark.prod_viewer
def test_checkresult_IOS(main_homepage):
    page = main_homepage
    apply_filter_checkbox_iOS(page)

@pytest.mark.order(17)
@pytest.mark.prod_viewer
def test_testrun_info_IOS(main_homepage,write_result, ios_flag):
    page = main_homepage
    IOS_testrun_webtoon_bottom = page.locator(testrun_first).filter(
        has_text=re.compile(r"Webtoon_하단\s*컨트롤러$", re.IGNORECASE) 
    ).first

    try:
        IOS_testrun_webtoon_bottom.wait_for(state="visible", timeout=10000)
        IOS_testrun_webtoon_bottom.scroll_into_view_if_needed()
        IOS_testrun_webtoon_bottom.click()
    
        IOS_testrun_info = get_testrun_info(page, testrun_id_section)
        for step in ["T434","T435","T438","T439","T440"]:
            write_result(step, IOS_testrun_info)

    except Exception as e:
        for step in ["T434","T435","T438","T439","T440"]:
            write_result(step, "No Info")
        ios_flag["run"] = False
        pytest.skip("⚠️ IOS 테스트 결과 없음 - 테스트 정보 확인 skip")

@pytest.mark.order(18)
@pytest.mark.prod_viewer
def test_check_testresult_IOS(main_homepage, write_result,ios_flag):
    if not ios_flag["run"]:
        for step in ["R434","R435","R438","R439","R440"]:
            write_result(step, "N/T")
        pytest.skip("⚠️ AOS 테스트 결과 없음 - 결과 확인 skip")

    page = main_homepage
    App_CheckList_388_iOS = get_testrun_status_IOS(page, testrun_status)
   
    for step in ["R434","R435","R438","R439","R440"]:
        write_result(step, App_CheckList_388_iOS)

@pytest.mark.order(19)
@pytest.mark.prod_viewer
def test_back_testrun_list_IOS(main_homepage, ios_flag):
    back_and_or_reset_IOS(main_homepage, ios_flag.get("run", False))


# -------------------------------
# ⌛ [Stage] 뷰어 프로젝트 ⌛
# ------------------------------


# -------------------------------
# 자동화 테스트 결과 비교
# -------------------------------

# 비교 (1번시트 row, 2번시트 row)
row_pairs = [
    (441, 412),
    (430, 413),
    (431, 414),
    (432, 415),
    (433, 416),
    (434, 417),
    (435, 418),
    (438, 421)
]
# 열 매핑 및 비교 열
col1 = "E"  # 1번시트 비교 열
col2 = "B"  # 2번시트 비교 열
copy_map = {
    "P": "J",
    "Q": "K",
    "R": "L",
}

@pytest.mark.prod_viewer
@pytest.mark.stg_viewer
@pytest.mark.order(20)
@pytest.mark.parametrize("row1,row2", row_pairs)
def test_copy_cell_if_match(sheet, row1, row2):
    sheet1 = sheet
    sheet2 = sheet.spreadsheet.worksheet("App_Regression_Checklist v4.5")
    copy_if_match(sheet1, sheet2, row1, row2, col1, col2, copy_map)
