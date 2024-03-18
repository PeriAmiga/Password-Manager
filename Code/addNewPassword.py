import tkinter as tk
from tkinter import *
from tkinter import font
from tkinter import messagebox
import font
import functions
import mysql.connector
from db import dbConnection
import manager


def openAddNewPasswordPage(addNewPasswordRoot, username, passwordsData):

    #Add new password to the database
    def addNewPasswordFunc():

        conn = dbConnection.dbConnect()
        cursor = conn.cursor()

        appname = appNameInput.get()
        url = urlInput.get()
        appusername = usernameInput.get()
        password = passwordInput.get()

        if (appname == "" or url == "" or username == "" or password == ""):
            errorLabel.config(text = "Please complete all the fields")
            errorLabel.grid(row=5, columnspan=3, pady=5)
            return

        if not (functions.isValidUrl(url)):
            errorLabel.config(text = 'Please change the URL, it should be like "https://www.example.com"')
            errorLabel.grid(row=5, columnspan=3, pady=5)
            return

        #Query to add the new data to the table passwords
        query = "INSERT INTO passwords(user, name, url, username, password)VALUES (%s, %s, %s, %s, %s)"
        try:
            encryptedPassword = functions.encryptPassword(password)
            cursor.execute(query, (username, appname, url, appusername, encryptedPassword))
            conn.commit()
            passwordsData.append([None, username, appname, url, appusername, encryptedPassword])
            messagebox.showinfo(title="DataBase", message="The password has been added successfully")
        except:
            messagebox.showerror(title="DataBase", message="Something went wrong, please try again")
        finally:
            cursor.close()
            conn.close()
            managerParent = addNewPasswordRoot.master
            managerWindow = tk.Toplevel(managerParent.master)
            manager.openManagerPage(managerWindow, username, passwordsData)
            addNewPasswordRoot.destroy()
            managerParent.destroy()

    #Cancel the addition of new data
    def cancelFunc():
        addNewPasswordRoot.master.deiconify()
        addNewPasswordRoot.destroy()


    #Fonts
    headlineFont, labelsFont, buttonsFont, resetPasswordFont = font.configureFonts()

    #Objects
    PasswordManagerAddNewPassword = Label(addNewPasswordRoot, text="Password Manager - Add New Password", font = headlineFont)
    appNameLabel = Label(addNewPasswordRoot, text = "App Name: ", font = labelsFont)
    appNameInput = Entry(addNewPasswordRoot, width = 30)
    urlLabel = Label(addNewPasswordRoot, text = "URL: ", font = labelsFont)
    urlInput = Entry(addNewPasswordRoot, width = 30)
    usernameLabel = Label(addNewPasswordRoot, text = "Username: ", font = labelsFont)
    usernameInput = Entry(addNewPasswordRoot, width = 30)
    passwordLabel = Label(addNewPasswordRoot, text = "Password: ", font = labelsFont)
    passwordInput = Entry(addNewPasswordRoot, width = 30, show = '*')
    showPasswordButton = Button(addNewPasswordRoot, text="Show", command=lambda: functions.togglePasswordVisibility(passwordInput, showPasswordButton), font = buttonsFont, cursor = "hand2")
    errorLabel = Label(addNewPasswordRoot, font = labelsFont, fg = "red")
    saveButton = Button(addNewPasswordRoot, text = "Save", command = addNewPasswordFunc, font = buttonsFont, cursor = "hand2")
    cancelButton = Button(addNewPasswordRoot, text = "Cancel", command = cancelFunc, font = buttonsFont, cursor = "hand2")
    addNewPasswordRoot.bind("<Return>", lambda event, button=saveButton: functions.onEnterKey(event, button))


    #Packing to root
    PasswordManagerAddNewPassword.grid(row=0, column=0, columnspan=3, pady=20)

    appNameLabel.grid(row=1, column=0, sticky='e')
    appNameInput.grid(row=1, column=1, padx=10)
    urlLabel.grid(row=2, column=0, sticky='e')
    urlInput.grid(row=2, column=1, padx=10)
    usernameLabel.grid(row=3, column=0, sticky='e')
    usernameInput.grid(row=3, column=1, padx=10)
    passwordLabel.grid(row=4, column=0, sticky='e')
    passwordInput.grid(row=4, column=1, pady=10)
    showPasswordButton.grid(row=4, column=2, padx=10)
    saveButton.grid(row=6, column=1, sticky='w')
    cancelButton.grid(row=6, column=1, pady = 10, sticky='e')

    addNewPasswordRoot.update_idletasks() #Update the geometry of the window
    functions.windowDesign(addNewPasswordRoot)

if __name__ == "__main__":
    addNewPasswordWindow = tk.Toplevel()
    openAddNewPasswordPage(addNewPasswordWindow)
    addNewPasswordWindow.mainloop()