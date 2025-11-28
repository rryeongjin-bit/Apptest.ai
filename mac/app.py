import json
import logging
import threading
import subprocess
from flask import Flask, request, make_response
from slack_sdk import WebClient
from slack_sdk.signature import SignatureVerifier

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# 환경변수 또는 직접 입력
SLACK_BOT_TOKEN = {}
SLACK_SIGNING_SECRET = {}

client = WebClient(token=SLACK_BOT_TOKEN)
signature_verifier = SignatureVerifier(SLACK_SIGNING_SECRET)


def run_pytest(marker, test_dir, test_file, channel, client):
    """Pytest 실행을 쓰레드에서 수행 (실시간 로그 출력)"""
    cwd_path = "C:/Users/User/Desktop/automation/apptestAI/win"
    # 특정 파일 입력이 없으면 디렉토리 전체 실행
    path_to_test = f"test_apptestai/{test_dir}/{test_file}" if test_file else f"test_apptestai/{test_dir}"
    cmd = ["pytest", "-s", "-m", marker, path_to_test]

    logging.info(f"실행 명령어: {' '.join(cmd)}")

    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, cwd=cwd_path
    )

    # 실시간 로그 출력
    for line in proc.stdout:
        print(line, end="")  # VSCode 터미널에 출력
        logging.info(line.strip())

    proc.wait()
    logging.info("자동화 완료 ✅")

    # Slack으로 결과 전송 (주석 처리)
    # client.chat_postMessage(
    #     channel=channel,
    #     text=f"테스트 실행 완료!\n```{output}```"
    # )


@app.route("/run_autotest", methods=["POST"])
def slash_command():
    """Slash Command 호출 시 모달 띄우기"""
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
                    "label": {"type": "plain_text", "text": "테스트 파일명 (선택, 확장자 포함)"},
                    "element": {"type": "plain_text_input", "action_id": "test_file"}
                }
            ],
            "private_metadata": channel_id
        }
    )

    return make_response("", 200)


@app.route("/interact", methods=["POST"])
def interact():
    """Slack 모달 Submit 이벤트 수신"""
    if not signature_verifier.is_valid_request(request.get_data(), request.headers):
        return make_response("Invalid request", 403)

    payload = json.loads(request.form["payload"])
    if payload["type"] == "view_submission" and payload["view"]["callback_id"] == "pytest_modal":
        values = payload["view"]["state"]["values"]
        channel = payload["view"]["private_metadata"]

        marker = values["marker_input"]["marker"]["value"]
        test_dir = values["dir_input"]["test_dir"]["value"]
        test_file = values.get("file_input", {}).get("test_file", {}).get("value", None)

        logging.info(f"모달 제출: marker={marker}, test_dir={test_dir}, test_file={test_file}")

        # Pytest 실행을 별도 쓰레드에서 수행 (VSCode 터미널에서 실시간 출력)
        threading.Thread(target=run_pytest, args=(marker, test_dir, test_file, channel, client)).start()

        return make_response("", 200)

    return make_response("", 200)


if __name__ == "__main__":
    app.run(port=3000, host="0.0.0.0")