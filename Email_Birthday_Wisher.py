# Project - Email Birthday Wisher Automation

import os
import random
import smtplib
import pandas
from datetime import datetime
from zoneinfo import ZoneInfo

# ---------------- LETTER FILES ----------------

letters = [
    "LETTER_1.txt",
    "LETTER_2.txt",
    "LETTER_3.txt",
    "LETTER_4.txt"
]

path_for_letter = random.choice(letters)
path = "Birthday_Data.csv"

# ---------------- EMAIL LOGIN ----------------

user_gmail = os.getenv("EMAIL")
user_password = os.getenv("EMAIL_PASSWORD")

# ---------------- RANDOM SENDERS ----------------

senders = [
    "Shubham 😎",
    "Your Bro 🔥",
    "Best Friend 🚀",
    "Secret Sender 😄"
]

# ---------------- INDIA DATE ----------------

today = datetime.now(ZoneInfo("Asia/Kolkata"))
today_date = (today.month, today.day)

print("Today Date:", today_date)

# ---------------- READ CSV ----------------

data = pandas.read_csv(path)
data.columns = data.columns.str.strip()

print("Columns found:", data.columns.tolist())
print("Selected Letter:", path_for_letter)

# ---------------- SMTP CONNECTION ----------------

connection = smtplib.SMTP("smtp.gmail.com", 587)
connection.starttls()
connection.login(user=user_gmail, password=user_password)

count = 0

# ---------------- MAIN LOOP ----------------

for index, BirthDay_Boy in data.iterrows():

    print(
        "Checking:",
        BirthDay_Boy["Name"],
        (BirthDay_Boy["Month"], BirthDay_Boy["Day"])
    )

    if (
        int(BirthDay_Boy["Month"]),
        int(BirthDay_Boy["Day"])
    ) == today_date:

        print("Birthday Match Found!")

        with open(path_for_letter, "r", encoding="utf-8") as file:

            letter = file.read()

            letter = letter.replace(
                "[NAME]",
                BirthDay_Boy["Name"]
            )

            letter = letter.replace(
                "[SENDER]",
                random.choice(senders)
            )

            clean_lines = []

            for content in letter.splitlines():

                if content.strip().startswith("#"):
                    continue

                clean_lines.append(content)

            final_letter = "\n".join(clean_lines)

            message = f"""Subject: Happy Birthday!

{final_letter}
"""

            print("Sender:", user_gmail)
            print("Receiver:", BirthDay_Boy["Gmail"])

            connection.sendmail(
                from_addr=user_gmail,
                to_addrs=BirthDay_Boy["Gmail"],
                msg=message
            )

            print("Sent to:", BirthDay_Boy["Name"])

            count += 1

# ---------------- CLOSE ----------------

connection.quit()

print(f"\nTotal Emails Sent: {count}")
