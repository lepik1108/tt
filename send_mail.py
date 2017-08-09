import smtplib
import os

from email.mime.text import MIMEText
from pymongo import MongoClient


sender = 'lepik@le.le'
receiver = os.environ['TT_MAIL_RECEIVER']

client = MongoClient('localhost', 27017)
db = client.rozetka
table = db.top_products

body = 'Продукты, помеченные как "Топ Продаж":\n'
for cursor in table.find({}):
	body += cursor['name'] + ' - ' + cursor['price'] + '\n'

message = MIMEText(body)
message['Subject'] = 'Test task deployment results'
message['From'] = sender
message['To'] = receiver

smtpObj = smtplib.SMTP('localhost')
try:
	smtpObj.sendmail(sender, receiver, message.as_string())         
	print ("Successfully sent email")
except:
	print ("Error: unable to send email")
smtpObj.quit()
