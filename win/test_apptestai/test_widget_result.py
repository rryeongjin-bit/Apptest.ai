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
    
@pytest.mark.order(4)
@pytest.mark.prod_widget
def test_checkresult_AOS(main_homepage):
    page = main_homepage
    apply_filter_checkbox_AOS(page)

@pytest.mark.order(5)
@pytest.mark.prod_widget
def test_testrun_info_AOS(main_homepage, write_result,aos_flag):
    page = main_homepage
    AOS_testrun_widget = page.locator(testrun_first).filter(
        has_text=re.compile(r"숏컷_위젯", re.IGNORECASE)
    ).first

    try:
        AOS_testrun_widget.wait_for(state="visible", timeout=10000)
        AOS_testrun_widget.scroll_into_view_if_needed()
        AOS_testrun_widget.click()

        AOS_testrun_info = get_testrun_info(page, testrun_id_section)
        write_result("S478", AOS_testrun_info)
        write_result("S477", AOS_testrun_info)
    except Exception as e:

        write_result("S478", "No Info")
        write_result("S477", "No Info")
        aos_flag["run"] = False
        pytest.skip("⚠️ AOS 테스트 결과 없음 - 테스트 정보 확인 skip")

@pytest.mark.order(6)
@pytest.mark.prod_widget
def test_check_testresult_AOS(main_homepage, write_result, aos_flag):
    if not aos_flag["run"]:
        write_result("P478", "N/T")
        write_result("P477", "N/T")
        pytest.skip("⚠️ AOS 테스트 결과 없음 - 결과 확인 skip")

    page = main_homepage
    App_CheckList_478_AOS= get_testrun_status_AOS(page, testrun_status, testrun_result_message_AOS)
    write_result("P478", App_CheckList_478_AOS)
    write_result("P477", App_CheckList_478_AOS)

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
def test_testrun_info_IOS(main_homepage,write_result, ios_flag):
    page = main_homepage
    IOS_testrun_widget = page.locator(testrun_first).filter(
        has_text=re.compile(r"숏컷_위젯", re.IGNORECASE)
    ).first

    try:
        IOS_testrun_widget.wait_for(state="visible", timeout=10000)
        IOS_testrun_widget.scroll_into_view_if_needed()
        IOS_testrun_widget.click()
    
        IOS_testrun_info = get_testrun_info(page, testrun_id_section)
        write_result("T479", IOS_testrun_info)
        write_result("T477", IOS_testrun_info)
    except Exception as e:
        write_result("T479", "No Info")
        write_result("T477", "No Info")
        ios_flag["run"] = False
        pytest.skip("⚠️ IOS 테스트 결과 없음 - 테스트 정보 확인 skip")

@pytest.mark.order(10)
@pytest.mark.prod_widget
def test_check_testresult_IOS(main_homepage, write_result,ios_flag):
    if not ios_flag["run"]:
        write_result("R479", "N/T")
        write_result("R477", "N/T")
        pytest.skip("⚠️ IOS 테스트 결과 없음 - 결과 확인 skip")

    page = main_homepage
    App_CheckList_479_iOS = get_testrun_status_IOS(page, testrun_status, testrun_result_message_IOS)
    write_result("R479", App_CheckList_479_iOS)
    write_result("R477", App_CheckList_479_iOS)

@pytest.mark.order(11)
@pytest.mark.prod_widget
def test_back_testrun_list_IOS(main_homepage, ios_flag):
    back_and_or_reset_IOS(main_homepage, ios_flag.get("run", False))

# -------------------------------
# ⌛ [Stage] 위젯 프로젝트 ⌛
# ------------------------------


# -------------------------------
# 자동화 테스트 결과 비교
# -------------------------------

# 비교 (1번시트 row, 2번시트 row)
row_pairs = [
    (477, 449),
    (478, 450),
    (479, 451),
]

# 열 매핑 및 비교 열
col1 = "E"  # 1번시트 비교 열
col2 = "B"  # 2번시트 비교 열
copy_map = {
    "P": "J",
    "Q": "K",
    "R": "L",
}

@pytest.mark.prod_widget
@pytest.mark.stg_widget
@pytest.mark.order(12)
@pytest.mark.parametrize("row1,row2", row_pairs)
def test_copy_cell_if_match(sheet, row1, row2):
    sheet1 = sheet
    sheet2 = sheet.spreadsheet.worksheet("App_Regression_Checklist v4.5")

    val1 = sheet1.acell(f"{col1}{row1}").value
    val2 = sheet2.acell(f"{col2}{row2}").value
    print(f"🔎 비교: 1번시트 {col1}{row1}={val1!r}, 2번시트 {col2}{row2}={val2!r}")

    if val1 == val2:
        print(f"✅ 값 일치 → 1번시트(O,P,Q{row1}) → 2번시트(J,K,L{row2}) 복사 시작")
        for c1, c2 in copy_map.items():
            value = sheet1.acell(f"{c1}{row1}").value
            sheet2.update_acell(f"{c2}{row2}", value)
            print(f"📋 복사: {c1}{row1} → {c2}{row2} ({value})")
    else:
        print(f"❌ {row1}행 ↔ {row2}행: 값 불일치 → 복사 안 함")

    print("🏁 결과 복사 완료!")


