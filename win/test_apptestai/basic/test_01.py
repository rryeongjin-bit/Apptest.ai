import pytest
import re
from element_total import *
from common_utils2 import *
from conftest2 import *

# myridi 영역
def test_001_login_enter_project(main_homepage):
    page = main_homepage
    login_and_select_project(page)

def test_002_check_enter_project(main_homepage):
    page = main_homepage
    page.click(prod_basic)

    target_project = page.locator(project_title).get_by_text("[Prod] 기본기능 확인")
    try:
        target_project.wait_for(state="visible", timeout=5000)
    except TimeoutError:
        assert False, f"❌ {prod_basic} 폴더 진입 실패"

    assert target_project.is_visible(), f"❌ {prod_basic} 폴더 진입 실패"

def test_003_checkresult(main_homepage):
    page = main_homepage
    targets = [
            (title_recent_result, "Recent Test Runs"),
        ]

    click_and_verify(page, btn_test_run, targets)
    select_rows(page)

def test_004_checkresult_AOS(main_homepage):
    page = main_homepage
    apply_filter_checkbox_AOS(page)

def test_005_testrun_info_AOS(main_homepage, aos_flag, sheet):
    page = main_homepage
    testrun_basic = page.locator(testrun_first).filter(
        has_text=re.compile(r"기본기능 확인", re.IGNORECASE)
    ).first

    try:
        testrun_basic.wait_for(state="attached", timeout=5000)
        testrun_basic.scroll_into_view_if_needed()
        testrun_basic.wait_for(state="visible", timeout=5000)
        testrun_basic.click()

        AOS_testrun_info = get_testrun_info(page, testrun_id_section)
        write_result_by_key(sheet,"App_CheckList_003", AOS_testrun_info, column="O")

    except Exception as e:
        write_result_by_key(sheet, "App_CheckList_003", "No Info", column="O")
        aos_flag["run"] = False
        pytest.skip("⚠️ AOS 테스트 결과 없음 - 테스트 정보 확인 skip")

def test_006_App_CheckList_003(main_homepage, aos_flag, sheet):
    page = main_homepage

    # 1️⃣ 화면 열기
    page.locator(btn_screen).filter(has_text="Screen").click()
    page.wait_for_timeout(30000)

    # 2️⃣ 공통 selector
    content_box_selector = container_scroll
    step_status_selectors = [
        step_status_warning,
        step_status_assert,
        step_status_passed,
    ]
    step_name_selector = step_name
    end_test_selector = end_test

    EXCEL_KEY = "App_CheckList_003"

    target_text = re.compile(r"\[결과\]\s*App_CheckList_003\s*리디캐시\s*상세화면$")

    # 3️⃣ step status 찾기
    matched_status, found_text = scroll_and_find_step_status(
        page=page,
        content_box_selector=content_box_selector,
        step_status_selectors=step_status_selectors,
        step_name_selector=step_name_selector,
        end_test_selector=end_test_selector,
        target_text=target_text,
        debug=True,
    )

    # 4️⃣ 검증
    if not matched_status:
        write_result_by_key(sheet, EXCEL_KEY, "N/T", column="L")
        pytest.fail("step을 찾지 못함")

    assert target_text.search(found_text) is not None

    # 5️⃣ status 판별
    status_text = matched_status.inner_text().strip().lower()

    if "passed" in status_text or "assert" in status_text:
        result = "passed"
    elif "warning" in status_text:
        result = "warning"
    elif "failed" in status_text:
        result = "failed"
    else:
        result = "N/T"

    # 6️⃣ AOS flag 처리
    if not aos_flag["run"]:
        result = "N/T"

    # 7️⃣ 엑셀 기록
    write_result_by_key(sheet, EXCEL_KEY, result, column="L")


# def test_006_scroll_and_find(main_homepage):
#     page = main_homepage

#     # 화면 열기
#     page.locator(btn_screen).filter(has_text="Screen").click()
#     page.wait_for_timeout(1000)

#     # 실제 스크롤 영역
#     content_box_selector = container_scroll

#     # ✅ step status (warning / assert / passed)
#     step_status_selectors = [
#         step_status_warning,
#         step_status_assert,
#         step_status_passed,
#     ]

#     # ✅ step 이름이 들어있는 요소
#     step_name_selector = step_name

#     # ✅ 리스트 최하단 판단용 요소
#     end_test_selector = end_test

#     target_text = "[결과] App_CheckList_029"

#     # 🔍 공통함수 호출
#     matched_status, found_text = scroll_and_find_step_status(
#         page=page,
#         content_box_selector=content_box_selector,
#         step_status_selectors=step_status_selectors,
#         step_name_selector=step_name_selector,
#         end_test_selector=end_test_selector,
#         target_text=target_text,
#         debug=True,
#     )

#     # ✅ 결과 처리
#     if matched_status:
#         print("🎯 최종 발견:", found_text)

#         # (선택) 해당 status 클래스 출력
#         class_name = matched_status.get_attribute("class")
#         print("📌 status class:", class_name)

#         # (선택) 화면에 확실히 보이게
#         matched_status.scroll_into_view_if_needed()

#         assert target_text in found_text
#     else:
#         print("⚠️ target_text 미발견")
#         assert False, f"'{target_text}' step을 찾지 못함"

