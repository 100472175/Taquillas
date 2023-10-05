import os.path
import sys
import time
import schedule
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from confirmation.email_send import send_backup_email_db


def job():
    send_backup_email_db()
    # add your Twitter code here

# Run job on a specific day of the week
schedule.every().friday.at("22:22").do(job)

while True:
    print(1)
    schedule.run_pending()
    time.sleep(1800)