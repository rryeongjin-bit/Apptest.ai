import pytest
import re
from element_total import *
from common_utils import *
from conftest import *

TCID1 = "이름변경 노출대기"

def test_001_login_enter_project(main_homepage):
    page = main_homepage
    login_and_select_project(page)

def test_002_check_enter_project(main_homepage):
    page = main_homepage
    page.click(prod_usersfile)

    target_project = page.locator(project_title).get_by_text("[Prod] 사용자파일")
    try:
        target_project.wait_for(state="visible", timeout=5000)
    except TimeoutError:
        assert False, f"❌ {prod_usersfile} 폴더 진입 실패"

    assert target_project.is_visible(), f"❌ {prod_usersfile} 폴더 진입 실패"

def test_003_checkresult(main_homepage):
    page = main_homepage
    targets = [
            (title_recent_result, "Recent Test Runs"),
        ]

    click_and_verify(page, btn_test_run, targets)
    select_rows(page)

"""
📍[사용자파일] epub_상단 컨트롤러/본문
"""
def test_004_checkresult_AOS(main_homepage):
    page = main_homepage
    apply_filter_checkbox_AOS(page)

def test_005_testrun_info_AOS_epub1(main_homepage, aos_flag, sheet):
    page = main_homepage
    AOS_testrun_usersfile_epub = page.locator(testrun_first).filter(
        has_text=re.compile(r"Epub_상단\s*컨트롤러", re.IGNORECASE)
    ).first

    try:
        AOS_testrun_usersfile_epub.wait_for(state="attached", timeout=5000)
        AOS_testrun_usersfile_epub.scroll_into_view_if_needed()
        AOS_testrun_usersfile_epub.wait_for(state="visible", timeout=5000)
        AOS_testrun_usersfile_epub.click()

        AOS_testrun_info = get_testrun_info(page, testrun_id_section)
        write_result_by_key(sheet, TCID1, AOS_testrun_info, column="S")

    except Exception as e:
        write_result_by_key(sheet, TCID1, "No Info", column="S")
        aos_flag["run"] = False
        pytest.skip("⚠️ AOS 테스트 결과 없음 - 테스트 정보 확인 skip")

def test_006_enter_screenshot(main_homepage):
    page = main_homepage

    page.locator(btn_screen).filter(has_text="Screen").click()
    page.wait_for_timeout(1000)

    matched_step, step_text = scroll_and_find_by_text(
        page=page,
        step_text_selector=".sc-hBLBPu.eilAuJ",
        target_text="이름변경 노출대기",
        debug=True
    )

    assert matched_step is not None, "❌ step 못 찾음"

    print("🎯 최종 발견:", step_text)

# def test_007_check_stepresult(main_homepage):
#     page = main_homepage

#     root = page.locator(screenshot)
#     target_step = root.locator("div", has_text=TCID1).first
#     target_step.scroll_into_view_if_needed()
#     target_step.wait_for(state="visible", timeout=60000)

#     # 하위 요소 중 assert / passed / warning 텍스트 가진 요소 선택
#     status_element = target_step.locator("div", has_text=re.compile(r"assert|passed|warning", re.IGNORECASE)).first()
#     status_element.wait_for(state="visible", timeout=60000)

#     # 실제 텍스트 가져오기
#     status_text = status_element.inner_text().strip().lower()
#     if status_text in ["assert", "passed"]:
#         print("pass")
#     elif status_text == "warning":
#         print("warning")
#     else:
#         print(f"알 수 없는 상태: {status_text}")


# def test_007_back_testrun_list_AOS_epub1(main_homepage, aos_flag):
#     back_and_or_reset_AOS(main_homepage, aos_flag.get("run", False))
