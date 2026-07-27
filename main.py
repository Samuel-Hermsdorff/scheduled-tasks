import os
import pandas as pd
import smtplib
import datetime as dt
import random as rd
from email.message import EmailMessage

NUMBER_OF_LETTERS = 3
MY_PASSWORD = os.environ.get("MY_PASSWORD")
EMAIL_SERVER = "smtp.gmail.com"
PORT_NUMBER = 587
MY_EMAIL = os.environ.get("MY_EMAIL")
EMAIL_SUBJECT = "Happy Birthday!!"


letters_list = []
birthday_dates = {}
# check if today matches any birthday date in the birthday.csv file
# select a random letter from the list and substitute [NAME] with the name whose birthday matches today
for letter_number in range(1,NUMBER_OF_LETTERS + 1):
    with open(f"letter_templates/letter_{letter_number}.txt", mode='r', encoding="utf-8") as letter_file:
        letters_list.append(letter_file.read())

df = pd.read_csv('birthdays.csv')
date = dt.datetime.now()

for row in df.itertuples():
    birthday_dates[(row.month, row.day)] = (row.name, row.email)

todays_date = (date.month, date.day)

for birthday_date, person_infos in birthday_dates.items():
    if birthday_date == todays_date:
        letter_template = rd.choice(letters_list)
        letter_to_send = letter_template.replace("[NAME]", person_infos[0])
        try:
            msg = EmailMessage()
            msg['Subject'] = EMAIL_SUBJECT
            msg['From'] = MY_EMAIL
            msg['To'] = person_infos[1]
            msg.set_content(letter_to_send)
            with smtplib.SMTP(host=EMAIL_SERVER, port=PORT_NUMBER) as connection:
                connection.starttls()
                connection.login(user=MY_EMAIL,password=GOOGLE_PASS)
                connection.send_message(msg)
        except Exception as error:
            print(f"Error: {error}")
