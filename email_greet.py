import imaplib  #for accessing emails over imap protocol
import smtplib  #module used for sending emails using SMTP
import email
import traceback 
import time
import re

EMAIL = "@gmail.com" 
USERNAME_EMAIL = "enter-your-email" + EMAIL 
_PWD_ = "enter-your-new-generated-password" 
SMTP_PORT = 993
SMTP_SERVER = "imap.gmail.com" 

word_to_check = ["congrat", "congo", "felicitat",]

def reading_emails_from_gmail():
    """ The function will return the last 5 emails with a word similar to or same as  "congratulations" 
    """ 

    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(USERNAME_EMAIL,_PWD_)
        mail.select('inbox')

        info = mail.search(None, 'ALL')

        mail_id = info[1]
        mail_id_list = mail_id[0].split()   
        first_email_id = int(mail_id_list[0])
        recent_email_id = int(mail_id_list[-1])

        congratulation_email_found = 0

        for i in range(recent_email_id,first_email_id, -1):
            info = mail.fetch(str(i), '(RFC822)' )

            for response in info:
                arr = response[0]
                if isinstance(arr, tuple):
                    msg = email.message_from_string(str(arr[1],'utf-8'))
                    email_subject = msg['subject']      #get the subject of the email

                    body = ""

                    # get the body of email
                    if msg.is_multipart():
                        for given_part in msg.walk():
                            content_type = given_part.get_content_type()
                            content_status = str(given_part.get('Content-Status'))
 
                            if content_type == 'text/plain' and 'attachment' not in content_status:
                                body = any.get_payload(decode=True)  
                                break
        
                    else:
                        body = msg.get_payload(decode=True)
                    
                    # Regex expression to find words similar to or equivalent to congratulations!
                    regex = r"(?=("+'|'.join(word_to_check)+r"))"

                    # If that expression is either found in the subject or in the body of the email regardless of its CASE ( uppercase or lowercase) then print the subject 
                    # and update the number
                    if re.search(regex, str(body), re.IGNORECASE) or re.search(regex, str(email_subject), re.IGNORECASE):
                        print('Subject : ' + email_subject + '\n')
                        congratulation_email_found += 1
                        break

            # As only last 5 emails are to be displayed as an output          
            if congratulation_email_found == 5:
                break
            
    except Exception as e:
        traceback.print_exc() 
        print(str(e))

#calling the function
reading_emails_from_gmail()
