import smtplib
from pathlib import Path
import os
from dotenv import load_dotenv

class Util:
    '''Utility class'''
    
    @staticmethod
    def send_email(data):
        '''Function to send email to a user'''
        
        BASE_DIR = Path(__file__).resolve().parent.parent
        print(BASE_DIR)
        load_dotenv(os.path.join(BASE_DIR, ".env"))
        
        EMAIL_HOST_USER = os.getenv('MY_EMAIL')
        EMAIL_HOST_PASSWORD = os.getenv('PASSWORD')
        
        with smtplib.SMTP('smtp.gmail.com', 587) as conn:
            conn.starttls()
            conn.login(user=EMAIL_HOST_USER, password=EMAIL_HOST_PASSWORD)
            
            conn.sendmail(
                from_addr=EMAIL_HOST_USER, 
                to_addrs=EMAIL_HOST_USER,
                msg=f"Subject:Message from {data['name'].split()[-1]}\n\nHi, my name is {data['name']} with email {data['email']}.\n\nThis is my message:\n{data['message']}"
            )
            
            conn.sendmail(
                from_addr=EMAIL_HOST_USER, 
                to_addrs=data['email'],
                msg=f"Subject:BUHREC has received your email.\n\nThank you for contacting us, {data['name'].split()[-1]}.\n\nYour email has been received and a response will be provided as soon as possible."
            )
            