import tkinter as tk
from tkinter import *
from tkinter import font
from tkinter import messagebox
import font
import functions
import mysql.connector
from db import dbConnection


def openRegisterPage(registerRoot):

    #Register user
    def registerFunc():

        conn = dbConnection.dbConnect()
        cursor = conn.cursor()

        email = emailInput.get()
        username = usernameInput.get()
        password = passwordInput.get()
        confirmPass = confirmPasswordInput.get()

        if (email == "" or username == "" or password == "" or confirmPass == ""):
            errorLabel.config(text = "Please complete all the fields")
            errorLabel.grid(row=6, columnspan=3, pady=5)
            return

        #Query to check if a user with the provided username or email exists
        query = "SELECT * FROM users WHERE username = %s OR email = %s"
        cursor.execute(query, (username, email))
        if (cursor.fetchone()):
            errorLabel.config(text = "The requested username or email is already in use, Please choose another one")
            errorLabel.grid(row=6, columnspan=3, pady=5)
            return

        if (functions.passwordTest(password) == FALSE):
            errorLabel.config(text = "Please choose another password, the password does not meet the requirements")
            errorLabel.grid(row=6, columnspan=3, pady=5)
            return

        if (password != confirmPass):
            errorLabel.config(text = "The passwords are not match")
            errorLabel.grid(row=6, columnspan=3, pady=5)
            return

        #Hash the password
        with open('./salt.txt', 'r', encoding='utf-8') as file:
            salt = file.read().strip()

        hashPassword = functions.hash(password, salt)



        errorLabel.destroy()
        insert_query = "INSERT INTO users (email, username, password) VALUES (%s, %s, %s)"
        data = (email, username, hashPassword)
        cursor.execute(insert_query, data)
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo(title="DataBase", message="The user created successfully")
        registerRoot.master.deiconify()
        registerRoot.destroy()


    #Fonts
    headlineFont, labelsFont, buttonsFont, resetPasswordFont = font.configureFonts()

    #Objects
    PasswordManagerRegister = Label(registerRoot, text="Password Manager - Register", font = headlineFont)
    emailLabel = Label(registerRoot, text = "Email: ", font = labelsFont)
    emailInput = Entry(registerRoot, width = 30)
    usernameLabel = Label(registerRoot, text = "Username: ", font = labelsFont)
    usernameInput = Entry(registerRoot, width = 30)
    passwordLabel = Label(registerRoot, text = "Password: ", font = labelsFont)
    passwordInput = Entry(registerRoot, width = 30, show = '*')
    showPasswordButton = Button(registerRoot, text = "Show", command=lambda: functions.togglePasswordVisibility(passwordInput, showPasswordButton), font = buttonsFont, cursor = "hand2")
    suggestPasswordButton = Button(registerRoot, text = "Suggest Strong Password", command=lambda: functions.suggestPassword(passwordInput), borderwidth = 0, font = resetPasswordFont, fg = "red", cursor = "hand2")
    confirmPasswordLabel = Label(registerRoot, text = "Confirm Password: ", font = labelsFont)
    confirmPasswordInput = Entry(registerRoot, width = 30, show = '*')
    showConfirmPasswordButton = Button(registerRoot, text = "Show", command=lambda: functions.togglePasswordVisibility(confirmPasswordInput, showConfirmPasswordButton), font = buttonsFont, cursor = "hand2")
    errorLabel = Label(registerRoot, font = labelsFont, fg = "red")
    registerButton = Button(registerRoot, text = "Register", command = registerFunc, font = buttonsFont, cursor = "hand2")
    registerRoot.bind("<Return>", lambda event, button=registerButton: functions.onEnterKey(event, button))

    #Packing to root
    PasswordManagerRegister.grid(row=0, column=0, columnspan=3, pady=20)
    emailLabel.grid(row=1, column=0, sticky='e')
    emailInput.grid(row=1, column=1, padx=10, pady=5)
    usernameLabel.grid(row=2, column=0, sticky='e')
    usernameInput.grid(row=2, column=1, padx=10, pady=5)
    passwordLabel.grid(row=3, column=0, sticky='e')
    passwordInput.grid(row=3, column=1, pady=5)
    showPasswordButton.grid(row=3, column=2, padx=10, pady=5)
    confirmPasswordLabel.grid(row=4, column=0, sticky='e')
    confirmPasswordInput.grid(row=4, column=1, pady=5)
    showConfirmPasswordButton.grid(row=4, column=2, padx=10)
    suggestPasswordButton.grid(row=5, columnspan=3, pady=5)
    registerButton.grid(row=7, columnspan=3, pady=5)

    registerRoot.update_idletasks() #Update the geometry of the window
    functions.windowDesign(registerRoot)

if __name__ == "__main__":
    registerWindow = tk.Toplevel()
    openRegisterPage(registerWindow)
    registerWindow.mainloop()