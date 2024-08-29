import sqlite3
import requests
from datetime import datetime

# Load environment variables (replace this with your actual values or a .env file)
TELEGRAM_API_TOKEN = '7211412404:AAFTO0ud7ljRciRCCleffFZFKqdxKESzSGs'
CHAT_ID = '5550108562'
DATABASE = 'task_manager.db'  # Update this path based on your project structure

def get_due_tasks():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, due_date FROM task WHERE completed = 0")
    tasks = cursor.fetchall()
    conn.close()

    due_tasks = []
    current_date = datetime.now().date()  # Get today's date without time
    for task in tasks:
        try:
            # Parse datetime and extract date part
            due_date = datetime.strptime(task[2], '%Y-%m-%d %H:%M:%S.%f').date()
            if due_date <= current_date:
                due_tasks.append(task)
        except ValueError as e:
            print(f"Date parsing error: {e}")
    return due_tasks


def send_sms(task):
    message = f"Task Due: {task[1]} (Due on: {task[2]})"
    url = f"https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/sendMessage"
    data = {
        'chat_id': CHAT_ID,
        'text': message
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print(f"Notification sent for task: {task[1]}")
    else:
        print(f"Failed to send notification for task: {task[1]}")

def main():
    due_tasks = get_due_tasks()
    for task in due_tasks:
        send_sms(task)

if __name__ == "__main__":
    main()
