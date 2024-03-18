import tkinter as tk
from tkinter import *
from tkinter import font
from tkinter import messagebox
from tkinter import filedialog
from db import dbConnection
from db import configuration
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string
import hashlib
import pbkdf2
from cryptography.fernet import Fernet
import base64
import pandas as pd
import manager


#Password visibility
def togglePasswordVisibility(passwordInput, showPasswordButton):
    if passwordInput.cget("show") == "":
        passwordInput.config(show="*") #Hide the password
        showPasswordButton.config(text="Show")
    else:
        passwordInput.config(show="") #Show the password
        showPasswordButton.config(text="Hide")


#Decrypted Password visibility
def toggleDecryptedPasswordVisibility(passwordInput, showPasswordButton, encryptedPassword, decryptedPassword):
    if passwordInput.cget("show") == "":
        passwordInput.config(show="*") #Hide the password
        passwordInput.config(state=tk.NORMAL)
        passwordInput.delete(0, tk.END) #Clear the current password
        passwordInput.insert(0, encryptedPassword) #Insert the new encrypted password
        passwordInput.config(state=tk.DISABLED)
        showPasswordButton.config(text="Show")
    else:
        passwordInput.config(show="") #Show the password
        passwordInput.config(state=tk.NORMAL)
        passwordInput.delete(0, tk.END) #Clear the current password
        passwordInput.insert(0, decryptedPassword) #Insert the new decrypted password
        passwordInput.config(state=tk.DISABLED)
        showPasswordButton.config(text="Hide")


#Edit usernames and passwords
def editData(username, editButtons, usernameInput, passwordInput, editButton, showPasswordButton, url, sortedPasswordsData, sortedDecryptedPasswordsData, index):
    global oldUsername
    global oldPassword

    def cancelEditingData(oldUsername, oldPassword):
        editButton.config(text="Edit")
        passwordInput.config(show="*")
        showPasswordButton.config(text="Show", command=lambda pi=passwordInput, spb=showPasswordButton, ep=oldPassword, dp=decryptPassword(oldPassword): toggleDecryptedPasswordVisibility(pi, spb, ep, dp))
        usernameInput.delete(0, END)
        passwordInput.delete(0, END)
        usernameInput.insert(0, oldUsername)
        passwordInput.insert(0, oldPassword)
        usernameInput.config(state=tk.DISABLED)
        passwordInput.config(state=tk.DISABLED)
        for button in editButtons:
            if button is not editButton:
                button.config(state=tk.NORMAL)


    newUsername = ""
    newPassword = ""
    urlText = ""

    #If the password is currently in "show" mode, change it to "hide" before editing
    if showPasswordButton.cget("text") == "Hide":
        showPasswordButton.invoke()

    #Option to edit data in the db
    if editButton.cget("text") == "Edit":
        editButton.config(text="Save")
        passwordInput.config(show="")  #Show the password
        showPasswordButton.config(text="Cancel")
        oldUsername = usernameInput.get()
        oldPassword = passwordInput.get()
        oldDecryptedPassword = decryptPassword(oldPassword)
        usernameInput.config(state=tk.NORMAL)
        passwordInput.config(state=tk.NORMAL)
        passwordInput.delete(0, tk.END) #Clear the current encrypted password
        passwordInput.insert(0, oldDecryptedPassword) #Insert the old decrypted password
        showPasswordButton.config(command = lambda oU = oldUsername, oP = oldPassword: cancelEditingData(oU, oP))

        #Disable the option to edit 2 rows in one time
        for button in editButtons:
            if button is not editButton:
                button.config(state=tk.DISABLED)

    #Option to save the changes in the db
    else:
        newUsername = usernameInput.get()
        newPassword = passwordInput.get()
        newEncryptedPassword = encryptPassword(newPassword)
        passwordInput.delete(0, tk.END) #Clear the current decrypted password
        passwordInput.insert(0, newEncryptedPassword) #Insert the encrypted password
        urlText = url.cget("text")
        usernameInput.config(state=tk.DISABLED)
        passwordInput.config(state=tk.DISABLED)
        editButton.config(text="Edit")
        passwordInput.config(show="*")  #Hide the password
        showPasswordButton.config(text="Show", state=tk.NORMAL)
        showPasswordButton.config(text="Show", command=lambda pi=passwordInput, spb=showPasswordButton, ep=newEncryptedPassword, dp=decryptPassword(newEncryptedPassword): toggleDecryptedPasswordVisibility(pi, spb, ep, dp))
        conn = dbConnection.dbConnect()
        cursor = conn.cursor()
        query = "UPDATE passwords SET username = %s, password = %s WHERE user = %s AND username = %s AND password = %s AND url = %s"
        try:
            cursor.execute(query, (newUsername, newEncryptedPassword, username,oldUsername, oldPassword, urlText))
            conn.commit()
            oldPasswordData = sortedPasswordsData[index]
            newPasswordData = (*oldPasswordData[:5], newEncryptedPassword, *oldPasswordData[6:])
            sortedPasswordsData[index] = newPasswordData
            sortedDecryptedPasswordsData[index] = newPassword
            messagebox.showinfo(title="DataBase", message="The username and password updated successfully")
            oldUsername = ""
            oldPassword = ""
        except:
            messagebox.showerror(title="DataBase", message="Something went wrong, please try again")
            usernameInput.delete(0, END)
            passwordInput.delete(0, END)
            usernameInput.insert(0, oldUsername)
            passwordInput.insert(0, oldPassword)
            oldUsername = ""
            oldPassword = ""
        finally:
            for button in editButtons:
                if button is not editButton:
                    button.config(state=tk.NORMAL)
            cursor.close()
            conn.close()


#Password requirements: 10 characters, at least 1 special character, 1 uppercase letter, and 1 lowercase letter
def passwordTest(password):
    #Define a regular expression pattern to match the requirements
    pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%^&+=!])(?!.*\s).{10,}$"

    #Use re.match to check if the password matches the pattern
    return bool(re.match(pattern, password))

def onClosing(window):
    #Close this window
    window.destroy()
    #Close all parent windows (if any)
    parent = window.master
    while parent:
        parent.destroy()
        parent = parent.master

def windowDesign(window):
    #Get the updated geometry of the window
    window.update_idletasks()
    #Add title to the program
    window.title("PasswordManager - By Peri Amiga")
    #Add icon to the program
    window.iconbitmap("")
    img = PhotoImage(file='../Images/icon.png')
    window.iconphoto(False, img)
    #Bring the new window to the front
    window.attributes("-topmost", True)
    #Cancel the option to resize the window
    window.resizable(False, False)
    #When the X button is clicked, close the entire program
    window.protocol("WM_DELETE_WINDOW", lambda: onClosing(window))

    #Get screen dimension and find the center point to set the position of the windows
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    window_width = window.winfo_width()
    window_height = window.winfo_height()

    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)

    window.geometry(f'+{center_x}+{center_y}')

#Simulate a button click when the Enter key is pressed
def onEnterKey(event, button):
    button.invoke()

def deleteRow(user, appname, url, username, password):
    conn = dbConnection.dbConnect()
    cursor = conn.cursor()
    query = "DELETE from passwords WHERE user = %s AND name = %s AND url = %s AND username = %s AND password = %s"
    try:
        cursor.execute(query, (user, appname, url, username, password))
        conn.commit()
        messagebox.showinfo(title="DataBase", message="The username and password deleted successfully")
    except:
        messagebox.showerror(title="DataBase", message="Something went wrong, please try again")
    finally:
        cursor.close()
        conn.close()

def generateRandomPassword():
    #Define the character sets for uppercase, lowercase, special characters, and digits
    uppercaseLetters = string.ascii_uppercase
    lowercaseLetters = string.ascii_lowercase
    specialCharacters = '!@#$%^&*?'
    digits = string.digits

    #Initialize the password with one character from each category
    password = [
        random.choice(uppercaseLetters),
        random.choice(lowercaseLetters),
        random.choice(specialCharacters),
        random.choice(digits)
    ]

    #Add random characters to complete the 10-character password
    while len(password) < 10:
        password.append(random.choice(uppercaseLetters + lowercaseLetters + specialCharacters + digits))

    #Shuffle the characters to randomize the password
    random.shuffle(password)

    #Convert the list of characters to a string
    return ''.join(password)

def sendMail(username):
    #Generate a new random password with 10 characters
    newPassword = generateRandomPassword()

    #Hash the password
    with open('./salt.txt', 'r', encoding='utf-8') as file:
        salt = file.read().strip()

    hashNewPassword = hash(newPassword, salt)

    #Update the new password in the database for the user
    conn = dbConnection.dbConnect()
    cursor = conn.cursor()
    #Query to get the email of the user
    query = "SELECT email FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    userEmail = cursor.fetchone()[0]
    query = "UPDATE users SET password = %s WHERE username = %s"
    cursor.execute(query, (hashNewPassword, username))
    conn.commit()
    cursor.close()
    conn.close()

    #Send mail with new password
    try:
            #Email server settings for Gmail
            smtpServer = configuration.smtpServer
            smtpPort = configuration.smtpPort

            #Sender and recipient
            systemEmail = configuration.systemEmail
            recipientEmail = userEmail

            #Create an email message
            subject = 'Password Manager - Password Reset'
            message = f'Here is your new password: {newPassword}.\nDo not share it with anyone!'
            msg = MIMEMultipart()
            msg['From'] = systemEmail
            msg['To'] = recipientEmail
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'plain'))

            #Connect to the Gmail SMTP server
            server = smtplib.SMTP(smtpServer, smtpPort)
            server.starttls()  #Use TLS (Transport Layer Security)

            #Login to your Gmail account
            systemEmailPassword = configuration.systemEmailPassword
            server.login(systemEmail, systemEmailPassword)

            #Send the email
            server.sendmail(systemEmail, recipientEmail, msg.as_string())

            #Quit the SMTP server
            server.quit()

            return True  #Email sent successfully
    except Exception as e:
        print(f'Error sending email: {str(e)}')
        return False  #Email sending failed


def suggestPassword(passwordInput):
    #Define the character sets
    uppercase_letters = string.ascii_uppercase
    lowercase_letters = string.ascii_lowercase
    special_characters = '@#$%^&+=!'

    #Ensure at least one character from each set
    password = [random.choice(uppercase_letters),
                random.choice(lowercase_letters),
                random.choice(special_characters),
                random.choice(string.digits)]

    #Fill the rest of the password with random characters
    password += [random.choice(string.ascii_letters + string.digits + special_characters) for i in range(10)]

    #Shuffle the characters to make the password random
    random.shuffle(password)

    #Clear the entry "passwordInput"
    passwordInput.delete(0, tk.END)

    #Convert the list of characters to a string and set it as the value of passwordInput
    passwordInput.insert(0, ''.join(password))


def hash(str, salt):
    input_bytes = str.encode('utf-8')
    hash_bytes = hashlib.pbkdf2_hmac('sha256', input_bytes, salt.encode('utf-8'), 1000, 32)
    return hash_bytes.hex()


def encryptPassword(password):
    try:
        with open('./symmetric.txt', 'r', encoding='utf-8') as file:
            key = file.read().strip()
        key_bytes = base64.b64decode(key) #Decode the base64-encoded key
        cipher = Fernet(key_bytes)
        encryptedPassword_bytes = cipher.encrypt(password.encode())
        encryptedPasswordStr = encryptedPassword_bytes.decode('utf-8')  #Decode bytes to str
        return encryptedPasswordStr
    except Exception as e:
        print("Error encrypting password:", e)
        return None

def decryptPassword(encryptedPassword):
    try:
        with open('./symmetric.txt', 'r', encoding='utf-8') as file:
            key = file.read().strip()
        key_bytes = base64.b64decode(key) #Decode the base64-encoded key
        cipher = Fernet(key_bytes)
        decryptedPassword = cipher.decrypt(encryptedPassword).decode()
        return decryptedPassword
    except Exception as e:
        print("Error decrypting password:", e)
        return None


#Check if the url is valid
def isValidUrl(url):
    # Regex pattern to match URL format
    urlPattern = re.compile(
        r'^(https?://)?'  #http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  #Domain
        r'localhost|'  #localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  #If it is ipv4
        r'(?::\d+)?'  #Optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return bool(re.match(urlPattern, url))


def chooseCsvDirectory(root):
    root = tk.Tk()
    root.withdraw()  #Hide the main window

    filePath = filedialog.askopenfilename(
        title="Select CSV File",
        filetypes=[("CSV files", "*.csv")]
    )
    return filePath


def importDataFunc(managerRoot, clientUsername, passwordsData):
    messagebox.showinfo(title="CSV File", message="Please ensure that the data includes column headers for the Name, URL, Username, and Password")
    # Read CSV file
    try:
        filePath = chooseCsvDirectory(managerRoot)
        data = pd.read_csv(filePath)

        #Convert all columns to strings
        data = data.astype(str)


        #Extracting each column by name to a list
        requiredColumns = ['name', 'url', 'username', 'password']
        if not all(colName in data.columns for colName in requiredColumns):
            messagebox.showerror(title="CSV File", message="Please ensure that the CSV file include the next columns: name, url, username and password")
            return

        appNameArray = data['name'].tolist()
        urlArray = data['url'].tolist()
        usernameArray = data['username'].tolist()
        decryptedPasswordArray = data['password'].tolist()

        failures = []

        #Adding the data to the arrays and to the database
        for i in range(len(appNameArray)):
            name = appNameArray[i]
            url = urlArray[i]
            username = usernameArray[i]
            decryptedPassword = decryptedPasswordArray[i]
            #Check if the data of each row is correct
            if (name == "nan" or url == "nan" or username == "nan" or decryptedPassword == "nan"):
                failures.append(i + 2)
                continue

            if not (isValidUrl(url)):
                failures.append(i + 2)
                continue

            conn = dbConnection.dbConnect()
            cursor = conn.cursor()

            encryptedPassword = encryptPassword(decryptedPassword)

            #Check if the data is already exists in the database before adding it
            queryCheck = "SELECT * FROM passwords WHERE user = %s and name = %s and url = %s and username = %s"
            cursor.execute(queryCheck, (clientUsername, name, url, username))
            result = cursor.fetchone()
            if (result):
                if (decryptPassword(result[5]) == decryptedPassword):
                    continue

            #Query to add the new data to the table passwords
            queryInsert = "INSERT INTO passwords(user, name, url, username, password)VALUES (%s, %s, %s, %s, %s)"
            try:
                cursor.execute(queryInsert, (clientUsername, name, url, username, encryptedPassword))
                conn.commit()
                queryData = "SELECT * FROM passwords WHERE user = %s"
                cursor.execute(queryData, (clientUsername,))
                passwordsData = cursor.fetchall()
            except:
                messagebox.showerror(title="DataBase", message="Something went wrong, please try again")
            finally:
                cursor.close()
                conn.close()
        #Refreshing the window
        managerWindow = tk.Toplevel(managerRoot.master)
        manager.openManagerPage(managerWindow, clientUsername, passwordsData)
        managerRoot.destroy()
        #Check if some data did not import
        if (len(failures) == 0):
            messagebox.showinfo(title="DataBase", message="The data has been imported successfully")
        else:
            messagebox.showerror(title="DataBase", message=f"Some of the data in the file failed to add successfully.\nThis can be caused by two reasons:\n1. One of the parameters in the row is empty.\n2. The URL in the row is invalid.\n\nPlease check the next rows and try again:\n{', '.join(str(item) for item in failures)}")

    except FileNotFoundError:
        messagebox.showerror(title="CSV File", message="File not found. Please make sure you've entered the correct file path or canceled the operation")