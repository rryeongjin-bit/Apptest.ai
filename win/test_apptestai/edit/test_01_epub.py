import pytest
import re
from element_total import *
from common_utils import *
from conftest import *

TCID1 = "상단_책갈피"

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

def test_006_scroll_and_find(main_homepage):
    page = main_homepage

    # 화면 열기
    page.locator(btn_screen).filter(has_text="Screen").click()
    page.wait_for_timeout(1000)

    # 실제 스크롤 영역
    content_box_selector = container_scroll

    # ✅ step status (warning / assert / passed)
    step_status_selectors = [
        step_status_warning,
        step_status_assert,
        step_status_passed,
    ]

    # ✅ step 이름이 들어있는 요소
    step_name_selector = step_name

    # ✅ 리스트 최하단 판단용 요소
    end_test_selector = end_test

    target_text = TCID1

    # 🔍 공통함수 호출
    matched_status, found_text = scroll_and_find_step_status(
        page=page,
        content_box_selector=content_box_selector,
        step_status_selectors=step_status_selectors,
        step_name_selector=step_name_selector,
        end_test_selector=end_test_selector,
        target_text=target_text,
        debug=True,
    )

    # ✅ 결과 처리
    if matched_status:
        print("🎯 최종 발견:", found_text)

        # (선택) 해당 status 클래스 출력
        class_name = matched_status.get_attribute("class")
        print("📌 status class:", class_name)

        # (선택) 화면에 확실히 보이게
        matched_status.scroll_into_view_if_needed()

        assert target_text in found_text
    else:
        print("⚠️ target_text 미발견")
        assert False, f"'{target_text}' step을 찾지 못함"

# def test_007_back_testrun_list_AOS_epub1(main_homepage, aos_flag):
#     back_and_or_reset_AOS(main_homepage, aos_flag.get("run", False))
