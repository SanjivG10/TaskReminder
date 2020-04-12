from  tkinter import Button,Spinbox,StringVar
from tkinter.ttk import Progressbar
import tkinter.ttk as ttk 
from tkinter import * 
import time, calendar
from datetime import datetime
from timeRemainder import getTimeMaxTime
from  database import saveIntoDatabase,getData,delDatabase,updateTheListDatabase

class EditLabel(Label):
    def __init__(self, master=None, text=None, width=None, **kwargs):
        if text and width and len(text) > width:
            text = text[:width-3] + '...'
        label=self.label = Label(master, text=text, width=width, **kwargs)
        label.config(padx=10,pady=10)
        label.grid(row=MyRowLabel.counter,column=0)

    def destroy(self):
        self.label.destroy()

class MyRowLabel():
    counter = 1
    LABEL_WIDTH = 16
    dataHolderArray = [] 

    def  __init__(self,parent,key,tasksName,timeForTasks,**kwargs):
        self.parent = parent  
        self.editLabel = EditLabel(parent,tasksName,MyRowLabel.LABEL_WIDTH,**kwargs)

        progressBarContainerFrame=self.progressBarContainerFrame = Frame(parent)
        progressBarContainerFrame.grid(row=MyRowLabel.counter,column=1)

        times,maxTimes = getTimeMaxTime(timeForTasks)

        kwargs['length'] = 40

        kwargs['maximum'] = maxTimes[0]
        kwargs['value'] = times[0]
        self.yearProgressBar =self.yearProgressBar = Progressbar(progressBarContainerFrame,**kwargs)
        self.yearProgressBar.grid(row=0,column=0)
        label = Label(progressBarContainerFrame,text='',padx=2)
        label.grid(row=0,column=1)
        self.labelYear = Label(progressBarContainerFrame,text="{} years".format(times[0]),padx=2)
        self.labelYear.grid(row=MyRowLabel.counter+1,column=0)

        kwargs['maximum'] = maxTimes[1]
        kwargs['value'] = times[1]
        self.monthProgressBar = Progressbar(progressBarContainerFrame,**kwargs)
        self.monthProgressBar.grid(row=0,column=2)
        label = Label(progressBarContainerFrame,text='',padx=2)
        label.grid(row=0,column=3)
        self.labelMonth = Label(progressBarContainerFrame,text="{} months".format(times[1]),padx=2)
        self.labelMonth.grid(row=MyRowLabel.counter+1,column=2)


        kwargs['maximum'] = maxTimes[2]
        kwargs['value'] = times[2]
        self.dayProgressBar = Progressbar(progressBarContainerFrame,**kwargs)
        self.dayProgressBar.grid(row=0,column=4)
        label = Label(progressBarContainerFrame,text='',padx=2)
        label.grid(row=0,column=5)
        self.labelDay  = Label(progressBarContainerFrame,text="{} days".format(times[2]),padx=2)
        self.labelDay.grid(row=MyRowLabel.counter+1,column=4)


        kwargs['maximum'] = maxTimes[3]
        kwargs['value'] = times[3]
        self.hourProgressBar = Progressbar(progressBarContainerFrame,**kwargs)
        self.hourProgressBar.grid(row=0,column=6)
        label = Label(progressBarContainerFrame,text='',padx=2)
        label.grid(row=0,column=7)
        self.labelHour = Label(progressBarContainerFrame,text="{} hours".format(times[3]),padx=2)
        self.labelHour.grid(row=MyRowLabel.counter+1,column=6)


        kwargs['maximum'] = maxTimes[4]
        kwargs['value'] = times[4]
        self.minuteProgressBar = Progressbar(progressBarContainerFrame,**kwargs)
        self.minuteProgressBar.grid(row=0,column=8)
        label = Label(progressBarContainerFrame,text='',padx=2)
        label.grid(row=0,column=9)
        self.labelMinute = Label(progressBarContainerFrame,text="{} minutes".format(times[4]),padx=2)
        self.labelMinute.grid(row=MyRowLabel.counter+1,column=8)

        MyRowLabel.counter+=1
        MyRowLabel.dataHolderArray.append([key,self])

    def destroy(self):
        self.progressBarContainerFrame.destroy() 
        self.editLabel.destroy()

class MyButton(Button):
    def  __init__(self,parent,key=None,**kwargs):
        super().__init__(parent,**kwargs)
        self.key= key

            
class MySpinBox(Spinbox):
    
    def __init__(self,parent,dothis,**kw):
        self.str = StringVar()
        if kw.get('textvariable'):
            self.str.set(kw.get('textvariable'))
        else:
            self.str.set('')
        kw['textvariable'] = self.str   
        self.str.trace('w',self.stringChangeListener)
        super().__init__(parent,**kw)
        self.old_value = ''
        self.get, self.set = self.str.get, self.str.set
        self.dothis = dothis

    def stringChangeListener(self,*args):
        if self.dothis:
            self.dothis(self)        

class MyDialog:
    def __init__(self, parent,data=None):
        top = self.top = Toplevel(parent)
        
        self.error = ''
        self.ts= None
        self.taskVal = ''
        if data:
            self.taskVal= list(data.values())[0][0]
        
        timeSelectionFrame = Frame(top)
        timeSelectionFrame.pack()
        
        myFrame = Frame(top)
        myFrame.pack()

        timeSelectionFrame = Frame(top)
        timeSelectionFrame.pack()

        myLabel = Label(myFrame, text='Enter new task and time')
        myLabel.pack()

        self.taskString = Entry(myFrame)
        self.taskString.insert(END,self.taskVal)
        self.taskString.pack()

        mySubmitButton = Button(myFrame, text='Save', command=self.send)
        mySubmitButton.pack(side=BOTTOM,pady=10)

        if not data:
            year, month, day, hour, minute = map(int, time.strftime("%Y %m %d %H %M").split())
        else:
            now =datetime.fromtimestamp(int(list(data.values())[0][1]))
            year, month, day, hour, minute,second=now.year, now.month, now.day, now.hour, now.minute, now.second

        yearLabel = Label(timeSelectionFrame, text="Year")
        yearLabel.grid(column=0,row=0)

        self.yearSpinner = MySpinBox(timeSelectionFrame,self.validateInt,textvariable=year,from_=2020, to=2100, width=5)
        self.yearSpinner.grid(column=1,row=0)

        monthLabel = Label(timeSelectionFrame, text="Month")
        monthLabel.grid(column=0,row=1)
        self.monthSpinner = MySpinBox(timeSelectionFrame,self.validateInt,textvariable=month, from_=1, to=12, width=5)
        self.monthSpinner.grid(column=1,row=1)

        dayLabel = Label(timeSelectionFrame, text="Day")
        dayLabel.grid(column=0,row=2)
        self.daySpinner = MySpinBox(timeSelectionFrame,self.validateInt,textvariable=day, from_=1, to=31, width=5)
        self.daySpinner.grid(column=1,row=2)

        hourLabel = Label(timeSelectionFrame, text="Hour")
        hourLabel.grid(column=0,row=3)
        self.hourSpinner= MySpinBox(timeSelectionFrame,self.validateInt,textvariable=hour, from_=0, to=23, width=5)
        self.hourSpinner.grid(column=1,row=3)

        minuteLabel = Label(timeSelectionFrame, text="Minute")
        minuteLabel.grid(column=0,row=4)
        self.minuteSpinner = MySpinBox(timeSelectionFrame,self.validateInt,textvariable=minute,from_=0, to=59, width=5)
        self.minuteSpinner.grid(column=1,row=4)

        self.errorLabel = Label(timeSelectionFrame, text="",fg='#ff0000',bd=2)
        self.errorLabel.grid(column=0,row=6,padx=5,pady=5)
    
    def send(self):
        self.error=''
        self.errorLabel['text']=''
    
        day = self.daySpinner.get().strip()
        month = self.monthSpinner.get().strip()
        year = self.yearSpinner.get().strip()
        hour = self.hourSpinner.get().strip()
        minute = self.minuteSpinner.get().strip()

        Cyear, Cmonth, Cday, Chour, Cminute = map(int, time.strftime("%Y %m %d %H %M").split())
        day,month,year,hour,minute = map(int,[day,month,year,hour,minute])

        
        
        selectedDateString = '{}-{}-{} {}:{}:{}'.format(year,month,day,hour,minute,0)

        try:
            dt = datetime.strptime(selectedDateString, '%Y-%m-%d %H:%M:%S')
            self.ts = time.mktime(dt.timetuple())
        except ValueError:
            self.error='Date given is invalid.Check '

        if self.ts and not ((self.ts-time.time())/60>5):
            self.error = 'Date must be at least 5 minutes from your current time'
        
        if year-Cyear >5:
            self.error='Time difference is too much'
        
        if ( self.ts and self.ts-time.time() < 0):
            self.error='The time looks like it is of past'

        self.taskVal = self.taskString.get()
        
        if len(self.taskVal)<5:
            self.error='Write at least 5 letter for your task'
        
        if self.error:
            self.errorLabel['text'] = self.error
        else:
            self.top.destroy()

        #let me validate year, time and seconds  
        #check if year is valid!  

    
    def validateInt(self,spinBoxRef):
        if spinBoxRef.get().isdigit():
            spinBoxRef.old_value=spinBoxRef.get()
        else:
            spinBoxRef.set(spinBoxRef.old_value)


class DeleteRow(MyRowLabel):
    def __init__(self,frame,val,index,data,editDialogRef):

        l = Label(frame,text=val[0],padx=10,pady=10)
        l.grid(row=index,column=0) 

        times,maxTimes = getTimeMaxTime(val[1])
        
        l = Label(frame,text=':'.join(times),padx=10,pady=10)
        l.grid(row=index,column=1)
        
        b = MyButton(frame,text='Delete',key=index,padx=10,pady=2)
        b['command'] = lambda: self.delData(b.key,data,editDialogRef,index) 
        b.grid(row=index,column=2)

    def delData(self,key,data,editDialogRef,index):
        currentData = data[key]
        for key,val in currentData.items():
            deletedDataDateKey=key
            delDatabase(key)

        editDialogRef.top.destroy()

        for index,eachMyRowLabelDataArray in enumerate(MyRowLabel.dataHolderArray):
            keyOfThatVal = eachMyRowLabelDataArray[0]
            valRef = eachMyRowLabelDataArray[1]
            if keyOfThatVal==deletedDataDateKey:
                valRef = eachMyRowLabelDataArray[1].destroy()    
                MyRowLabel.dataHolderArray.pop(index)
                break 


class DeleteDialog():
    def __init__(self,parent): 
        top = self.top = Toplevel(parent)
        frame = Frame(top)
        frame.pack()
        data = getData()

        for index,eachData in enumerate(data):
            for key,val in eachData.items():
                DeleteRow(frame,val,index,data,self)

class EditRow(MyRowLabel):
    def __init__(self,frame,val,index,data,editDialogRef):
        self.top = frame 
        l = Label(frame,text=val[0],padx=10,pady=10)
        l.grid(row=index,column=0) 

        times,maxTimes = getTimeMaxTime(val[1])
        
        self.label = Label(frame,text=':'.join(times),padx=10,pady=10)
        self.label.grid(row=index,column=1)
        
        b = MyButton(frame,text='Edit',key=index,padx=10,pady=2)
        b['command'] = lambda: self.editData(b.key,data,editDialogRef) 
        b.grid(row=index,column=2)

    def editData(self,key,data,editDialogRef):

        currentData = data[key]
        print(currentData)

        keyDate = list(currentData.keys())[0]
        inputDialog = MyDialog(self.top,currentData)
        self.top.wait_window(inputDialog.top)
        if inputDialog.taskVal and inputDialog.ts:
            updateTheListDatabase(keyDate,inputDialog.taskVal,inputDialog.ts)
        
        editDialogRef.top.destroy()

        editedText = inputDialog.taskVal
        editedTime = inputDialog.ts 

        if len(editedText) > MyRowLabel.LABEL_WIDTH:
            editedText = editedText[:MyRowLabel.LABEL_WIDTH-3] + '...'

        times,maxTimes = getTimeMaxTime(editedTime)

        for index,eachMyRowLabelDataArray in enumerate(MyRowLabel.dataHolderArray):
            keyOfThatVal = eachMyRowLabelDataArray[0]
            print(keyOfThatVal,keyDate)
            if keyOfThatVal==keyDate:
                editedRowLabel=  eachMyRowLabelDataArray[1]
                break 
        
        editedRowLabel.editLabel.label['text']= editedText

        editedRowLabel.yearProgressBar['value'] = times[0]
        editedRowLabel.labelYear['text']= "{} years".format(times[0])

        editedRowLabel.monthProgressBar['value'] = times[1]
        editedRowLabel.labelMonth['text']= "{} months".format(times[1])

        editedRowLabel.dayProgressBar['value'] = times[2]
        editedRowLabel.labelDay['text']= "{} days".format(times[2])

        editedRowLabel.hourProgressBar['value'] = times[3]
        editedRowLabel.labelHour['text']= "{} hours".format(times[3])

        editedRowLabel.minuteProgressBar['value'] = times[4]
        editedRowLabel.labelMinute['text']= "{} minutes".format(times[4])

        
class EditDialog():
    def __init__(self,parent): 
        top = self.top = Toplevel(parent)
        frame = Frame(top)
        frame.pack()
        data = getData()

        for index,eachData in enumerate(data):
            for key,val in eachData.items():
                EditRow(frame,val,index,data,self)


