import os
import json
import threading
import subprocess
import logging
from conftest import *
from flask import Flask, request, make_response
from slack_sdk import WebClient
from slack_sdk.signature import SignatureVerifier


# 환경변수 또는 직접 입력
SLACK_BOT_TOKEN = {}
SLACK_SIGNING_SECRET = {}

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

app = Flask(__name__)
client = WebClient(token=SLACK_BOT_TOKEN)
signature_verifier = SignatureVerifier(SLACK_SIGNING_SECRET)

def run_pytest(marker, test_dir, test_file=None):
    """Pytest를 subprocess로 실행하고 실시간 로그 출력"""
    import os, subprocess, logging

    # app.py가 있는 폴더 기준
    cwd_path = os.path.dirname(__file__)
    cmd = ["pytest", "-s"]

    if marker:
        cmd += ["-m", marker]

    if test_file:
        cmd.append(os.path.join(test_dir, test_file))
    else:
        cmd.append(test_dir)

    logging.info(f"Pytest 명령어: {' '.join(cmd)}")

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, cwd=cwd_path)

    for line in iter(proc.stdout.readline, ''):
        if line:
            logging.info(line.strip())

    proc.wait()
    logging.info("✅ 자동화 테스트 완료")

    # Slack 채널로 결과 전송 (필요 시 활성화)
    # client.chat_postMessage(channel=channel, text=f"테스트 완료!\n```{output}```")

# --- Slash Command: 모달 띄우기 ---
@app.route("/run_autotest", methods=["POST"])
def slash_command():
    trigger_id = request.form["trigger_id"]
    channel_id = request.form["channel_id"]

    client.views_open(
        trigger_id=trigger_id,
        view={
            "type": "modal",
            "callback_id": "pytest_modal",
            "title": {"type": "plain_text", "text": "Pytest 실행기"},
            "submit": {"type": "plain_text", "text": "실행"},
            "blocks": [
                {
                    "type": "input",
                    "block_id": "marker_input",
                    "label": {"type": "plain_text", "text": "Marker"},
                    "element": {"type": "plain_text_input", "action_id": "marker"}
                },
                {
                    "type": "input",
                    "block_id": "dir_input",
                    "label": {"type": "plain_text", "text": "테스트 디렉토리"},
                    "element": {"type": "plain_text_input", "action_id": "test_dir"}
                },
                {
                    "type": "input",
                    "block_id": "file_input",
                    "optional": True,
                    "label": {"type": "plain_text", "text": "테스트 파일명 (선택)"},
                    "element": {"type": "plain_text_input", "action_id": "test_file"}
                }
            ],
            "private_metadata": channel_id
        }
    )
    return make_response("", 200)

# --- Slack 모달 제출 이벤트 처리 ---
@app.route("/interact", methods=["POST"])
def interact():
    if not signature_verifier.is_valid_request(request.get_data(), request.headers):
        return make_response("Invalid request", 403)

    payload = json.loads(request.form["payload"])
    if payload["type"] != "view_submission":
        return make_response("", 200)

    values = payload["view"]["state"]["values"]
    channel = payload["view"]["private_metadata"]

    marker = values["marker_input"]["marker"]["value"]
    test_dir = values["dir_input"]["test_dir"]["value"]
    test_file = values.get("file_input", {}).get("test_file", {}).get("value")

    # Pytest를 쓰레드에서 실행 (실시간 로그 출력)
    threading.Thread(target=run_pytest, args=(marker, test_dir, test_file)).start()

    return make_response("", 200)

# --- Flask 앱 실행 ---
if __name__ == "__main__":
    app.run(port=3000, host="0.0.0.0")