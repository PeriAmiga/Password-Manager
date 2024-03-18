import tkinter as tk
from tkinter import *
from tkinter import font
from tkinter import messagebox
import font
import functions
import mysql.connector
from db import dbConnection
import manager

def openChangePasswordPage(changePasswordRoot, username, passwordsData):

    #Add new password to the database
    def changePasswordFunc():

        conn = dbConnection.dbConnect()
        cursor = conn.cursor()

        email = emailInput.get()
        oldPassword = oldPasswordInput.get()
        newPassword = newPasswordInput.get()
        confirmNewPassword = confirmNewPasswordInput.get()

        if (email == "" or oldPassword == "" or newPassword == "" or confirmNewPassword == ""):
            errorLabel.config(text = "Please complete all the fields")
            errorLabel.grid(row=5, columnspan=3, pady=5)
            return

        if (functions.passwordTest(newPassword) == FALSE):
            errorLabel.config(text = "Please choose another password, the password does not meet the requirements")
            errorLabel.grid(row=5, columnspan=3, pady=5)
            return

        if (newPassword != confirmNewPassword):
            errorLabel.config(text = "The new password and confirm password do not match")
            errorLabel.grid(row=5, columnspan=3, pady=5)
            return

        #Hash the password
        with open('./salt.txt', 'r', encoding='utf-8') as file:
            salt = file.read().strip()

        hashOldPassword = functions.hash(oldPassword, salt)
        hashNewPassword = functions.hash(newPassword, salt)

        #Query to check if a user with the provided email, username and password exists
        query = "SELECT * FROM users WHERE email = %s AND username = %s AND password = %s"
        cursor.execute(query, (email, username, hashOldPassword))
        if not (cursor.fetchone()):
            errorLabel.config(text = "There appears to be an issue with the data you have entered")
            errorLabel.grid(row=5, columnspan=3, pady=5)
            return

        #Query to Update the new password to the table users
        query = "UPDATE users SET password = %s WHERE email = %s AND username = %s AND password = %s"
        try:
            cursor.execute(query, (hashNewPassword, email, username, hashOldPassword))
            conn.commit()
            messagebox.showinfo(title="DataBase", message="The password has been changed successfully")
        except:
            messagebox.showerror(title="DataBase", message="Something went wrong, please try again")
        finally:
            cursor.close()
            conn.close()
            managerParent = changePasswordRoot.master
            managerWindow = tk.Toplevel(managerParent.master)
            manager.openManagerPage(managerWindow, username, passwordsData)
            changePasswordRoot.destroy()
            managerParent.destroy()

    #Cancel the addition of new data
    def cancelFunc():
        changePasswordRoot.master.deiconify()
        changePasswordRoot.destroy()


    #Fonts
    headlineFont, labelsFont, buttonsFont, resetPasswordFont = font.configureFonts()

    #Objects
    PasswordManagerChangePassword = Label(changePasswordRoot, text="Password Manager - Change Password", font = headlineFont)
    emailLabel = Label(changePasswordRoot, text = "Email: ", font = labelsFont)
    emailInput = Entry(changePasswordRoot, width = 30)
    oldPasswordLabel = Label(changePasswordRoot, text = "Old Password: ", font = labelsFont)
    oldPasswordInput = Entry(changePasswordRoot, width = 30, show = '*')
    showOldPasswordButton = Button(changePasswordRoot, text="Show", command=lambda: functions.togglePasswordVisibility(oldPasswordInput, showOldPasswordButton), font = buttonsFont, cursor = "hand2")
    newPasswordLabel = Label(changePasswordRoot, text = "New Password: ", font = labelsFont)
    newPasswordInput = Entry(changePasswordRoot, width = 30, show = '*')
    showNewPasswordButton = Button(changePasswordRoot, text="Show", command=lambda: functions.togglePasswordVisibility(newPasswordInput, showNewPasswordButton), font = buttonsFont, cursor = "hand2")
    confirmNewPasswordLabel = Label(changePasswordRoot, text = "Confirm New Password: ", font = labelsFont)
    confirmNewPasswordInput = Entry(changePasswordRoot, width = 30, show = '*')
    showConfirmNewPasswordButton = Button(changePasswordRoot, text="Show", command=lambda: functions.togglePasswordVisibility(confirmNewPasswordInput, showConfirmNewPasswordButton), font = buttonsFont, cursor = "hand2")
    errorLabel = Label(changePasswordRoot, font = labelsFont, fg = "red")
    saveButton = Button(changePasswordRoot, text = "Save", command = changePasswordFunc, font = buttonsFont, cursor = "hand2")
    cancelButton = Button(changePasswordRoot, text = "Cancel", command = cancelFunc, font = buttonsFont, cursor = "hand2")
    changePasswordRoot.bind("<Return>", lambda event, button=saveButton: functions.onEnterKey(event, button))


    #Packing to root
    PasswordManagerChangePassword.grid(row=0, column=0, columnspan=3, pady=20)

    emailLabel.grid(row=1, column=0, sticky='e')
    emailInput.grid(row=1, column=1, padx=10, pady=5)
    oldPasswordLabel.grid(row=2, column=0, sticky='e')
    oldPasswordInput.grid(row=2, column=1, padx=10)
    showOldPasswordButton.grid(row=2, column=2, padx=10, pady=5)
    newPasswordLabel.grid(row=3, column=0, sticky='e')
    newPasswordInput.grid(row=3, column=1, padx=10)
    showNewPasswordButton.grid(row=3, column=2, padx=10, pady=5)
    confirmNewPasswordLabel.grid(row=4, column=0, sticky='e')
    confirmNewPasswordInput.grid(row=4, column=1, padx=10)
    showConfirmNewPasswordButton.grid(row=4, column=2, padx=10, pady=5)
    saveButton.grid(row=6, column=1, sticky='w')
    cancelButton.grid(row=6, column=1, pady = 10, sticky='e')

    changePasswordRoot.update_idletasks() #Update the geometry of the window
    functions.windowDesign(changePasswordRoot)

if __name__ == "__main__":
    changePasswordWindow = tk.Toplevel()
    openChangePasswordPage(changePasswordWindow)
    changePasswordWindow.mainloop()