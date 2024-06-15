from flask import Flask

app = Flask(__name__)
access_granted = False  # This will be updated based on admin's response

@app.route('/allow', methods=['GET'])
def allow():
    global access_granted
    access_granted = True
    return "Access granted.", 200

@app.route('/deny', methods=['GET'])
def deny():
    global access_granted
    access_granted = False
    return "Access denied.", 200

if __name__ == "__main__":
    app.run(port=5000)

import smtplib
from email.mime.text import MIMEText

def send_verification_email(admin_email):
    allow_link = "http://localhost:5000/allow"
    deny_link = "http://localhost:5000/deny"

    message = f"""
    Please click the appropriate link below to allow or deny the action:
    
    Allow: {allow_link}
    Deny: {deny_link}
    """
    msg = MIMEText(message)
    msg['Subject'] = 'Action Verification'
    msg['From'] = 'your_email@example.com'
    msg['To'] = admin_email

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login('your_email@example.com', 'your_email_password')
        server.sendmail('your_email@example.com', admin_email, msg.as_string())

# Usage
send_verification_email('admin_email@example.com')

import tkinter as tk
from tkinter import simpledialog, messagebox
import time
import requests

def check_email_verification():
    for _ in range(10):  # Check for admin's response for a certain period
        response = requests.get('http://localhost:5000/status')
        if response.status_code == 200 and response.text == "Access granted.":
            return True
        elif response.status_code == 200 and response.text == "Access denied.":
            return False
        time.sleep(10)  # Check every 10 seconds
    return False

def check_password(stored_password):
    entered_password = simpledialog.askstring("Password", "Enter your password:", show='*')
    
    if entered_password == stored_password:
        send_verification_email('admin_email@example.com')
        if check_email_verification():
            messagebox.showinfo("Success", "Password correct. Access granted.")
        else:
            messagebox.showwarning("Denied", "Access denied.")
    else:
        messagebox.showerror("Error", "Incorrect password.")

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    stored_password = "my_secure_password"
    
    check_password(stored_password)

    root.mainloop()

if __name__ == "__main__":
    main()

