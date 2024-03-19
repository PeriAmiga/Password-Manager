import tkinter as tk
from tkinter import *
from tkinter import font

def configureFonts():
    headlineFont = font.Font(family="Helvetica", size=14, weight="bold", underline=1)
    labelsFont = font.Font(family="Helvetica", size=12)
    buttonsFont = font.Font(family="Helvetica")
    resetPasswordFont = font.Font(family="Helvetica")
    SuggestPasswordFont = font.Font(family="Helvetica", underline=0)

    return headlineFont, labelsFont, buttonsFont, resetPasswordFont