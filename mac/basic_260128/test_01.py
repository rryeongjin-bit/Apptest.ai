import pytest
import re
from element_total import *
from common_utils2 import *
from conftest2 import *

TCID_001 = "App_CheckList_001"
TCID_002 = "App_CheckList_002"
TCID_003 = "App_CheckList_003"
TCID_004 = "App_CheckList_004"
TCID_005 = "App_CheckList_005"
TCID_006 = "App_CheckList_006"

def test_001_login_enter_project(page):
    login_and_select_project(page)

def test_002_check_enter_project(page):
    page.click(prod_basic)

    target_project = page.locator(project_title).get_by_text("[Prod] 기본기능 확인")
    try:
        target_project.wait_for(state="visible", timeout=5000)
    except TimeoutError:
        assert False, f"❌ {prod_basic} 폴더 진입 실패"

    assert target_project.is_visible(), f"❌ {prod_basic} 폴더 진입 실패"

def test_003_checkresult(page):
    targets = [
            (title_recent_result, "Recent Test Runs"),
        ]

    click_and_verify(page, btn_test_run, targets)
    select_rows(page)

def test_004_checkresult_AOS(page):
    apply_filter_checkbox_AOS(page)

def test_005(page):
    testrun_basic = page.locator(testrun_first).filter(
        has_text=re.compile(r"기본기능 확인", re.IGNORECASE)
    ).first

    testrun_basic.wait_for(state="attached", timeout=5000)
    testrun_basic.scroll_into_view_if_needed()
    testrun_basic.wait_for(state="visible", timeout=5000)
    testrun_basic.click()

# 앱 실행
def test_006(page, aos_flag, sheet):
    try:
        testrun_info = get_testrun_info(page, testrun_id_section)
        write_result_by_key(sheet,TCID_001, testrun_info, column="O")
    
    except Exception as e:
        write_result_by_key(sheet, TCID_001, "No Info", column="O")
        aos_flag["run"] = False
        pytest.skip("⚠️ AOS 테스트 결과 없음 - 테스트 정보 확인 skip")

def test_007(page, sheet, step_selectors):
    open_screen_tab(page)

    run_step_and_record_result(
        page=page,
        sheet=sheet,
        tcid=TCID_001,
        target_text=re.compile(r"^리디앱 실행$"),
        selectors=step_selectors,
    )

# 로그인
def test_008(page, aos_flag, sheet):
    try:
        testrun_info = get_testrun_info(page, testrun_id_section)
        write_result_by_key(sheet,TCID_002, testrun_info, column="O")
    
    except Exception as e:
        write_result_by_key(sheet, TCID_002, "No Info", column="O")
        aos_flag["run"] = False
        pytest.skip("⚠️ AOS 테스트 결과 없음 - 테스트 정보 확인 skip")

def test_009(page, sheet, step_selectors):
    run_step_and_record_result(
        page=page,
        sheet=sheet,
        tcid=TCID_002,
        target_text=re.compile(r"^로그인$"),
        selectors=step_selectors,
    )

#마이리디


def test_007(page, sheet):
# 1️⃣ 화면 열기
    page.locator(btn_screen).filter(has_text="Screen").click()
    page.wait_for_timeout(10000)

    # 2️⃣ 공통 selector
    content_box_selector = container_scroll
    step_status_selectors = [
        step_status_warning,
        step_status_assert,
        step_status_passed,
    ]
    step_name_selector = step_name
    end_test_selector = end_test
    target_text = re.compile(r"^리디앱 실행$")

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
        write_result_by_key(sheet, TCID_001, "N/T", column="L")
        pytest.fail("step을 찾지 못함")

    assert target_text.search(found_text) is not None

    # 5️⃣ status 판별
    cls = matched_status.get_attribute("class") or ""
    cls = cls.lower()

    if "passed" in cls or "assert" in cls:
        result = "passed"
    elif "warning" in cls:
        result = "warning"
    elif "failed" in cls:
        result = "failed"
    else:
        result = "N/T"

    # 7️⃣ 엑셀 기록
    write_result_by_key(sheet, TCID_001, result, column="L")
    
# 로그인
def test_008(page, aos_flag, sheet):
    try:
        testrun_info = get_testrun_info(page, testrun_id_section)
        write_result_by_key(sheet,TCID_002, testrun_info, column="O")
    
    except Exception as e:
        write_result_by_key(sheet, TCID_002, "No Info", column="O")
        aos_flag["run"] = False
        pytest.skip("⚠️ AOS 테스트 결과 없음 - 테스트 정보 확인 skip")

def test_009(page, sheet):
    content_box_selector = container_scroll
    step_status_selectors = [
        step_status_warning,
        step_status_assert,
        step_status_passed,
    ]
    step_name_selector = step_name
    end_test_selector = end_test
    target_text = re.compile(r"^로그인$")

    matched_status, found_text = scroll_and_find_step_status(
        page=page,
        content_box_selector=content_box_selector,
        step_status_selectors=step_status_selectors,
        step_name_selector=step_name_selector,
        end_test_selector=end_test_selector,
        target_text=target_text,
        debug=True,
    )

    if not matched_status:
        write_result_by_key(sheet, TCID_002, "N/T", column="L")
        pytest.fail("step을 찾지 못함")

    assert target_text.search(found_text) is not None

    cls = matched_status.get_attribute("class") or ""
    cls = cls.lower()

    if "passed" in cls or "assert" in cls:
        result = "passed"
    elif "warning" in cls:
        result = "warning"
    elif "failed" in cls:
        result = "failed"
    else:
        result = "N/T"

    write_result_by_key(sheet, TCID_002, result, column="L")

# myridi 영역