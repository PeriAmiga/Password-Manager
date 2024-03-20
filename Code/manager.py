import tkinter as tk
from tkinter import *
from tkinter import font
import font
import functions
import mysql.connector
import webbrowser
import addNewPassword
import changePassword
from db import dbConnection
import pandas as pd
import os
from pathlib import Path
from tkinter import messagebox

def openManagerPage(managerRoot, username, passwordsData):


    def openUrl(event):
        #Get the URL from the label's text
        url = event.widget.cget("text")
        webbrowser.open(url)


    def dataSearch(event):
        search_text = searchInput.get().lower()
        for row in dataRows:
            if search_text in row[0].cget("text").lower() or search_text in row[1].cget("text").lower():
                for item in row:
                    item.grid()
            else:
                for item in row:
                    item.grid_remove()


    def clearSearch(event):
        searchInput.delete(0, END)
        dataSearch(event)


    def deleteData(appnameLabel, url, usernameInput, passwordInput, showPasswordButton, editButton, deleteButton, dataRows, editButtons, sortedPasswordsData, sortedDecryptedPasswordsData, index):

        #If the password is currently in "show" mode, change it to "hide" before editing
        if showPasswordButton.cget("text") == "Hide":
            showPasswordButton.invoke()

        editButtons.remove(editButton)
        dataRows.remove([appnameLabel, url, usernameInput, passwordInput, showPasswordButton, editButton, deleteButton])
        appname = appnameLabel.cget("text")
        u = url.cget("text")
        ui = usernameInput.get()
        pi = passwordInput.get()
        functions.deleteRow(username, appname, u, ui, pi)
        sortedPasswordsData.pop(index)
        #Refreshing the window
        managerWindow = tk.Toplevel(managerRoot.master)
        openManagerPage(managerWindow, username, sortedPasswordsData)
        managerRoot.destroy()


    def addNewDataFunc():
        addNewPasswordWindow = tk.Toplevel(managerRoot)
        addNewPassword.openAddNewPasswordPage(addNewPasswordWindow, username, passwordsData)
        managerRoot.withdraw()


    def changePasswordFunc():
        changePasswordWindow = tk.Toplevel(managerRoot)
        changePassword.openChangePasswordPage(changePasswordWindow, username, passwordsData)
        managerRoot.withdraw()


    def extractDataFunc(passwordsData, sortedDecryptedPasswordsData):
        excelData = []
        excelData.append(["name", "url", "username", "password"]) #Headlines
        for data, decryptedData in zip(sortedPasswordsData, sortedDecryptedPasswordsData):
            excelData.append([data[2], data[3], data[4], decryptedData]) #Data
        #Create a DataFrame from the data
        excelTable = pd.DataFrame(excelData)

        desktopPath = Path.home() / "Desktop"  #Get the path to the desktop
        #Modify the export path to save the file on the desktop
        excelFilePath = desktopPath / "Password Manager - Passwords.csv"

        #Check if the file already exists
        if os.path.exists(excelFilePath):
            os.remove(excelFilePath)  #Remove the existing file

        #Export the DataFrame to an Excel file
        excelTable.to_csv(excelFilePath, index=False, header=False)
        messagebox.showinfo(title="CSV File", message="The data has been successfully extracted. You can find it on your desktop")


    #Update the scrollbar when the canvas's size changes
    def updateScrollRegion(event):
        canvas.configure(scrollregion=canvas.bbox("all"))


    #Sorting the data
    sortedPasswordsData = sorted(passwordsData, key=lambda x: x[2])
    #Creating an array with decrypted passwords
    sortedDecryptedPasswordsData = []
    for password in sortedPasswordsData:
        encryptedPassword = password[5]
        decryptedPassword = functions.decryptPassword(encryptedPassword)
        sortedDecryptedPasswordsData.append(decryptedPassword)


    #Fonts
    headlineFont, labelsFont, buttonsFont, resetPasswordFont = font.configureFonts()
    dataFont = tk.font.Font(family="Helvetica", size=10)
    urlFont = tk.font.Font(family="Helvetica", size=10, underline=1)


    #Objects
    PasswordManagerManager = Label(managerRoot, text = "Password Manager - Manager", font = headlineFont)
    helloLabel = Label(managerRoot, text = f'Hello {username},', font = labelsFont)
    changePasswordButton = Button(managerRoot, text = "Change Password", font = buttonsFont, cursor = "hand2", command = changePasswordFunc)
    searchLabel = Label(managerRoot, text = "Search by Appname or URL:", font = labelsFont)
    searchInput = Entry(managerRoot, width = 20, font = dataFont)
    clearButton = Button(managerRoot, text = "Clear", font = buttonsFont, cursor = "hand2")

    appnameLabel = Label(managerRoot, text = "App Name", font = labelsFont)
    urlLabel = Label(managerRoot, text = "URL", font = labelsFont)
    usernameLabel = Label(managerRoot, text = "Username", font = labelsFont)
    passwordLabel = Label(managerRoot, text = "Password", font = labelsFont)

    canvas = Canvas(managerRoot) #Create a Canvas widget that will display all the data within it
    scrollbar = Scrollbar(managerRoot, orient="vertical", command=canvas.yview) #Create a scrollbar widget
    canvas.configure(yscrollcommand=scrollbar.set) #Configure the Canvas to scroll with the scrollbar
    frame = Frame(canvas) #Create a frame to contain the data inside the Canvas
    canvas.create_window((0, 0), window=frame, anchor="nw")

    importData = Button(managerRoot, text = "Import Data", font = buttonsFont, cursor = "hand2", command = lambda mr=managerRoot, pd=passwordsData, un=username: functions.importDataFunc(mr, un, pd))
    extractData = Button(managerRoot, text = "Extract Data", font = buttonsFont, cursor = "hand2", command = lambda pd=passwordsData, sdp=sortedDecryptedPasswordsData: extractDataFunc(pd, sdp))
    addNewData = Button(managerRoot, text = "Add New Data", font = buttonsFont, cursor = "hand2", command = addNewDataFunc)


    #Packing to root
    PasswordManagerManager.grid(row=0, column=0, columnspan=8, pady=20)
    helloLabel.grid(row=1, column=0, padx=10)
    changePasswordButton.grid(row=1, column=6, padx=10, pady=10)
    searchLabel.grid(row=2, column=2, padx=5)
    searchInput.grid(row=2, column=3, padx=5)
    clearButton.grid(row=2, column=4, pady=20)
    appnameLabel.grid(row=3, column=0, padx=10)
    urlLabel.grid(row=3, column=1, padx=10)
    usernameLabel.grid(row=3, column=2, padx=10)
    passwordLabel.grid(row=3, column=3, padx=10)
    canvas.grid(row=4, column=0, columnspan=7, sticky="nsew")
    scrollbar.grid(row=4, column=7, sticky="ns")


    #adding all the data to the window
    rowNum = 4
    dataRows = []
    editButtons = []
    index = 0
    for data, decryptedData in zip(sortedPasswordsData, sortedDecryptedPasswordsData):
        #Objects
        appnameLabel = Label(frame, text = data[2], font = dataFont)
        url = Label(frame, text = data[3], font = urlFont, fg = "blue")
        usernameInput = Entry(frame, width = 20, font = dataFont)
        passwordInput = Entry(frame, width = 20, font = dataFont, show = '*')
        showPasswordButton = Button(frame, text = "Show", font = buttonsFont, cursor = "hand2")
        showPasswordButton.config(command=lambda pi=passwordInput, spb=showPasswordButton, ep=data[5], dp=decryptedData: functions.toggleDecryptedPasswordVisibility(pi, spb, ep, dp))
        editButton = Button(frame, text = "Edit", font = buttonsFont, cursor = "hand2")
        editButton.config(command=lambda ui=usernameInput, pi=passwordInput, eb=editButton, spb=showPasswordButton, url=url, spd=sortedPasswordsData, sdp=sortedDecryptedPasswordsData, i=index: functions.editData(username, editButtons, ui, pi, eb, spb, url, spd, sdp, i))
        deleteButton = Button(frame, text = "Delete", font = buttonsFont, cursor = "hand2")
        editButtons.append(editButton)
        dataRows.append([appnameLabel, url, usernameInput, passwordInput, showPasswordButton, editButton, deleteButton])
        deleteButton.config(command = lambda an=appnameLabel, u=url, ui=usernameInput, pi=passwordInput, spb=showPasswordButton, eb=editButton, db=deleteButton, dr=dataRows, ebs=editButtons, spd=sortedPasswordsData, sdp=sortedDecryptedPasswordsData, i=index: deleteData(an, u, ui, pi, spb, eb, db, dr, ebs, spd, sdp, i))


        #Packing to root
        appnameLabel.grid(row=rowNum, column=0, padx=10, pady=10)
        url.grid(row=rowNum, column=1, padx=10)
        usernameInput.grid(row=rowNum, column=2, padx=10)
        passwordInput.grid(row=rowNum, column=3, padx=10)
        showPasswordButton.grid(row=rowNum, column=4, padx=10)
        editButton.grid(row=rowNum, column=5, padx=10)
        deleteButton.grid(row=rowNum, column=6, padx=10)

        #Adding data to the username and password entries
        usernameInput.delete(0, END)
        passwordInput.delete(0, END)
        usernameInput.insert(0, data[4])
        passwordInput.insert(0, data[5])
        usernameInput.config(state=tk.DISABLED)
        passwordInput.config(state=tk.DISABLED)

        #Turn the urls to be clickable
        url.bind("<Button-1>", openUrl)
        url.config(cursor="hand2")

        rowNum = rowNum + 1
        index = index + 1
    addNewData.grid(row=rowNum, columnspan=8, pady=10)
    importData.grid(row=rowNum, column=5, padx=10)
    extractData.grid(row=rowNum, column=6, padx=10)
    searchInput.bind("<KeyRelease>", dataSearch) #Apply Search
    clearButton.bind("<Button-1>", clearSearch) #Clear Search Input
    canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(-1 * int(event.delta/120), "units"))
    frame.bind("<Configure>", updateScrollRegion)
    managerRoot.update_idletasks() #Update the geometry of the window
    functions.windowDesign(managerRoot)


if __name__ == "__main__":
    managerWindow = tk.Toplevel()
    openManagerPage(managerWindow)
    managerWindow.mainloop()