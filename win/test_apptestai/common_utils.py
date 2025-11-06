
import os
import pytest
from element_total import *
# from element_copy import *
from playwright.sync_api import Page
from playwright.sync_api import sync_playwright
from playwright.sync_api import TimeoutError

# 테로 로그인/계정변경 & 프로젝트 폴더 진입
def login_and_select_project(page, target_account_name="QA part", folder_name="Mobile App"):
    try:
        page.goto("https://app.apptest.ai")
        if "Dashboard" not in page.inner_text("body"):
            raise RuntimeError("❌ 로그인 실패")

        page.click(btn_changeaccount)
        page.click(qa_account)
        target_account = page.locator(account_section).get_by_text(target_account_name)
        if not target_account.is_visible():
            raise RuntimeError(f"❌ {target_account_name} 계정 변경 실패")

        page.click(folder_mobileapp)
        target_folder = page.locator(folder_title_section).get_by_text(folder_name)
        if not target_folder.is_visible():
            raise RuntimeError(f"❌ {folder_name} 프로젝트 폴더 선택 실패")

    except Exception as e:
        pytest.fail(f"로그인 & 프로젝트 폴더 선택 실패: {e}")

# 테스트 결과 목록 600개 보기
def select_rows(page):
    page.wait_for_selector("#rows")
    page.select_option("#rows", "600")
    
    page.wait_for_timeout(5000)

    selected_value = page.eval_on_selector("#rows", "el => el.value")
    assert selected_value == "600", f"테스트 결과 목록 600개 보기 실패 — rows : {selected_value}"
    print("✅ 테스트 결과 목록 600개 정렬 완료")
        
# 스크롤
def scroll_until_element_found(page: Page, selector: str, max_attempts: int = 10, wait_time: int = 500) -> bool:
    element = page.locator(selector)

    for _ in range(max_attempts):
        if element.count() > 0 and element.is_visible():
            return True
        element.scroll_into_view_if_needed()
        page.wait_for_timeout(wait_time)

    return False

# 요소 선택 
def click_and_verify(page: Page, button_selector: str, targets: list[tuple[str, str]]):
    page.click(button_selector)

    for sel, expected_text in targets:
        found = scroll_until_element_found(page, sel)
        assert found, f"❌ 요소를 찾지 못했습니다: {sel}"

        element = page.locator(sel)
        if expected_text:
            text_found = expected_text in element.inner_text()
            assert text_found, f"❌ '{expected_text}' 발견 실패: {sel}"

# test run_AOS 필터적용
def apply_filter_checkbox_AOS(page: Page):
    page.click(btn_test_filter)

    filter_container = page.locator(filter_os_section)
    checkbox = filter_container.locator("img[data-testid='checkBox']").nth(0)

    checkbox.scroll_into_view_if_needed()
    checkbox.wait_for(state="visible", timeout=5000)
    checkbox.click(force=True)

    apply_button = page.get_by_role("button", name="Apply")
    apply_button.scroll_into_view_if_needed()
    apply_button.wait_for(state="visible", timeout=5000)
    apply_button.click()

    page.wait_for_timeout(5000)

    target_elem = page.locator(target_filterbox)
    target_elem.wait_for(state="visible", timeout=5000)
    assert target_elem.is_visible(), "❌ Android 필터 적용 실패"

# test run_IOS 필터 적용
def apply_filter_checkbox_iOS(page: Page):
    page.click(btn_test_filter)

    filter_container = page.locator(filter_os_section)
    checkbox = filter_container.locator("img[data-testid='checkBox']").nth(1)

    checkbox.scroll_into_view_if_needed()
    checkbox.wait_for(state="visible", timeout=5000)
    checkbox.click(force=True)

    apply_button = page.get_by_role("button", name="Apply")
    apply_button.scroll_into_view_if_needed()
    apply_button.wait_for(state="visible", timeout=5000)
    apply_button.click()

    page.wait_for_timeout(5000)

    target_elem = page.locator(target_filterbox)
    target_elem.wait_for(state="visible", timeout=5000)
    assert target_elem.is_visible(), "❌ iOS 필터 적용 실패"

def back_and_or_reset_AOS(page: Page, run_flag: bool):
    try:
        if run_flag:
            # test run 목록 복귀
            back_button = page.locator(return_to_testrun)
            back_button.wait_for(state="visible", timeout=5000)
            back_button.click()

        #테스트 기기 OS 필터 초기화
        reset_button = page.locator(reset_filter)
        reset_button.wait_for(state="visible", timeout=5000)
        reset_button.scroll_into_view_if_needed()
        reset_button.click()
        page.wait_for_timeout(5000)

    except Exception as e:
        raise RuntimeError(f"⚠️ AOS test run 목록 복귀/필터 초기화 실패: {e}")

# test run 목록 복귀
def back_and_or_reset_IOS(page: Page, run_flag: bool):
    try:
        if run_flag:
            back_button = page.locator(return_to_testrun)
            back_button.wait_for(state="visible", timeout=5000)
            back_button.click()

        #테스트 기기 OS 필터 초기화
        reset_button = page.locator(reset_filter)
        reset_button.wait_for(state="visible", timeout=5000)
        reset_button.scroll_into_view_if_needed()
        reset_button.click()
        page.wait_for_timeout(5000)

    except Exception as e:
        raise RuntimeError(f"⚠️ IOS test run 목록 복귀/필터 초기화 실패: {e}")

# 테스트 정보 출력
def get_testrun_info(page: Page, testrun_id_section: str) -> str:
    target_testrun_id = page.locator(testrun_id_section)
    testrun_info = target_testrun_id.inner_text().strip()

    if not testrun_info:
        raise ValueError("❌ testrun_info 확인 실패")
    print(f"🔎 testrun_info: {testrun_info}")
    return testrun_info

# 테스트 결과 출력_AOS
def get_testrun_status_AOS(page: Page, testrun_status: str):
    target_passmessage_AOS = testrun_passmessage_AOS
    target_warningmessage_AOS = testrun_warningmessage_AOS

    target_status_AOS = page.locator(testrun_status)
    result_testrun_status_AOS = target_status_AOS.inner_text().strip()
 
    # testrun status에 따른 결과메시지 확인
    if result_testrun_status_AOS == "Passed":
        message_selector = f"{target_passmessage_AOS} span"
    elif result_testrun_status_AOS in ["Warning", "Failed"]:
        message_selector = f"{target_warningmessage_AOS} span"
    else:
        print("⚠️ 테스트 실행 결과 메시지를 찾을 수 없습니다.")
        return result_testrun_status_AOS

    # 테스트 결과메시지 출력
    test_message_AOS = page.locator(message_selector)
    count = test_message_AOS.count()
    if count == 0:
        print("⚠️ 테스트 실행 결과 메시지를 찾을 수 없습니다.")
    else:
        for i in range(count):
            text = test_message_AOS.nth(i).inner_text().strip()
            if text:
                print(f"💡 테스트 결과 출력 : {text}")
            else:
                raise ValueError("⚠️ 테스트 실행 결과 메시지를 찾을 수 없습니다.")

    return result_testrun_status_AOS

# 테스트 결과 출력_IOS
def get_testrun_status_IOS(page: Page, testrun_status: str):
    target_passmessage_IOS = testrun_passmessage_IOS
    target_warningmessage_IOS = testrun_warningmessage_IOS

    target_status_IOS = page.locator(testrun_status)
    result_testrun_status_IOS = target_status_IOS.inner_text().strip()

    # testrun status에 따른 결과메시지 확인
    if result_testrun_status_IOS == "Passed":
        message_selector = f"{target_passmessage_IOS} span"
    elif result_testrun_status_IOS in ["Warning", "Failed"]:
        message_selector = f"{target_warningmessage_IOS} span"
    else:
        print("⚠️ 테스트 실행 결과 메시지를 찾을 수 없습니다.")
        return result_testrun_status_IOS

    # 테스트 결과메시지 출력
    test_message_IOS = page.locator(message_selector)
    count = test_message_IOS.count()
    if count == 0:
        print("⚠️ 테스트 실행 결과 메시지를 찾을 수 없습니다.")
    else:
        for i in range(count):
            text = test_message_IOS.nth(i).inner_text().strip()
            if text:
                print(f"💡 테스트 결과 출력 : {text}")
            else:
                raise ValueError("⚠️ 테스트 실행 결과 메시지를 찾을 수 없습니다.")

    return result_testrun_status_IOS
 
# test run 목록 복귀 & 필터초기화
def back_to_testrun_list(page: Page, return_to_testrun: str, reset_filter: str):
    try:
        back_button = page.locator(return_to_testrun)
        back_button.wait_for(state='visible', timeout=5000)
        back_button.click()

        reset_button = page.locator(reset_filter)
        reset_button.wait_for(state="visible", timeout=5000)
        reset_button.scroll_into_view_if_needed()
        reset_button.click()
        page.wait_for_timeout(5000)
    except Exception as e:
        raise RuntimeError(f"❌ testrun 목록 복귀 & os 필터 초기화 실패: {e}")
        
    
# google sheet update
def write_to_sheet(auto_test_sheet, cell: str, value: str):
    """
    sheet : gspread.models.Worksheet 객체
    cell : "C3" 처럼 문자열로 지정
    value : 기록할 값
    """
    auto_test_sheet.update(range_name = cell, values = [[value]])