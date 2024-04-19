import smtplib
import imaplib
import email
from email.mime.multipart import MIMEMultipart
import tkinter as tk
from email.mime.text import MIMEText

def send_email():
    sender_email = sender_email_entry.get()
    sender_password = sender_password_entry.get()
    recipient_email = recipient_email_entry.get()
    recipient_password = recipient_password_entry.get()
    subject = subject_entry.get()
    body = body_entry.get('1.0', 'end-1c')  # Get text from Text widget
    
    try:
        # Set up SMTP connection
        server = smtplib.SMTP( 'smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        
        # Compose email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        server.sendmail(sender_email, recipient_email, msg.as_string())
        result_label.config(text="Email sent successfully", fg="green")
        
        # Close connection
        server.quit()
    except Exception as e:
        result_label.config(text="An error occurred: " + str(e), fg="red")

def receive_email():
    email_address = recipient_email_entry.get()
    password = recipient_password_entry.get()
    
    try:
        # Set up IMAP connection
        mail = imaplib.IMAP4_SSL( 'smtp.gmail.com')
        mail.login(email_address, password)
        mail.select('inbox')
        
        # Search for latest email
        result, data = mail.search(None, 'ALL')
        latest_email_id = data[0].split()[-1]
        
        # Fetch latest email
        result, data = mail.fetch(latest_email_id, '(RFC822)')
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)
        
        # Print email body
        received_email_body.delete('1.0', 'end')  # Clear previous content
        received_email_body.insert('1.0', msg.get_payload())
        
        # Close connection
        mail.close()
        mail.logout()
    except Exception as e:
        result_label.config(text="An error occurred: " + str(e), fg="red")

def receive_email():
    email_address = recipient_email_entry.get()
    password = recipient_password_entry.get()
    
    try:
        # Set up IMAP connection
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(email_address, password)
        mail.select('inbox')
        
        # Search for latest email
        result, data = mail.search(None, 'ALL')
        latest_email_id = data[0].split()[-1]
        
        # Fetch latest email
        result, data = mail.fetch(latest_email_id, '(RFC822)')
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)
        
        # Extract text part from email
        text = ""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == 'text/plain':
                    text = part.get_payload(decode=True).decode()
                    break
        else:
            text = msg.get_payload(decode=True).decode()
        
        # Print email body
        received_email_body.delete('1.0', 'end')  # Clear previous content
        received_email_body.insert('1.0', text)
        
        # Close connection
        mail.close()
        mail.logout()
    except Exception as e:
        result_label.config(text="An error occurred: " + str(e), fg="red")



# GUI setup
root = tk.Tk()
root.title("Email Client")

sender_email_label = tk.Label(root, text="Your Email:")
sender_email_label.grid(row=0, column=0, sticky="e")
sender_email_entry = tk.Entry(root)
sender_email_entry.grid(row=0, column=1)

sender_password_label = tk.Label(root, text="Your Password:")
sender_password_label.grid(row=1, column=0, sticky="e")
sender_password_entry = tk.Entry(root, )
sender_password_entry.grid(row=1, column=1)

recipient_email_label = tk.Label(root, text="Recipient Email:")
recipient_email_label.grid(row=2, column=0, sticky="e")
recipient_email_entry = tk.Entry(root)
recipient_email_entry.grid(row=2, column=1)

recipient_password_label = tk.Label(root, text="Recipient Password:")
recipient_password_label.grid(row=3, column=0, sticky="e")
recipient_password_entry = tk.Entry(root, )
recipient_password_entry.grid(row=3, column=1)

subject_label = tk.Label(root, text="Subject:")
subject_label.grid(row=4, column=0, sticky="e")
subject_entry = tk.Entry(root)
subject_entry.grid(row=4, column=1)

body_label = tk.Label(root, text="Body:")
body_label.grid(row=5, column=0, sticky="ne")
body_entry = tk.Text(root, height=5, width=30)
body_entry.grid(row=5, column=1)

send_button = tk.Button(root, text="Send Email", command=send_email)
send_button.grid(row=6, column=0, columnspan=2, pady=5)

receive_button = tk.Button(root, text="Receive Email", command=receive_email)
receive_button.grid(row=7, column=0, columnspan=2, pady=5)
populate_fields()  # Call the function to populate fields

result_label = tk.Label(root, text="", fg="green")
result_label.grid(row=8, column=0, columnspan=2)

received_email_label = tk.Label(root, text="Received Email:")
received_email_label.grid(row=9, column=0, sticky="ne")
received_email_body = tk.Text(root, height=5, width=30)
received_email_body.grid(row=9, column=1)

root.mainloop()
