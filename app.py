from flask import Flask, request, jsonify
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

TODOIST_API_TOKEN = os.getenv("TODOIST_API_TOKEN")
VERIFICATION_TOKEN = os.getenv("TODOIST_VERIFICATION_TOKEN")

task_counter = 1

@app.route("/webhook", methods=["POST"])
def webhook():
    global task_counter
    # Проверка токена
    if request.headers.get("Authorization") != VERIFICATION_TOKEN:
        return "Unauthorized", 401

    data = request.json
    if data.get("event_name") == "item:added":
        task_id = data["event_data"]["id"]
        content = data["event_data"]["content"]

        # Добавление номера к задаче
        updated_content = f"{task_counter} {content}"
        task_counter += 1

        url = f"https://api.todoist.com/rest/v2/tasks/{task_id}"
        headers = {
            "Authorization": f"Bearer {TODOIST_API_TOKEN}",
            "Content-Type": "application/json"
        }
        payload = {"content": updated_content}
        requests.post(url, json=payload, headers=headers)

    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
