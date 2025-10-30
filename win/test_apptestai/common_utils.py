
import os
import pytest
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
