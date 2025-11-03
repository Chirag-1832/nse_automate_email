from nsetools import Nse
from datetime import date, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# === CONFIG ===
SENDER_EMAIL = os.environ['EMAIL_USER']
APP_PASSWORD = os.environ['EMAIL_PASS']
RECEIVER_EMAIL = os.environ['EMAIL_TO']

# === DATA ===
nse = Nse()
yesterday = (date.today() - timedelta(days=1)).strftime('%d-%b-%Y')

nifty = nse.get_index_quote("nifty 50")
gainers = nse.get_top_gainers()[:5]
losers = nse.get_top_losers()[:5]

# === EMAIL BODY ===
email_body = f"""
<h2>📊 NSE Daily Summary – {yesterday}</h2>
<b>NIFTY 50:</b> {nifty['lastPrice']} ({nifty['pChange']}%)<br><br>
<b>Top Gainers:</b><br>
<ul>{''.join([f"<li>{x['symbol']} ({x['netPrice']}%)</li>" for x in gainers])}</ul>
<b>Top Losers:</b><br>
<ul>{''.join([f"<li>{x['symbol']} ({x['netPrice']}%)</li>" for x in losers])}</ul>
"""

# === EMAIL SEND ===
msg = MIMEMultipart("alternative")
msg["Subject"] = f"NSE Summary – {yesterday}"
msg["From"] = SENDER_EMAIL
msg["To"] = RECEIVER_EMAIL
msg.attach(MIMEText(email_body, "html"))

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(SENDER_EMAIL, APP_PASSWORD)
    server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())

print("✅ Email sent successfully!")
