from __future__ import print_function
import gmailapi
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.text import MIMEText
import base64
import json
import sys
import logging
import logging.handlers
import gmailapi
import datetime

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
SENDER = None
RECIPIENTS = None

# Attempting to load sender
try:
  with open("sender.txt", "r") as f:
    SENDER = f.read()
except Exception as e:
  logger.error(str(e))

# Attempting to grab data
notification = None
try:
  notification = sys.argv[1]
  logger.debug("Received argument: %s" % notification)
except IndexError:
  logger.error("The script was run but no arguments were found. Exiting...")
  exit(0)

# Decoding base64 string
decoded_data = None
try:
  decoded_data = str(base64.b64decode(sys.argv[1]), 'utf-8')
  logger.debug("Decoded base64 string: %s" % decoded_data)
except UnicodeDecodeError as e:
  logger.error(str(e))
  logger.error("Could not decode the argument from a base64 string. Exiting...")
  exit(0)

# Decoding JSON string
data = None
try:
  data = json.loads(decoded_data)
  logger.debug("Decoded JSON string: %s" % str(data))
except Exception as e:
  logger.error(str(e))
  logger.error("Could not decode JSON string into a dict. Exiting...")
  exit(0)

# Getting notification type
notificationtype = None
try:
  notificationtype = sys.argv[2]
  logger.debug("Received notification type: %s" % notificationtype)
except IndexError as e:
  logger.error(str(e))
  logger.error("Notification type was not found. Exiting...")
  exit(0)

# Daily
if notificationtype == "daily":
  # Getting recipients
  with open("recipients_daily.txt") as f:
    RECIPIENTS = f.read().replace("\n", ", ")
  
  subject = "CTQA: Daily Reports"
  body = "%d daily report(s) from the CTQA utility are attached.\nDate/time Run: %s" % (len(data), str(datetime.datetime.now()))
  gmailapi.email(SENDER, RECIPIENTS, subject, body, attachments=data)

# Weekly
elif notificationtype == "weekly":
  # Getting recipients
  with open("recipients_weekly.txt") as f:
    RECIPIENTS = f.read().replace("\n", ", ")
  
  subject = "CTQA: Weekly Reports"
  body = "%d weekly report(s) from the CTQA utility are attached.\nDate/time Run: %s" % (len(data), str(datetime.datetime.now()))
  gmailapi.email(SENDER, RECIPIENTS, subject, body, attachments=data)

# Failure
elif notificationtype == "failure":
  # Getting recipients
  with open("recipients_failure.txt") as f:
    RECIPIENTS = f.read().replace("\n", ", ")
  
  filename = os.path.basename(data["reportLocation"]).split(".")[0]
  roi_value = data["roiValue"]

  subject = "CTQA: FAILURE"
  body = "Failure detected in site: %s.\nRegion of interest value: %f\nDate/time Run: %s"  % (filename, roi_value, str(datetime.datetime.now()))
  gmailapi.email(SENDER, RECIPIENTS, subject, body, attachments=[data["reportLocation"]])
  
# Warning
elif notificationtype == "warning":
  # Getting recipients
  with open("recipients_warning.txt") as f:
    RECIPIENTS = f.read().replace("\n", ", ")

  filename = os.path.basename(data["reportLocation"]).split(".")[0]
  roi_value = data["roiValue"]
  forecast_days = data["forecastDays"]
  
  subject = "CTQA: WARNING"
  body = "Drift detected in site: %s.\nRegion of interest value: %f\nForecast Days: %d\nDate/time Run: %s"  % (filename, roi_value, forecast_days, str(datetime.datetime.now()))
  gmailapi.email(SENDER, RECIPIENTS, subject, body, attachments=[data["reportLocation"]])

else:
  logger.error("Notification type is not a recognized value. Exiting...")
  exit(0)

logger.debug("Finished\n")
