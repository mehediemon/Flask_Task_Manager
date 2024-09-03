import requests
import psycopg2
from datetime import datetime

TELEGRAM_BOT_TOKEN = 'token'
TELEGRAM_CHAT_ID = 'chat id'
DATABASE_URL = 'postgresql://task_manager_user:12345678@127.0.0.1/task_manager_db'

def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    payload = {'chat_id': TELEGRAM_CHAT_ID, 'text': message}
    requests.post(url, data=payload)

def check_due_tasks():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT id, title, due_date, description FROM task WHERE completed = FALSE AND due_date <= %s", (datetime.now(),))
    tasks = cur.fetchall()
    for task_id, title, due_date, description in tasks:
        message = f'Task Due: {title} {description} (Due Date: {due_date})'
        send_telegram_message(message)
    cur.close()
    conn.close()

if __name__ == "__main__":
    check_due_tasks()
