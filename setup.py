import os
from google_auth_oauthlib.flow import InstalledAppFlow
import gmailapi
import logging
import logging.handlers
import pickle

# Logger setup
LOG_FILENAME = 'ctqa_email.log'
# Set up a specific logger with our desired output level
logger = logging.getLogger("CTQA-Email")
logger.setLevel(logging.DEBUG)
# Add the log message handler to the logger
handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=2000000, backupCount=3)
formatter = logging.Formatter("%(asctime)s:%(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S")
handler.setFormatter(formatter)
logger.addHandler(handler)

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    'https://www.googleapis.com/auth/gmail.send'
]

sender = input("Please type the GMail address you would like to use: ")

# Creating/writing to sender text file
with open("sender.txt", "w") as f:
  f.write(sender)

# Creating recipient text files
open("recipients_daily.txt", "a").close()
open("recipients_weekly.txt", "a").close()
open("recipients_warning.txt", "a").close()
open("recipients_failure.txt", "a").close()

flow = InstalledAppFlow.from_client_secrets_file(
  'ctqa-creds.json', SCOPES)
creds = flow.run_local_server()

# Save the credentials for the next run
with open('token.pickle', 'wb') as token:
  pickle.dump(creds, token)

answer = input("Would you like to send a test email? (y/n): ")
if answer == "y" or answer == "Y":
  answer = input("Where would you like to send the test email?: ")
  res = gmailapi.email(sender, answer, "CTQA-Emailer Test", "Test Message Body")

  if res == -1:
    print("The test message could not be sent. Please check the log for more details.")
  else:
    print("Your test message has been sent successfully!")
