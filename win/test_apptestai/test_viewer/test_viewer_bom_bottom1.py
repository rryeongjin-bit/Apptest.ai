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
📍 뷰어_BOM_BOM_하단 컨트롤러(상단기능/프로그래스/목차/독서노트/보기설정)
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
    AOS_testrun_bom_bottom1 = page.locator(testrun_first).filter(
        has_text=re.compile(r"^\[뷰어\]\s*BOM_BOM_하단\s*컨트롤러\(상단기능/프로그래스/목차/독서노트/보기설정\)$", re.IGNORECASE)  
    ).first

    try:
        AOS_testrun_bom_bottom1.wait_for(state="visible", timeout=10000)
        AOS_testrun_bom_bottom1.scroll_into_view_if_needed()
        AOS_testrun_bom_bottom1.click()

        AOS_testrun_info = get_testrun_info(page, testrun_id_section)
        for step in  ["S358","S359","S360","S361","S362","S363","S364"]:
            write_result(step, AOS_testrun_info)

    except Exception as e:
        for step in ["S358","S359","S360","S361","S362","S363","S364"]:
            write_result(step, "No Info")
        aos_flag["run"] = False
        pytest.skip("⚠️ AOS 테스트 결과 없음 - 테스트 정보 확인 skip")

@pytest.mark.order(6)
@pytest.mark.prod_viewer
def test_check_testresult_AOS(main_homepage, write_result, aos_flag):
    if not aos_flag["run"]:
        for step in ["P358","P359","P360","P361","P362","P363","P364"]:
            write_result(step, "N/T")
        pytest.skip("⚠️ AOS 테스트 결과 없음 - 결과 확인 skip")

    page = main_homepage
    App_CheckList_342_AOS = get_testrun_status_AOS(page, testrun_status)
    
    for step in ["P358","P359","P360","P361","P362","P363","P364"]:
        write_result(step, App_CheckList_342_AOS)

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
    IOS_testrun_bom_bottom1 = page.locator(testrun_first).filter(
         has_text=re.compile(r"^\[뷰어\]\s*BOM_BOM_하단\s*컨트롤러\(상단기능/프로그래스/목차/독서노트/보기설정\)$", re.IGNORECASE)  
    ).first

    try:
        IOS_testrun_bom_bottom1.wait_for(state="visible", timeout=10000)
        IOS_testrun_bom_bottom1.scroll_into_view_if_needed()
        IOS_testrun_bom_bottom1.click()
    
        IOS_testrun_info = get_testrun_info(page, testrun_id_section)
        for step in ["T358","T359","T360","T361","T362","T363","T364"]:
            write_result(step, IOS_testrun_info)

    except Exception as e:
        for step in ["T358","T359","T360","T361","T362","T363","T364"]:
            write_result(step, "No Info")
        ios_flag["run"] = False
        pytest.skip("⚠️ IOS 테스트 결과 없음 - 테스트 정보 확인 skip")

@pytest.mark.order(10)
@pytest.mark.prod_viewer
def test_check_testresult_IOS(main_homepage, write_result,ios_flag):
    if not ios_flag["run"]:
        for step in ["R358","R359","R360","R361","R362","R363","R364"]:
            write_result(step, "N/T")
        pytest.skip("⚠️ AOS 테스트 결과 없음 - 결과 확인 skip")

    page = main_homepage
    App_CheckList_342_iOS = get_testrun_status_IOS(page, testrun_status)
   
    for step in ["R358","R359","R360","R361","R362","R363","R364"]:
        write_result(step, App_CheckList_342_iOS)

@pytest.mark.order(11)
@pytest.mark.prod_viewer
def test_back_testrun_list_IOS(main_homepage, ios_flag):
    back_and_or_reset_IOS(main_homepage, ios_flag.get("run", False))

# -------------------------------
# ⌛ [Stage] 뷰어 프로젝트 ⌛
# ------------------------------


# -------------------------------
# 자동화 테스트 결과 비교
# -------------------------------

# # 비교 (1번시트 row, 2번시트 row)
row_pairs = [
    (358, 369),
    (359, 370),
    (360, 371),
    (361, 372),
    (362, 373),
    (363, 374),
    (364, 375)
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
@pytest.mark.order(12)
@pytest.mark.parametrize("row1,row2", row_pairs)
def test_copy_cell_if_match(sheet, row1, row2):
    sheet1 = sheet
    sheet2 = sheet.spreadsheet.worksheet("App_Regression_Checklist v4.5")
    copy_if_match(sheet1, sheet2, row1, row2, col1, col2, copy_map)
