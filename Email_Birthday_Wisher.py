# Project - Email Birthday Wisher Automation

import os
import random
import smtplib
import pandas
from datetime import datetime as dt

# ---------------- PATHS ----------------

path_for_letter = "LETTER_{random.randint(1,3)}.txt"
path = "Birthday_Data.csv"

# ---------------- YOUR EMAIL LOGIN ----------------
# KEEP PRIVATE (do NOT share)
user_gmail = os.getenv("EMAL")
user_password = os.etenv("EMAIL_PASSWORD")


# ---------------- RANDOM SENDERS ----------------

senders = [
    "Robin 😎",
    "Your Bro 🔥",
    "Best Friend 🚀",
    "Secret Sender 😄"
]

# ---------------- DATE ----------------

today = dt.now()
today_date = (today.month, today.day)

# ---------------- READ CSV ----------------

data = pandas.read_csv(path)
data.columns = data.columns.str.strip()

# ---------------- SMTP CONNECTION ----------------

connection = smtplib.SMTP("smtp.gmail.com", 587)
connection.starttls()
connection.login(user=user_gmail, password=user_password)

count = 0

# ---------------- MAIN LOOP ----------------

for (index, BirthDay_Boy) in data.iterrows():

    if (BirthDay_Boy["Month"], BirthDay_Boy["Day"]) == today_date:

        # read random letter
        with open(path_for_letter, "r", encoding="utf-8", errors="ignore") as file:
            letter = file.read()
            letter = letter.replace("[NAME]", BirthDay_Boy["Name"])
            letter = letter.replace("[SENDER]", random.choice(senders))

            clean_lines = []
            for Content in letter.splitlines():
                if Content.strip().startswith("#"):
                    continue
                clean_lines.append(Content)

            final_letter = "\n".join(clean_lines)

            message = f"Subject:Happy Birthday!\n\n{final_letter}"

            connection.sendmail(
                from_addr=user_gmail,
                to_addrs=BirthDay_Boy["Gmail"],
                msg=message.encode("utf-8")
            )


        count += 1
        print("Sent to:", BirthDay_Boy["Name"])

# ---------------- CLOSE ----------------

connection.close()

print(f"\nTotal Emails Sent: {count}")
