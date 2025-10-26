import pytest
from element_total import *

@pytest.mark.order(1)
def test_login(main_homepage):
    page = main_homepage
    page.goto("https://app.apptest.ai")
    assert "Dashboard" in page.inner_text("body")

@pytest.mark.order(2)
def test_changeaccount(main_homepage):
    page = main_homepage
    page.click(btn_changeaccount)
    page.click(qa_account)

    target_account = page.locator(account_section).get_by_text("RIDI 시나리오 수정")
    assert target_account.is_visible(), "❌ QA part 계정 변환되지않음"

