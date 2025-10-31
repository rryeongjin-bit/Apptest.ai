import pytest
from element_total import *
from common_utils import *
from conftest import *

# -------------------------------
# 로그인&계정전환 + 프로젝트 폴더 진입
# -------------------------------

@pytest.mark.order(1)
@pytest.mark.default_step
@pytest.mark.prod_widget
@pytest.mark.stg_widget
def test_login(main_homepage):
    page = main_homepage
    page.goto("https://app.apptest.ai")
    assert "Dashboard" in page.inner_text("body")

@pytest.mark.order(2)
@pytest.mark.default_step
@pytest.mark.prod_widget
@pytest.mark.stg_widget
def test_changeaccount(main_homepage):
    page = main_homepage
    page.click(btn_changeaccount)
    page.click(qa_account)
    
    target_account = page.locator(account_section).get_by_text("QA part")
    assert target_account.is_visible(), "❌ QA part 계정 변환되지않음"

@pytest.mark.order(3)
@pytest.mark.default_step
@pytest.mark.prod_widget
@pytest.mark.stg_widget
def test_mobileapp(main_homepage):
    page = main_homepage
    page.click(folder_mobileapp)

    target_folder = page.locator(folder_title_section).get_by_text("Mobile App")
    assert target_folder.is_visible(), f"❌ {folder_mobileapp} 선택 실패"

# -------------------------------
# [Prod] 위젯 프로젝트
# -------------------------------

@pytest.mark.order(4)
@pytest.mark.default_step
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
    
@pytest.mark.order(5)
@pytest.mark.default_step
@pytest.mark.prod_widget
def test_checkresult(main_homepage):
    page = main_homepage
    page.click(btn_test_run)

    targets = [
        (title_recent_result, "Recent Test Runs"),
    ]

    for sel, target_text in targets:
        found = scroll_until_element_found(page, sel)
        assert found, f"❌ 요소를 찾지 못했습니다: {sel}"

@pytest.mark.order(6)
@pytest.mark.default_step
@pytest.mark.prod_widget
def test_checkresult_AOS(main_homepage):
    page = main_homepage
    page.click(btn_test_filter)

    target_title_AOS = page.locator(title_filter_section).get_by_text("Filter")
    assert target_title_AOS.is_visible(), f"❌ {btn_test_filter} 선택 실패"

    container_filter_AOS = page.locator(filter_os_section) 
    AOS_checkbox = container_filter_AOS.locator("img[data-testid='checkBox']").nth(0)

    try:
        AOS_checkbox.scroll_into_view_if_needed()
        AOS_checkbox.wait_for(state="visible", timeout=5000)
        AOS_checkbox.click(force=True)

        AOS_apply_button = page.get_by_role("button", name="Apply")
        AOS_apply_button.wait_for(state="visible", timeout=5000)
        AOS_apply_button.scroll_into_view_if_needed()
        AOS_apply_button.click()

        page.wait_for_timeout(5000)

        AOS_target_element = page.locator(target_filterbox)
        AOS_target_element.wait_for(state="visible", timeout=5000)
        assert AOS_target_element.is_visible(), "❌ Android 필터 적용 실패"
    except Exception as e:
        assert False, f"❌ test device OS 필터 적용 실패: {e}"

@pytest.mark.order(7)
@pytest.mark.default_step
@pytest.mark.prod_widget
def test_testrun_info_AOS(main_homepage, write_result):
    page = main_homepage
    page.click(first_testrun_id)
    AOS_testrun_info = get_testrun_info(page, testrun_id_section)
    write_result("S478", AOS_testrun_info)
    write_result("S477", AOS_testrun_info)

@pytest.mark.order(8)
@pytest.mark.default_step
@pytest.mark.prod_widget
def test_check_testresult_AOS(main_homepage, write_result):
    page = main_homepage
    App_CheckList_478_AOS= get_testrun_status_AOS(page, testrun_status, testrun_result_message_AOS)
    write_result("P478", App_CheckList_478_AOS)
    write_result("P477", "Passed")

@pytest.mark.order(9)
@pytest.mark.default_step
@pytest.mark.prod_widget
def test_back_testrun_list_AOS(main_homepage):
    page = main_homepage
    back_to_testrun_list(page, return_to_testrun, reset_filter)
  
@pytest.mark.order(10)
@pytest.mark.default_step
@pytest.mark.prod_widget
def test_checkresult_IOS(main_homepage):
    page = main_homepage
    page.click(btn_test_filter)

    target_title_IOS= page.locator(title_filter_section).get_by_text("Filter")
    assert target_title_IOS.is_visible(), f"❌ {btn_test_filter} 선택 실패"

    container_filter_IOS = page.locator(filter_os_section) 
    IOS_checkbox = container_filter_IOS.locator("img[data-testid='checkBox']").nth(1)

    try:
        IOS_checkbox.scroll_into_view_if_needed()
        IOS_checkbox.wait_for(state="visible", timeout=5000)
        IOS_checkbox.click(force=True)

        IOS_apply_button = page.get_by_role("button", name="Apply")
        IOS_apply_button.wait_for(state="visible", timeout=5000)
        IOS_apply_button.scroll_into_view_if_needed()
        IOS_apply_button.click()

        page.wait_for_timeout(5000)

        IOS_target_element = page.locator(target_filterbox)
        IOS_target_element.wait_for(state="visible", timeout=5000)
        assert IOS_target_element.is_visible(), "❌ IOS 필터 적용 실패"
    except Exception as e:
        assert False, f"❌ test device OS 필터 적용 실패: {e}"

@pytest.mark.order(11)
@pytest.mark.default_step
@pytest.mark.prod_widget
def test_testrun_info_IOS(main_homepage,write_result):
    page = main_homepage
    page.click(first_testrun_id)
    IOS_testrun_info = get_testrun_info(page, testrun_id_section)
    write_result("T479", IOS_testrun_info)
    write_result("T477", IOS_testrun_info)

@pytest.mark.order(12)
@pytest.mark.default_step
@pytest.mark.prod_widget
def test_check_testresult_IOS(main_homepage, write_result):
    page = main_homepage
    App_CheckList_479_iOS = get_testrun_status_IOS(page, testrun_status, testrun_result_message_IOS)
    write_result("R479", App_CheckList_479_iOS)
    write_result("R477", "Passed")

@pytest.mark.order(13)
@pytest.mark.default_step
@pytest.mark.prod_widget
def test_back_testrun_list_IOS(main_homepage):
    page = main_homepage
    back_to_testrun_list(page, return_to_testrun, reset_filter)


# -------------------------------
# [Stage] 위젯 프로젝트
# -------------------------------

@pytest.mark.order(4)
@pytest.mark.default_step
@pytest.mark.stg_widget
def test_project_widget(main_homepage):
    page = main_homepage
    page.click(stg_widget)

    target_project = page.locator(project_title).get_by_text("[Stage] 위젯")
    try:
        target_project.wait_for(state="visible", timeout=5000)
    except TimeoutError:
        assert False, f"❌ {stg_widget} 폴더 진입 실패"

    assert target_project.is_visible(), f"❌ {stg_widget} 폴더 진입 실패"
    
@pytest.mark.order(5)
@pytest.mark.default_step
@pytest.mark.stg_widget
def test_checkresult(main_homepage):
    page = main_homepage
    page.click(btn_test_run)

    targets = [
        (title_recent_result, "Recent Test Runs"),
    ]

    for sel, target_text in targets:
        found = scroll_until_element_found(page, sel)
        assert found, f"❌ 요소를 찾지 못했습니다: {sel}"

@pytest.mark.order(6)
@pytest.mark.default_step
@pytest.mark.stg_widget
def test_checkresult_AOS(main_homepage):
    page = main_homepage
    page.click(btn_test_filter)

    target_title_AOS = page.locator(title_filter_section).get_by_text("Filter")
    assert target_title_AOS.is_visible(), f"❌ {btn_test_filter} 선택 실패"

    container_filter_AOS = page.locator(filter_os_section) 
    AOS_checkbox = container_filter_AOS.locator("img[data-testid='checkBox']").nth(0)

    try:
        AOS_checkbox.scroll_into_view_if_needed()
        AOS_checkbox.wait_for(state="visible", timeout=5000)
        AOS_checkbox.click(force=True)

        AOS_apply_button = page.get_by_role("button", name="Apply")
        AOS_apply_button.wait_for(state="visible", timeout=5000)
        AOS_apply_button.scroll_into_view_if_needed()
        AOS_apply_button.click()

        page.wait_for_timeout(5000)

        AOS_target_element = page.locator(target_filterbox)
        AOS_target_element.wait_for(state="visible", timeout=5000)
        assert AOS_target_element.is_visible(), "❌ Android 필터 적용 실패"
    except Exception as e:
        assert False, f"❌ test device OS 필터 적용 실패: {e}"

@pytest.mark.order(7)
@pytest.mark.default_step
@pytest.mark.stg_widget
def test_testrun_info_AOS(main_homepage, write_result):
    page = main_homepage
    page.click(first_testrun_id)
    AOS_testrun_info = get_testrun_info(page, testrun_id_section)
    write_result("S478", AOS_testrun_info)
    write_result("S477", AOS_testrun_info)

@pytest.mark.order(8)
@pytest.mark.default_step
@pytest.mark.stg_widget
def test_check_testresult_AOS(main_homepage, write_result):
    page = main_homepage
    App_CheckList_478_AOS= get_testrun_status_AOS(page, testrun_status, testrun_result_message_AOS)
    write_result("P478", App_CheckList_478_AOS)
    write_result("P477", "Passed")

@pytest.mark.order(9)
@pytest.mark.default_step
@pytest.mark.stg_widget
def test_back_testrun_list_AOS(main_homepage):
    page = main_homepage
    back_to_testrun_list(page, return_to_testrun, reset_filter)
  
@pytest.mark.order(10)
@pytest.mark.default_step
@pytest.mark.stg_widget
def test_checkresult_IOS(main_homepage):
    page = main_homepage
    page.click(btn_test_filter)

    target_title_IOS= page.locator(title_filter_section).get_by_text("Filter")
    assert target_title_IOS.is_visible(), f"❌ {btn_test_filter} 선택 실패"

    container_filter_IOS = page.locator(filter_os_section) 
    IOS_checkbox = container_filter_IOS.locator("img[data-testid='checkBox']").nth(1)

    try:
        IOS_checkbox.scroll_into_view_if_needed()
        IOS_checkbox.wait_for(state="visible", timeout=5000)
        IOS_checkbox.click(force=True)

        IOS_apply_button = page.get_by_role("button", name="Apply")
        IOS_apply_button.wait_for(state="visible", timeout=5000)
        IOS_apply_button.scroll_into_view_if_needed()
        IOS_apply_button.click()

        page.wait_for_timeout(5000)

        IOS_target_element = page.locator(target_filterbox)
        IOS_target_element.wait_for(state="visible", timeout=5000)
        assert IOS_target_element.is_visible(), "❌ IOS 필터 적용 실패"
    except Exception as e:
        assert False, f"❌ test device OS 필터 적용 실패: {e}"

@pytest.mark.order(11)
@pytest.mark.default_step
@pytest.mark.stg_widget
def test_testrun_info_IOS(main_homepage,write_result):
    page = main_homepage
    page.click(first_testrun_id)
    IOS_testrun_info = get_testrun_info(page, testrun_id_section)
    write_result("T479", IOS_testrun_info)
    write_result("T477", IOS_testrun_info)

@pytest.mark.order(12)
@pytest.mark.default_step
@pytest.mark.stg_widget
def test_check_testresult_IOS(main_homepage, write_result):
    page = main_homepage
    App_CheckList_479_iOS = get_testrun_status_IOS(page, testrun_status, testrun_result_message_IOS)
    write_result("R479", App_CheckList_479_iOS)
    write_result("R477", "Passed")

@pytest.mark.order(13)
@pytest.mark.default_step
@pytest.mark.stg_widget
def test_back_testrun_list_IOS(main_homepage):
    page = main_homepage
    back_to_testrun_list(page, return_to_testrun, reset_filter)

# -------------------------------
# 자동화 테스트 결과 비교
# -------------------------------

# 비교대상 (1번시트 row, 2번시트 row)
row_pairs = [
    (476, 448),
    (477, 449),
    (478, 450),
    (479, 451),
]

# 열 매핑 및 비교 열
col1 = "E"  # 1번시트 비교 열
col2 = "B"  # 2번시트 비교 열
copy_map = {
    "P": "R",
    "Q": "S",
    "R": "T",
}

@pytest.mark.default_step
@pytest.mark.prod_widget
@pytest.mark.stg_widget
@pytest.mark.order(14)
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


