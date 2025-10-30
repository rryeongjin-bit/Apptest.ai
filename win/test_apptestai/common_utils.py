
import os
import pytest
from element_total import *
from playwright.sync_api import Page
from playwright.sync_api import sync_playwright
from playwright.sync_api import TimeoutError

def scroll_until_element_found(page, target_text, step=500, max_scrolls=5):
    """
    지정된 셀렉터 요소가 나타날 때까지 스크롤 다운.
    
    :param page: playwright의 page 객체
    :param selector: 찾을 셀렉터 (예: 'div.item:nth-child(1)')
    :param step: 한 번에 스크롤할 픽셀 높이
    :param max_scrolls: 최대 스크롤 시도 횟수 (무한루프 방지)
    :return: 요소가 발견되면 True, 아니면 False
    """
    for i in range(max_scrolls):
        try:
            # 요소가 보이면 바로 리턴
            if page.locator(target_text).is_visible():
                print(f"✅ target_element 발견! (시도 횟수: {i+1})")
                return True
        except PlaywrightTimeoutError:
            pass

        # JS 실행으로 스크롤 다운
        page.evaluate(f"window.scrollBy(0, {step})")
        page.wait_for_timeout(500)  # 스크롤 후 약간의 대기 (0.5초)

    print("❌ target_element 발견 실패")
    return False

# 테스트 정보 출력
def get_testrun_info(page: Page, testrun_id_section: str) -> str:
    target_testrun_id = page.locator(testrun_id_section)
    testrun_info = target_testrun_id.inner_text().strip()

    if not testrun_info:
        raise ValueError("❌ testrun_info 확인 실패")
    print(f"🔎 testrun_info: {testrun_info}")
    return testrun_info

# 테스트 결과 출력_AOS
def get_testrun_status_AOS(page: Page, testrun_status: str, testrun_result_message: str):
    target_status_AOS = page.locator(testrun_status)
    result_testrun_status_AOS = target_status_AOS.inner_text()
    
    if result_testrun_status_AOS in ["Warning", "Failed", "Passed"]:
        test_message_AOS = page.locator(f"{testrun_result_message_AOS} span")
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
def get_testrun_status_IOS(page: Page, testrun_status: str, testrun_result_message: str):
    target_status_IOS = page.locator(testrun_status)
    result_testrun_status_IOS = target_status_IOS.inner_text()
    
    if result_testrun_status_IOS in ["Warning", "Failed", "Passed"]:
        test_message_IOS = page.locator(f"{testrun_result_message_IOS} span")
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
