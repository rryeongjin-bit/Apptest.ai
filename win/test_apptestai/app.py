import os
import json
import threading
import subprocess
import logging
from flask import Flask, request, make_response
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk.signature import SignatureVerifier

SLACK_BOT_TOKEN = {}
SLACK_SIGNING_SECRET = {}
TARGET_CHANNEL = {}

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
client = WebClient(token=SLACK_BOT_TOKEN)
signature_verifier = SignatureVerifier(SLACK_SIGNING_SECRET)

# -----------------------
# Pytest 실행 후 Slack 전송
# -----------------------
def run_pytest_and_send_output(marker, test_dir, test_file, channel=None):
    cwd_path = os.path.dirname(__file__)
    cmd = ["pytest", "-s"]

    if marker:
        cmd += ["-m", marker]
    if test_file and test_file.strip():
        test_path = os.path.join(test_dir, test_file.strip())
        cmd.append(test_path)
    else:
        cmd.append(test_dir)

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        cwd=cwd_path,
    )

    output_lines = []
    for line in iter(proc.stdout.readline, ""):
        if line:
            output_lines.append(line.rstrip())
    proc.wait()

    output_text = "\n".join(output_lines)
    if len(output_text) > 3000:
        output_text = output_text[:3000] + "\n...[중략]"

    send_channel = channel or TARGET_CHANNEL
    try:
        client.chat_postMessage(channel=send_channel, text=f"```{output_text}```")
        logging.info(f"테스트 결과 전송 완료: {send_channel}")
    except SlackApiError as e:
        logging.error(f"Slack 메시지 전송 실패: {e.response['error']}")

# -----------------------
# Message Shortcut 처리
# -----------------------
@app.route("/interact", methods=["POST"])
def interact():
    if not signature_verifier.is_valid_request(request.get_data(), request.headers):
        return make_response("Invalid request", 403)

    payload = json.loads(request.form["payload"])
    ptype = payload.get("type")
    logging.info(f"Received payload:\n{json.dumps(payload, indent=2, ensure_ascii=False)}")

    # 1️⃣ 메시지 숏컷 클릭 시 모달 띄우기
    if ptype == "message_action" and payload.get("callback_id") == "run_apptest_result":
        trigger_id = payload["trigger_id"]
        channel_id = payload.get("channel", {}).get("id", TARGET_CHANNEL)

        modal_view = {
            "type": "modal",
            "callback_id": "run_apptest_result_modal",  # modal 제출용 callback
            "title": {"type": "plain_text", "text": "Pytest 실행기"},
            "submit": {"type": "plain_text", "text": "실행"},
            "blocks": [
                {
                    "type": "input",
                    "block_id": "marker_input",
                    "label": {"type": "plain_text", "text": "Marker"},
                    "element": {"type": "plain_text_input", "action_id": "marker"},
                },
                {
                    "type": "input",
                    "block_id": "dir_input",
                    "label": {"type": "plain_text", "text": "테스트 폴더명"},
                    "element": {"type": "plain_text_input", "action_id": "test_dir"},
                },
                {
                    "type": "input",
                    "block_id": "file_input",
                    "optional": True,
                    "label": {"type": "plain_text", "text": "테스트 파일명"},
                    "element": {"type": "plain_text_input", "action_id": "test_file"},
                },
            ],
            "private_metadata": channel_id,
        }

        try:
            response = client.views_open(trigger_id=trigger_id, view=modal_view)
            logging.info(f"views_open 성공: {response}")
        except SlackApiError as e:
            logging.error(f"views_open 실패: {e.response['error']}")

        return make_response("", 200)

    # 2️⃣ 모달 제출 처리
    if ptype == "view_submission" and payload.get("view", {}).get("callback_id") == "run_apptest_result_modal":
        values = payload["view"]["state"]["values"]
        channel = payload["view"]["private_metadata"]

        marker = values["marker_input"]["marker"]["value"]
        test_dir = values["dir_input"]["test_dir"]["value"]
        test_file = values.get("file_input", {}).get("test_file", {}).get("value")

        threading.Thread(
            target=run_pytest_and_send_output,
            args=(marker, test_dir, test_file, channel),
        ).start()

        return make_response("", 200)

    return make_response("", 200)

# -----------------------
# Flask 서버 실행
# -----------------------
if __name__ == "__main__":
    app.run(port=3000, host="0.0.0.0")