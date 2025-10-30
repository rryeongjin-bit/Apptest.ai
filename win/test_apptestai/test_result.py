import pytest
from element_total import *
from common_utils import *

@pytest.mark.order(1)
@pytest.mark.default_step
def test_login(main_homepage):
    page = main_homepage
    page.goto("https://app.apptest.ai")
    assert "Dashboard" in page.inner_text("body")

@pytest.mark.order(2)
@pytest.mark.default_step
def test_changeaccount(main_homepage):
    page = main_homepage
    page.click(btn_changeaccount)
    page.click(qa_account)
    
    target_account = page.locator(account_section).get_by_text("RIDI 시나리오 수정")
    assert target_account.is_visible(), "❌ QA part 계정 변환되지않음"

@pytest.mark.order(3)
@pytest.mark.default_step
def test_mobileapp(main_homepage):
    page = main_homepage
    page.click(folder_mobileapp)

    target_folder = page.locator(folder_title_section).get_by_text("Mobile App")
    assert target_folder.is_visible(), f"❌ {folder_mobileapp} 선택 실패"

# -------------------------------
# 위젯 프로젝트
# -------------------------------

@pytest.mark.order(4)
@pytest.mark.project_widget
def test_project_widget(main_homepage):
    page = main_homepage
    page.click(project_widget)

    target_project = page.locator(project_title).get_by_text("위젯")
    try:
        target_project.wait_for(state="visible", timeout=5000)
    except TimeoutError:
        assert False, f"❌ {project_widget} 폴더 진입 실패"

    assert target_project.is_visible(), f"❌ {project_widget} 폴더 진입 실패"
    
@pytest.mark.order(5)
@pytest.mark.project_widget
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
@pytest.mark.project_widget
def test_lastresult(main_homepage):
    page = main_homepage
    page.click(first_testrun_id)

    target_status = page.locator(testrun_status)
    result_testrun_status = target_status.inner_text()
    print(f"자동화테스트 결과 : {result_testrun_status}")
    assert result_testrun_status.strip() != "", "❌testrun_status 확인실패"

@pytest.mark.order(7)
@pytest.mark.project_widget
def test_checkscreen_detail(main_homepage):
    page = main_homepage
    page.click(btn_test_screen)

    target_testrun_id = page.locator(testrun_id_section)
    testrun_info = target_testrun_id.inner_text()
    print(f"🔎testrun_info : {testrun_info}")
    assert testrun_info.strip() != "", "❌ testrun_info 확인 실패"

    target_teststeps = [ (test_step_name, "App_CheckList_478")]
    for sel, target_text in target_teststeps:
        found = scroll_until_element_found(page, sel)
        assert found, f"⚠️ teststep_id 확인 필요 : {sel}"

    # target_test_step_result = 

