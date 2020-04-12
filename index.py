from tkinter import *
from tkinter import messagebox
import time, calendar
from datetime import datetime
from tkinter.ttk import Progressbar
from CustomWidgetClass import MyButton,MySpinBox,MyDialog,MyRowLabel,EditDialog,DeleteDialog
from database import saveIntoDatabase,getData

window = Tk()

window.title("My Work Reminder")
window.geometry('500x500')
window.minsize(500,500)
#let me create 3 different frames! 
#First Frame for holding tasks, time and progressbar(if I want)
#Second Frame for holding buttons! 

data= getData() 
def addToListOfTasks(taskName,userTime):
    saveIntoDatabase(taskName,userTime)
    MyRowLabel(tasksTimeFrame,taskName,userTime)

def addButtonClick():
    inputDialog = MyDialog(window)
    window.wait_window(inputDialog.top)
    if inputDialog.taskVal and inputDialog.ts:
        addToListOfTasks(inputDialog.taskVal,inputDialog.ts)

def editButtonClick():
    if data:
        EditDialog(tasksTimeFrame) 

def deleteButtonClick(tasksTimeFrame):
    if data:
        DeleteDialog(tasksTimeFrame)

tasksTimeFrame = Frame(window)
tasksTimeFrame.pack()

lbl = Label(tasksTimeFrame, text="tasks", font=("Monospace", 24))
lbl.grid(row=0,column=0)

lbl2 = Label(tasksTimeFrame, text="time rem", font=("Monospace", 24))
lbl2.grid(row=0,column=1)

for eachData in data:
    for key,val in eachData.items():
        MyRowLabel(tasksTimeFrame,val[0],int(val[1]))

buttonFrame = Frame(window)
buttonFrame.pack(side=BOTTOM,pady=10)

addButton = Button(buttonFrame, text="Add",command=addButtonClick)
addButton.grid(row=0,column=0,padx=10, pady=10)

editButton = Button(buttonFrame, text="Edit",command=editButtonClick)
editButton.grid(row=0,column=1,padx=10, pady=10)

deleteButton = Button(buttonFrame, text="Delete",command=lambda : deleteButtonClick(tasksTimeFrame))
deleteButton.grid(row=0,column=2,padx=10, pady=10)

window.mainloop()