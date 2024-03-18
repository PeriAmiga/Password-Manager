import tkinter as tk
from tkinter import *
from tkinter import font
from tkinter import messagebox
import font
import functions
import mysql.connector
from db import dbConnection
import manager

def openLoginPage(loginRoot):

    #Connect to user
    def loginFunc():

        conn = dbConnection.dbConnect()
        cursor = conn.cursor()

        username = usernameInput.get()
        password = passwordInput.get()

        if (username == "" or password == ""):
            errorLabel.config(text = "Please complete all the fields")
            errorLabel.grid(row=3, columnspan=3, pady=5)
            return

        #Hash the password
        with open('./salt.txt', 'r', encoding='utf-8') as file:
                    salt = file.read().strip()

        hashPassword = functions.hash(password, salt)

        #Query to check if a user with the provided username or email exists
        query = "SELECT * FROM users WHERE username = %s and password = %s"
        cursor.execute(query, (username, hashPassword))
        if not (cursor.fetchone()):
            errorLabel.config(text = "There appears to be an issue with the data you have entered")
            errorLabel.grid(row=3, columnspan=3, pady=5)
            return

        errorLabel.destroy()
        query = "SELECT * FROM passwords WHERE user = %s"
        cursor.execute(query, (username,))
        passwordsData = cursor.fetchall()
        cursor.close()
        conn.close()
        managerWindow = tk.Toplevel(loginRoot)
        manager.openManagerPage(managerWindow, username, passwordsData)
        loginRoot.withdraw()

    #Reset password by sending mail with new password
    def resetPasswordFunc():
        if usernameInput.get() == "":
            errorLabel.config(text = "Please fill in your username first")
            errorLabel.grid(row=3, columnspan=3, pady=5)
        else:
            conn = dbConnection.dbConnect()
            cursor = conn.cursor()
            #Query to check if a user with the provided username exists
            query = "SELECT email FROM users WHERE username = %s"
            cursor.execute(query, (usernameInput.get(),))
            if not (cursor.fetchone()):
                errorLabel.config(text = "There appears to be an issue with the data you have entered")
                errorLabel.grid(row=3, columnspan=3, pady=5)
                return
            errorLabel.destroy()
            flag = functions.sendMail(usernameInput.get())
            if flag == True:
                messagebox.showinfo(title="Mail Sent", message="A new password has been sent to your email")
            else:
                messagebox.showerror(title="Mail did not Sent", message="An error occurred while sending your new password. Please try again.")


    #Fonts
    headlineFont, labelsFont, buttonsFont, resetPasswordFont = font.configureFonts()

    #Objects
    PasswordManagerLogin = Label(loginRoot, text="Password Manager - Login", font = headlineFont)
    usernameLabel = Label(loginRoot, text = "Username: ", font = labelsFont)
    usernameInput = Entry(loginRoot, width = 30)
    passwordLabel = Label(loginRoot, text = "Password: ", font = labelsFont)
    passwordInput = Entry(loginRoot, width = 30, show = '*')
    showPasswordButton = Button(loginRoot, text="Show", command=lambda: functions.togglePasswordVisibility(passwordInput, showPasswordButton), font = buttonsFont, cursor = "hand2")
    errorLabel = Label(loginRoot, font = labelsFont, fg = "red")
    loginButton = Button(loginRoot, text = "Login", command = loginFunc, font = buttonsFont, cursor = "hand2")
    resetPasswordButton = Button(loginRoot, text = "Reset Password", command = resetPasswordFunc, borderwidth = 0, font = resetPasswordFont, fg = "blue", cursor = "hand2")
    loginRoot.bind("<Return>", lambda event, button=loginButton: functions.onEnterKey(event, button))


    #Packing to root
    PasswordManagerLogin.grid(row=0, column=0, columnspan=3, pady=20)
    usernameLabel.grid(row=1, column=0, sticky='e')
    usernameInput.grid(row=1, column=1, padx=10)
    passwordLabel.grid(row=2, column=0, sticky='e')
    passwordInput.grid(row=2, column=1, pady=10)
    showPasswordButton.grid(row=2, column=2, padx=10)
    loginButton.grid(row=4, columnspan=3, pady=5)
    resetPasswordButton.grid(row=5, columnspan=3, pady=5)

    loginRoot.update_idletasks() #Update the geometry of the window
    functions.windowDesign(loginRoot)

if __name__ == "__main__":
    loginWindow = tk.Toplevel()
    openLoginPage(loginWindow)
    loginWindow.mainloop()