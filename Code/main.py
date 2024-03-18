import tkinter as tk
from tkinter import *
from tkinter import font
import login
import register
import font
import functions
from db import schemaCreation
from db import dbConnection
from db import passwordsTableCreation
from db import usersTableCreation


root = Tk()

#Design the window
functions.windowDesign(root)

#Open login window
def loginFunc():
    loginWindow = tk.Toplevel(root)
    login.openLoginPage(loginWindow)
    root.withdraw()
#Open register window
def registerFunc():
    registerWindow = tk.Toplevel(root)
    register.openRegisterPage(registerWindow)
    root.withdraw()
#Close the program
def exitFunc():
    root.destroy()

#Fonts
headlineFont, labelsFont, buttonsFont, resetPasswordFont = font.configureFonts()

#Objects
PasswordManager = Label(root, text = "Password Manager", font = headlineFont)
loginButton = Button(root, text = "Login", command = loginFunc, font = buttonsFont, cursor = "hand2")
registerButton = Button(root, text = "Register", command = registerFunc, font = buttonsFont, cursor="hand2")
exitButton = Button(root, text = "Exit", command = exitFunc, font = buttonsFont, cursor="hand2")

#Packing to root
PasswordManager.grid(row=0, columnspan=1, pady=10)
loginButton.grid(row=1, columnspan=1, pady=5)
registerButton.grid(row=2, columnspan=1, pady=5)
exitButton.grid(row=3, columnspan=1, pady=5)

root.mainloop()