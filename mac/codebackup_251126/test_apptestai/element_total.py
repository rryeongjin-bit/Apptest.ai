

# -------------------------------
# 로그인
# -------------------------------
account_section = "#root > header > div.sc-empnci.jgzAsH > div.sc-ePDLzJ.rrOtd > div > div > div"
btn_changeaccount = "#root > header > div.sc-empnci.jgzAsH > div.sc-ePDLzJ.rrOtd > div > img"
qa_account = "text=QA part"

# -------------------------------
# mobile app 폴더
# -------------------------------

folder_mobileapp = "#root > div.sc-bJBgwP.cukmPM > div.sc-fThUAz.izgTQR > div.sc-SrznA.jxvbfe > div.sc-czkgLR.MPcHN > div:nth-child(2)"
folder_title_section = "#content_box"
project_title = "#content_box > div > main > div > div.sc-bwGlVi.eVgfbA > div.sc-fnLEGM.bwlCBK > div.sc-kSRfVL.cNsZuF > div"

prod_launchapp = "#default-table > tbody > tr:nth-child(26) > td:nth-child(1) > div > div > div"
prod_tabbar = "#default-table > tbody > tr:nth-child(25) > td:nth-child(1) > div > div > div"
prod_genrehome = "#default-table > tbody > tr:nth-child(27) > td:nth-child(1) > div > div > div"
prod_contentshome = "#default-table > tbody > tr:nth-child(24) > td:nth-child(1) > div > div > div"
prod_preview = "#default-table > tbody > tr:nth-child(23) > td:nth-child(1) > div > div > div"
prod_viewer = "#default-table > tbody > tr:nth-child(28) > td:nth-child(1) > div > div > div"
prod_usersfile = "#default-table > tbody > tr:nth-child(22) > td:nth-child(1) > div > div > div"
prod_shortcut= "#default-table > tbody > tr:nth-child(20) > td:nth-child(1) > div > div > div"
prod_widget= "#default-table > tbody > tr:nth-child(21) > td:nth-child(1) > div > div > div"

# stg_launchapp : 
# stg_tabbar : 
# stg_genrehome : 
# stg_contentshome : 
# stg_contentshome_preview : 
# stg_viewer : 
# stg_usersfile : 
# stg_shorcut : 
# stg_widget :

btn_test_run = "#content_box > div > main > div > div.sc-gytJtb.fnWbHz > div > div.sc-hhmtaI.khyKCC > div.sc-ffWQKd.fAZKew"
title_recent_result = "#content_box > div > main > div > div.sc-gytJtb.fnWbHz > div > div.sc-SqAfZ.YQrKg > div.sc-fhzFiK.khqNog.title-name"

##필터버튼
btn_test_filter = "#content_box > div > main > div > div.sc-gytJtb.fnWbHz > div > div.sc-SqAfZ.YQrKg > div.sc-fPHcVk.CZLqG > div.sc-efFkwH.bjOcBl > div > div.sc-jRBLiq.krpUeL"

#필터박스 상단 타이틀명
title_filter_section = r"#content_box > div > main > div > div.sc-gytJtb.fnWbHz > div > div.sc-jCDwHD.eaSytZ > div.sc-gPdWHE.kDvSnv > div.sc-joYSUE.VkESz > div.fixed.top-0.left-0.h-screen.w-screen.inset-0.z-\[1200\].bg-\[\#292929\].bg-opacity-30.animate-\[fadeIn_0\.5s_ease-in-out\].text-modal-header-font-color > div > div.text-\[18px\].font-semibold.flex.justify-between.p-\[20px\].border-b.border-\[\#E4E4E3\].text-modal-header-font-color > span"

##필터박스 os섹션 영역
filter_os_section = "div.sc-gpaZuh.kByeUA"

##필터적용 이후 box
target_filterbox = "div.sc-eWzREE.kilehQ > div.sc-eXAmlR.dNgBgM:nth-child(2)"

testrun_first = "#default-table > tbody > tr > td:nth-child(3) > a div.sc-eBMEME.jQHsJX > div"
testrun_id_section = "#result-wrapper > div.sc-hiEoHn.jAfewu > div.sc-ixziMx.bFIyFm > div.sc-iWvALN.faYaIC"
testrun_status = "#result-wrapper > div.sc-ckIfTa.kZEXWM > div > div > div.sc-iAITSW.fnPOYm > div.sc-gRfXlQ.iKtyGj > div > div.sc-hIsoIq.jBlmaP > div > div > div > div:nth-child(9) > div.sc-dKBpOM.iqIaUm > div > div > span"
testrun_passmessage_AOS = "#result-wrapper > div.sc-ckIfTa.kZEXWM > div > div > div.sc-gMZIbH.jwEIEk"
testrun_warningmessage_AOS = "#result-wrapper > div.sc-ckIfTa.kZEXWM > div > div > div.sc-gMZIbH.fCmnFE"
testrun_failmessage_AOS = "#result-wrapper > div.sc-ckIfTa.kZEXWM > div > div > div.sc-gMZIbH.kCxeAt"

testrun_passmessage_IOS = "#result-wrapper > div.sc-ckIfTa.kZEXWM > div > div > div.sc-gMZIbH.jwEIEk"
testrun_warningmessage_IOS = "#result-wrapper > div.sc-ckIfTa.kZEXWM > div > div > div.sc-gMZIbH.fCmnFE"
testrun_failmessage_IOS = "#result-wrapper > div.sc-ckIfTa.kZEXWM > div > div > div.sc-gMZIbH.kCxeAt"

return_to_testrun = "#result-wrapper > div.sc-hiEoHn.jAfewu > div.sc-ixziMx.bFIyFm > div.sc-bXxnNr.ciVfYv > div.sc-fDpJdc.bHCtrn"
reset_filter = "#content_box > div > main > div > div.sc-gytJtb.fnWbHz > div > div.sc-SqAfZ.YQrKg > div.sc-fPHcVk.CZLqG > div.sc-efFkwH.bjOcBl > div > div.sc-eXAmlR.sc-jtskMo.dNgBgM.jwNRkK"
