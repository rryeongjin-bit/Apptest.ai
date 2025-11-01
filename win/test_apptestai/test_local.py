import pytest
from element_copy import *
from common_utils import *
from conftest import *

# -------------------------------
# 로그인&계정전환 + 프로젝트 폴더 진입
# -------------------------------
@pytest.mark.order(1)
@pytest.mark.prod_widget
@pytest.mark.stg_widget
def test_login_enter_project(main_homepage):
    page = main_homepage
    login_and_select_project(page)

# -------------------------------
# [Prod] 위젯 프로젝트
# -------------------------------

@pytest.mark.order(2)
@pytest.mark.prod_widget
def test_project_widget(main_homepage):
    page = main_homepage
    page.click(prod_widget)

    target_project = page.locator(project_title).get_by_text("[Prod] 숏컷")
    try:
        target_project.wait_for(state="visible", timeout=5000)
    except TimeoutError:
        assert False, f"❌ {prod_widget} 폴더 진입 실패"

    assert target_project.is_visible(), f"❌ {prod_widget} 폴더 진입 실패"
    
@pytest.mark.order(3)
@pytest.mark.prod_widget
def test_checkresult(main_homepage):
    page = main_homepage
    page.click(btn_test_run)

    targets = [
        (title_recent_result, "Recent Test Runs"),
    ]

    for sel, target_text in targets:
        found = scroll_until_element_found(page, sel)
        assert found, f"❌ 요소를 찾지 못했습니다: {sel}"

# -------------------------------
# ⌛ [Stage] 위젯 프로젝트 ⌛
# ------------------------------


# -------------------------------
# 자동화 테스트 결과 비교
# -------------------------------

# 비교 (1번시트 row, 2번시트 row)
row_pairs = [
    (476, 448),
    (477, 449),
    (478, 450),
    (479, 451),
]

# 열 매핑 및 비교 열
col1 = "E"  # 1번시트 비교 열
col2 = "B"  # 2번시트 비교 열
copy_map = {
    "P": "R",
    "Q": "S",
    "R": "T",
}

@pytest.mark.prod_widget
@pytest.mark.stg_widget
@pytest.mark.order(12)
@pytest.mark.parametrize("row1,row2", row_pairs)
def test_copy_cell_if_match(sheet, row1, row2):
    sheet1 = sheet
    sheet2 = sheet.spreadsheet.worksheet("App_Regression_Checklist v4.5")

    val1 = sheet1.acell(f"{col1}{row1}").value
    val2 = sheet2.acell(f"{col2}{row2}").value
    print(f"🔎 비교: 1번시트 {col1}{row1}={val1!r}, 2번시트 {col2}{row2}={val2!r}")

    if val1 == val2:
        print(f"✅ 값 일치 → 1번시트(O,P,Q{row1}) → 2번시트(J,K,L{row2}) 복사 시작")
        for c1, c2 in copy_map.items():
            value = sheet1.acell(f"{c1}{row1}").value
            sheet2.update_acell(f"{c2}{row2}", value)
            print(f"📋 복사: {c1}{row1} → {c2}{row2} ({value})")
    else:
        print(f"❌ {row1}행 ↔ {row2}행: 값 불일치 → 복사 안 함")

    print("🏁 결과 복사 완료!")


