import os
import datetime

LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'user_activity.log')

def log_activity(message):
    try:
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(f'{timestamp} - {message}\n')
    except Exception as e:
        print(f"Error logging: {e}")
        print(f"Message: {message}")