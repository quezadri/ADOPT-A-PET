# for data scrapping
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# for operating system operations
from os import path

# for mailing
import smtplib
from email.message import EmailMessage
import pandas as pd

# for automatic running
import time
import datetime


print('Hello! Welcome to NJ Adopt A Pet Reminder!')

# Sending mail from user
# gmail account has to allow less secure 3rd party apps, used a throwaway account for this
def send_mail(subject, message):
    EMAIL_ADDRESS = 'NJAdoptaPet@gmail.com'
    EMAIL_PASSWORD = 'PythonLearning10!'

#Spreadsheet of recievers who enroll in reminders
    receiver_email_df = pd.read_excel('receivers.xlsx')
    receiver_email_list = list(receiver_email_df['address'])
    print(receiver_email_list)

    for receiver_email in receiver_email_list:
        print(receiver_email)
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = receiver_email

        msg.add_alternative(message, subtype='html')

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

# Num of new dogs and cats
def fill_message(new_dogs, new_cats):

#HTML integration for messaging
    html_message = """\
<!DOCTYPE html>
<html>
    <body>
        <img class="center" 
            style="width: 800px"
            src="data:image/jpeg;base64,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"
        >
        <h1 style="color:SlateGray; text-align: center;" >New listed pets!</h1>

        <p><strong>Hello! There are __no_dogs__ new doggies and __no_cats__ new moggies up for adoption today. Check them out at the links below:
        </strong></p>
<ul>
"""
    html_message = html_message.replace('__no_dogs__', str(len(new_dogs)))
    html_message = html_message.replace('__no_cats__', str(len(new_cats)))

    for pet_url in new_dogs:
        html_message += """
<li>
<span style="font-family: 'Lucida Sans Unicode', 'Lucida Grande', sans-serif;"><strong>Dog :&nbsp;</strong>__pet_url__
</span>
</li>        
"""
        html_message = html_message.replace('__pet_url__', pet_url)

    for pet_url in new_cats:
        html_message += """
<li>
<span style="font-family: 'Lucida Sans Unicode', 'Lucida Grande', sans-serif;"><strong>Cat :&nbsp;</strong>__pet_url__
</span>
</li>        
"""
        html_message = html_message.replace('__pet_url__', pet_url)

    html_message += """
</ul>
<p><span style="font-family: 'Lucida Sans Unicode', 'Lucida Grande', sans-serif;">Sent by NJ Adopt A Pet</span></p>
    </body>
</html>
"""

    return html_message

# add petId to history
def add_to_history(pet_id, filename):
    if path.exists(filename):
        with open(filename, 'a') as f:
            f.write(pet_id + '\n')
    else:
        with open(filename, 'w') as f:
            f.write(pet_id + '\n')

#Existing petID
def is_existing(pet_id, pet_id_history):
    for i in range(len(pet_id_history)):
        if pet_id == pet_id_history[i]:
            return True
    else:
        return False

#get petID history
def get_pet_id_history(filename):
    if path.exists(filename):
        with open(filename, 'r') as f:
            lines = f.readlines()
        out_list = []
        for line in lines:
            pet_id = line.replace('\n', '')
            if len(pet_id) > 0:
                out_list.append(pet_id)
            else:
                continue
        return out_list
    else:
        with open(filename, 'w') as f:
            f.write('')
            return []

#extract petID
def extract_id(url):
    url_elements = url.split('/')
    slug = url_elements[-1]
    slug_elements = slug.split('-')
    pet_id = slug_elements[0]
    return pet_id


def is_href(attribute):
    attribute_elements = attribute.split(':')
    header = attribute_elements[0]
    if header == 'https':
        return True
    else:
        return False


def get_pet_id(driver):
    pet_card_element = driver.find_element(By.CLASS_NAME, 'petcard')
    if pet_card_element is not None:
        pet_card_link_elements = pet_card_element.find_elements(By.CLASS_NAME, 'pet-card__link')
        if len(pet_card_link_elements) > 0:
            out_list = []
            for pet_card_link_element in pet_card_link_elements:
                attribute = pet_card_link_element.get_attribute('href')
                if is_href(attribute):
                    pet_id = extract_id(attribute)
                    out_list.append((pet_id, attribute))
                else:
                    continue
            return out_list
        else:
            return []
    else:
        return []

# check if new pets by petID
def check_new_pets(driver, url, filename):
    driver.get(url)

    pet_id_list = get_pet_id(driver)
    pet_id_history = get_pet_id_history(filename)
    new_listings = []
    for pet_id, pet_url in pet_id_list:
        print("Checking pet number : " + pet_id)
        if is_existing(pet_id, pet_id_history):
            print('Old listing')
        else:
            print('New listing')
            new_listings.append(pet_url)
            add_to_history(pet_id, filename)
    return new_listings

# if new petID, send email
def daily_task():
    options = ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.headless = True

    driver = Chrome(service=Service(ChromeDriverManager().install()), options=options)

    new_dogs = check_new_pets(driver, 'https://www.adoptapet.com/dog-adoption', '../dogs_ids.txt')
    new_cats = check_new_pets(driver, 'https://www.adoptapet.com/cat-adoption', '../cats_ids.txt')

    if len(new_dogs + new_cats) > 0:
        message = fill_message(new_dogs, new_cats)
        send_mail('New pets are available for adoption, check them out now!', message)

    driver.close()


# 24 hour timer
def timer(hours):
    print('Timer started at {} ({} hours)'.format(datetime.datetime.now(), hours))
    time.sleep(hours*60*60)


def main():
    while True:
        daily_task()
        timer(24)



if __name__ == '__main__':
    main()
