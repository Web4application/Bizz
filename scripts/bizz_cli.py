# scripts/bizz_cli.py

import argparse
import requests
import os

API_URL = os.getenv("API_URL", "http://localhost:8000")
API_KEY = os.getenv("API_KEY", "change-me")


def start_assistant():
    r = requests.get(f"{API_URL}/api/assistant/start")
    print("\n🤖", r.json().get("message", "No response"))


def send_chat(message):
    r = requests.post(
        f"{API_URL}/api/assistant/chat",
        json={"message": message},
        headers={"X-API-Key": API_KEY}
    )
    res = r.json()
    print("\n🧠 Response:", res.get("response"))
    print("\n📝 Memory:")
    for m in res.get("memory", []):
        print(f"- {m['role']}: {m['content']}")


def upload_file(filename):
    if not os.path.isfile(filename):
        print(f"File not found: {filename}")
        return
    with open(filename) as f:
        content = f.read()
    r = requests.post(
        f"{API_URL}/api/data/upload",
        json={"filename": os.path.basename(filename), "content": content},
        headers={"X-API-Key": API_KEY}
    )
    print("\n📁 Upload status:", r.json())


def main():
    parser = argparse.ArgumentParser(description="🛠️ Bizz CLI Toolkit")
    parser.add_argument("command", choices=["start", "chat", "upload"])
    parser.add_argument("--message", help="Message to send to assistant")
    parser.add_argument("--file", help="File to upload")

    args = parser.parse_args()

    if args.command == "start":
        start_assistant()
    elif args.command == "chat":
        if not args.message:
            print("--message is required for chat")
            return
        send_chat(args.message)
    elif args.command == "upload":
        if not args.file:
            print("--file is required for upload")
            return
        upload_file(args.file)


if __name__ == "__main__":
    main()
