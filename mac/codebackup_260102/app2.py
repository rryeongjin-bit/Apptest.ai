import os
import json
import threading
import subprocess
import logging
from flask import Flask, request, make_response
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk.signature import SignatureVerifier

SLACK_BOT_TOKEN ={}
SLACK_SIGNING_SECRET = {}
TARGET_CHANNEL ={}

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
client = WebClient(token=SLACK_BOT_TOKEN)
signature_verifier = SignatureVerifier(SLACK_SIGNING_SECRET)


def run_pytest_and_send_output(top_dir, sub_dir, test_file=None, channel=None):
    cwd_path = os.path.dirname(os.path.abspath(__file__))

    if test_file and test_file.strip():
        test_path = os.path.join(cwd_path, top_dir, sub_dir, test_file.strip())
    else:
        test_path = os.path.join(cwd_path, top_dir, sub_dir)

    if not os.path.exists(test_path):
        logging.error(f"테스트 경로 존재하지 않음: {test_path}")
        return

    send_channel = TARGET_CHANNEL
    # try:
    #     start_message = (
    #         f"- 프로젝트: `{top_dir}`\n"
    #         f"- 실행경로: `{test_path}`\n"
    #     )
    #     client.chat_postMessage(channel=send_channel, text=start_message)
    #     logging.info("테스트 자동화 시작 알림 전송 성공")
    # except SlackApiError as e:
    #     logging.error(f"Slack 시작 메시지 전송 실패: {e.response['error']}")

    cmd = ["pytest", "-s", test_path]
    logging.info(f"Pytest 실행 커맨드: {' '.join(cmd)}")

    try:
        result = subprocess.run(
            cmd,
            cwd=cwd_path,
            text=True,
            capture_output=True,
        )

        output_text = result.stdout + "\n" + result.stderr
        remove_keywords = ["platform ", "rootdir:", "configfile:", "plugins:", "collected "]
        filtered_lines = [line for line in output_text.splitlines() if not any(key in line for key in remove_keywords)]
        output_text = "\n".join(filtered_lines)

        logging.info(f"Pytest returncode: {result.returncode}")
        logging.info(f"Filtered Pytest output:\n{output_text}")  

        MAX_SLACK_LEN = 500
        slack_output_text = output_text
        if len(slack_output_text) > MAX_SLACK_LEN:
            slack_output_text = slack_output_text[:MAX_SLACK_LEN] + "\n...[중략]"

        # try:
        #     client.chat_postMessage(
        #         channel=send_channel,
        #         text=f"```{slack_output_text}```"
        #     )
        #     logging.info(f"테스트 결과 전송 완료: {send_channel}")
        # except SlackApiError as e:
        #     logging.error(f"Slack 메시지 전송 실패: {e.response['error']}")

    except Exception as e:
        logging.error(f"Pytest 실행 실패: {e}")


@app.route("/interact", methods=["POST"])
def interact():
    if not signature_verifier.is_valid_request(request.get_data(), request.headers):
        return make_response("Invalid request", 403)

    payload = json.loads(request.form["payload"])
    ptype = payload.get("type")

    logging.info(f"Received payload:\n{json.dumps(payload, indent=2, ensure_ascii=False)}")

    if ptype == "message_action" and payload.get("callback_id") == "run_apptest_result":
        trigger_id = payload["trigger_id"]
        channel_id = payload.get("channel", {}).get("id", TARGET_CHANNEL)

        modal_view = {
            "type": "modal",
            "callback_id": "run_apptest_result_modal",
            "title": {"type": "plain_text", "text": "Pytest 실행기"},
            "submit": {"type": "plain_text", "text": "실행"},
            "blocks": [
                {
                    "type": "input",
                    "block_id": "top_dir_input",
                    "label": {"type": "plain_text", "text": "최상위 폴더 (prod/stg)"},
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "top_dir",
                    },
                },
                {
                    "type": "input",
                    "block_id": "sub_dir_input",
                    "label": {"type": "plain_text", "text": "하위 프로젝트 폴더"},
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "sub_dir",
                    },
                },
                {
                    "type": "input",
                    "block_id": "file_input",
                    "optional": True,
                    "label": {"type": "plain_text", "text": "테스트 파일명"},
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "test_file",
                    },
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

    if ptype == "view_submission" and payload.get("view", {}).get("callback_id") == "run_apptest_result_modal":
        values = payload["view"]["state"]["values"]
        channel = payload["view"]["private_metadata"]

        top_dir = values["top_dir_input"]["top_dir"]["value"]
        sub_dir = values["sub_dir_input"]["sub_dir"]["value"]
        test_file = values.get("file_input", {}).get("test_file", {}).get("value")

        threading.Thread(
            target=run_pytest_and_send_output,
            args=(top_dir, sub_dir, test_file, channel),
        ).start()

        return make_response("", 200)

    return make_response("", 200)


if __name__ == "__main__":
    app.run(port=3000, host="0.0.0.0")