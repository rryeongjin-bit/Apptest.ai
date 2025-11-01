import pytest
from element_total import *
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

