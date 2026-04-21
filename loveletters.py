import os
import random
from dotenv import load_dotenv
from twilio.rest import Client

# Load environment variables from .env file
load_dotenv()

# Assign varrables using os.getenv
# This looks for the keys you defined in your .env file
ACC_SID = os.getenv('TWILIO_ACCOUNT_SID')
AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
FROM_NUM = os.getenv('TWILIO_PHONE_NUMBER')
TO_NUM = os.getenv('RECIPIENT_PHONE_NUMBER')

#---COMPLIMNET BANK---#
messages = [
    "good morning my love! you're so amazing. have an amazing day<333",
    "i just want to remind you that i love you so much reign and i think about you every second of every day",
    "you're my one true love. mahal kita reign<33333",
    "you're such a strong a beautiful person baby, you got this!!",
    "i fall more in love with you every day reign, have an amazing day muahh<3333",
    "i hope you have a great day today, i love you so much reign<3333",
    "you are my muse reign, you inspire me to push forward and improve every day. thank you for being in my corner. i value you so much!! mahal kita reign<3333",
    "it's okay to have bad days, just know that i love you so much and i'm here for you no matter what. you got this reign<3333",
    "i hope you have a great day today, i love you so much reign<3333",
    "i'm infatuated with your soul my love, you are the personification of peace and hope. i love you more than you'll ever know.",
    "you got this reign, i believe in you and i know you can do anything you set your mind to. i love you so much<3333",
    "don't forget to take care of yourself today reign, you deserve it. i love you so much<3333",
    "i love us, we're an amazing team and i can't wait to see what the future holds for us. i love you so much reign<3333",
    "i'll always be here for you reign, through the good and the bad. i love you so much<3333",
    "magandang umaga, reign. have a great day baby, ingat ka palagi. mahal kita<3333",
    "my soul yearns for yours, i love you so much reign. have an amazing day<3333",
]

def send_compliment():
    # we initittialize the client inside the function to ensure it uses the fresh credentials every time it runs.
    client = Client(ACC_SID, AUTH_TOKEN)
    body_text = random.choice(messages)
    
    try:
        message = client.messages.create(
            body=body_text,
            from_=FROM_NUM,
            to=TO_NUM
        )
        print(f"Message sent successfully! SID: {message.sid}")   
    except Exception as e:
        print(f"Failed to send message: {e}")
        