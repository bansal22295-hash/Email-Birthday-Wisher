# ==========================================================
# Email Birthday Wisher Automation (GitHub Actions Version)
# ==========================================================

import os
import random
import smtplib
import pandas

from datetime import datetime
from zoneinfo import ZoneInfo

from email.mime.text import MIMEText

# ==========================================================
# LETTER FILES
# ==========================================================

letters = [
    "LETTER_1.txt",
    "LETTER_2.txt",
    "LETTER_3.txt",
    "LETTER_4.txt",
    "LETTER_5.txt",
]

path_for_letter = random.choice(letters)

# ==========================================================
# CSV FILE
# ==========================================================

csv_file = "Birthday_Data.csv"

# ==========================================================
# GITHUB SECRETS
# ==========================================================

user_gmail = os.getenv("EMAIL")
user_password = os.getenv("EMAIL_PASSWORD")

# ==========================================================
# RANDOM SENDER NAMES
# ==========================================================

senders = [
    "Shubham 😎",
    "Your Bro 🔥",
    "Best Friend 🚀",
    "Secret Sender 😄"
]

# ==========================================================
# INDIA TIMEZONE
# ==========================================================

today = datetime.now(
    ZoneInfo("Asia/Kolkata")
)

today_date = (
    today.month,
    today.day
)

print("=" * 50)
print("EMAIL BIRTHDAY WISHER STARTED")
print("=" * 50)

print(f"Today Date : {today_date}")
print(f"Selected Letter : {path_for_letter}")

# ==========================================================
# VALIDATE SECRETS
# ==========================================================

if not user_gmail:
    raise ValueError(
        "EMAIL secret not found in GitHub Actions."
    )

if not user_password:
    raise ValueError(
        "EMAIL_PASSWORD secret not found in GitHub Actions."
    )

print("EMAIL Secret Found ✅")
print("PASSWORD Secret Found ✅")

# ==========================================================
# LOAD CSV
# ==========================================================

try:

    data = pandas.read_csv(csv_file)

    data.columns = (
        data.columns
        .str.strip()
    )

    print(
        "Columns Found:",
        data.columns.tolist()
    )

except FileNotFoundError:

    print(
        f"ERROR: '{csv_file}' not found."
    )

    raise

except Exception as error:

    print(
        "CSV Loading Error:",
        error
    )

    raise

# ==========================================================
# CONNECT TO GMAIL
# ==========================================================

try:

    print(
        "\nConnecting to Gmail..."
    )

    connection = smtplib.SMTP(
        "smtp.gmail.com",
        587
    )

    connection.starttls()

    connection.login(
        user=user_gmail,
        password=user_password
    )

    print(
        "Gmail Login Successful ✅"
    )

except Exception as error:

    print(
        "Gmail Login Failed ❌"
    )

    print(error)

    raise

# ==========================================================
# SEND EMAILS
# ==========================================================

count = 0

for index, birthday_person in data.iterrows():

    try:

        person_name = (
            birthday_person["Name"]
        )

        person_email = (
            birthday_person["Gmail"]
        )

        person_month = int(
            birthday_person["Month"]
        )

        person_day = int(
            birthday_person["Day"]
        )

        birthday_date = (
            person_month,
            person_day
        )

        print(
            f"\nChecking {person_name}"
        )

        print(
            f"CSV Date : {birthday_date}"
        )

        # --------------------------------------------------
        # Birthday Match
        # --------------------------------------------------

        if birthday_date == today_date:

            print(
                "Birthday Match Found 🎉"
            )

            # ----------------------------------------------
            # Read Letter
            # ----------------------------------------------

            try:

                with open(
                    path_for_letter,
                    "r",
                    encoding="utf-8"
                ) as file:

                    letter = file.read()

            except FileNotFoundError:

                print(
                    f"Letter File Missing: "
                    f"{path_for_letter}"
                )

                continue

            # ----------------------------------------------
            # Replace Placeholders
            # ----------------------------------------------

            letter = letter.replace(
                "[NAME]",
                person_name
            )

            letter = letter.replace(
                "[SENDER]",
                random.choice(senders)
            )

            # ----------------------------------------------
            # Remove Comment Lines
            # ----------------------------------------------

            clean_lines = []

            for line in (
                letter.splitlines()
            ):

                if (
                    line.strip()
                    .startswith("#")
                ):
                    continue

                clean_lines.append(
                    line
                )

            final_letter = (
                "\n".join(clean_lines)
            )

            # ----------------------------------------------
            # MIME Email
            # ----------------------------------------------

            message = MIMEText(
                final_letter,
                "plain",
                "utf-8"
            )

            message[
                "Subject"
            ] = "Happy Birthday! 🎂"

            message[
                "From"
            ] = user_gmail

            message[
                "To"
            ] = person_email

            print(
                f"Sender   : {user_gmail}"
            )

            print(
                f"Receiver : {person_email}"
            )

            # ----------------------------------------------
            # Send Email
            # ----------------------------------------------

            connection.sendmail(
                from_addr=user_gmail,
                to_addrs=person_email,
                msg=message.as_string()
            )

            count += 1

            print(
                f"Email Sent To "
                f"{person_name} ✅"
            )

        else:

            print(
                "No Birthday Today"
            )

    except KeyError as error:

        print(
            f"Missing CSV Column: "
            f"{error}"
        )

    except Exception as error:

        print(
            f"Error Processing Row: "
            f"{error}"
        )

# ==========================================================
# CLOSE CONNECTION
# ==========================================================

try:

    connection.quit()

    print(
        "\nSMTP Connection Closed ✅"
    )

except Exception as error:

    print(
        "Error Closing SMTP:"
    )

    print(error)

# ==========================================================
# FINAL REPORT
# ==========================================================

print("\n" + "=" * 50)

print(
    f"Total Emails Sent: {count}"
)

print("=" * 50)
