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

@pytest.mark.order(3)
def test_mobileapp(main_homepage):
    page = main_homepage
    page.click(folder_mobileapp)

    target_folder = page.locator(folder_title_section).get_by_text("Mobile App")
    assert target_folder.is_visible(), f"❌ {folder_mobileapp} 선택 실패"

@pytest.mark.order(4)
def test_project_widget(main_homepage):
    page = main_homepage
    page.click(project_widget)

    target_project = page.locator(project_title).get_by_text("위젯")
    assert target_project.is_visible(), f"❌ {project_widget} 선택 실패"
    
    