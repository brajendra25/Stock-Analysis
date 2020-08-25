#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 10:18:21 2020

@author: brajendra
"""

import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter.ttk import Combobox
from tkinter.filedialog import askopenfilename

class Application(tk.Frame):
    global df
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()
        self._dirPath = "/home/brajendra/dev/StockMarket/ProcessedFiles/"
        df = pd.DataFrame();

    def import_csv_data(self):
        csv_file_path = askopenfilename()
        self.v.set(csv_file_path)
        df = pd.read_csv(csv_file_path)
    
    def doNothing(self):
        print("nothing")



    def create_widgets(self):
        tk.Label(root, text='',bg='black', fg='white').grid(row=0, column=0)
        tk.Label(root, text='File Path',bg='black', fg='white').grid(row=1, column=0,columnspan=1)
        self.v = tk.StringVar()
        self.entry = tk.Entry(root, textvariable=self.v,width=40,state='disabled').grid(row=1, column=1,columnspan=3)
        tk.Label(root, text='',bg='black', fg='white').grid(row=2, column=0)
        
        tk.Label(root, text='Share Name:',bg='black', fg='white').grid(row=3, column=0,columnspan=1)
        self.number = tk.StringVar()  
        self.numberChosen = Combobox(root, width = 12, textvariable = self.number)# Adding Values  
        self.numberChosen['values'] = ("--Select--" , "AXISBANK", "AXISGOLD", "GOLDBEES","ICICIGOLD", "IDEA", "PNB","YESBANK")  
        self.numberChosen.grid(column = 1, row = 3,columnspan=1)  
        self.numberChosen.current(0)# Calling Main() 
        
        tk.Label(root, text='Select Year:',bg='black', fg='white').grid(row=3, column=3,columnspan=1)
        self.year = tk.StringVar()  
        self.yearChosen = Combobox(root, width = 12, textvariable = self.year)# Adding Values  
        self.yearChosen['values'] = ("--Select--" , "2020", "2019")  
        self.yearChosen.grid(column = 4, row = 3,columnspan=1)  
        self.yearChosen.current(0)# Calling Main() 
        
        tk.Label(root, text='Select Months:',bg='black', fg='white').grid(row=3, column=6,columnspan=1)
        self.month = tk.StringVar()  
        self.monthChosen = Combobox(root, width = 12, textvariable = self.month)# Adding Values  
        self.monthChosen['values'] = ("--Select--" , "01", "02","03","04","05","06","07","08","09","10","11","12")  
        self.monthChosen.grid(column = 7, row = 3,columnspan=1)  
        self.monthChosen.current(0)# Calling Main()
        
        tk.Label(root, text='',bg='black', fg='white').grid(row=4, column=0)
        
        tk.Label(root, text='X Name:',bg='black', fg='white').grid(row=5, column=0,columnspan=1)
        self.X = tk.StringVar()  
        self.XChosen = Combobox(root, width = 12, textvariable = self.X)# Adding Values  
        self.XChosen['values'] = ( "--Select--" ,"DATE" ,"LTP", "OPEN", "LOW","HIGH", "CLOSE", "VALUE","NO_OF_TRADES")  
        self.XChosen.grid(column = 1, row = 5,columnspan=1)  
        self.XChosen.current(0)# Calling Main() 
        
        tk.Label(root, text='Y Name:',bg='black', fg='white').grid(row=6, column=0,columnspan=1)
        self.Y = tk.StringVar()  
        self.YChosen = Combobox(root, width = 12, textvariable = self.Y)# Adding Values  
        self.YChosen['values'] = ("--Select--","DATE" ,"LTP", "OPEN", "LOW","HIGH", "CLOSE", "VALUE","NO_OF_TRADES")  
        self.YChosen.grid(column = 1, row = 6,columnspan=1)  
        self.YChosen.current(0)# Calling Main() 
        tk.Label(root, text='',bg='black', fg='white').grid(row=7, column=0)
        
        tk.Button(root, text='Browse',command=self.import_csv_data,bg='black', fg='white').grid(row=8, column=0,columnspan=1)
        tk.Button(root, text='Close',command=root.destroy,bg='black', fg='white').grid(row=8, column=1,columnspan=4)
        tk.Button(root, text='Graph', command=self.GraphAnalysis,bg='black', fg='white').grid(row=8, column=0,columnspan=3) 
        
        tk.Label(root, text='',bg='black', fg='white').grid(row=9, column=0)

    def say_hi(self):
        print("hi there, everyone!")
    
    def BreakDateColumns(self, _data,year,month):
        _data['DATE'] = pd.to_datetime(_data.DATE)
        _df = pd.DataFrame(_data)
        _year = _df['DATE'].dt.strftime('%Y')
        _month = _df['DATE'].dt.strftime('%m')
        _data["YEAR"] = _year
        _data['MONTH'] = _month
        _dataFilter = _data
        if year != "--Select--":
             _dataFilter = _data.loc[lambda x: x['YEAR'] == year]
        if month != "--Select--":
             _dataFilter = _dataFilter[_dataFilter.MONTH==month]
        #_dataFilter = _data.mask(lambda x: x['YEAR'] == year).mask(lambda x: x['Months'] == month)
        return _dataFilter
        
        

    def FileProcessing(self,_data):
        _data['DATE'] = pd.to_datetime(_data.DATE)
        _data.sort_values(by=['DATE'], inplace=True, ascending=True)

        _data = _data.drop_duplicates()
        _data = _data.dropna()
        _data = _data.apply(lambda x: x.str.lstrip() if x.dtype == "object" else x)
        _data.columns = _data.columns.str.upper()
        _data.columns = _data.columns.str.rstrip()
        _data.columns = _data.columns.str.replace(' ','_')
        _data.columns = _data.columns.str.replace('.','')
        return _data
    
    def GraphAnalysis(self):
        _fileName =  self.numberChosen.get()
        xAxis = self.X.get()
        yAxis = self.Y.get()
        _selectedYear = self.year.get()
        _selectedMonth = self.month.get()
        _data = pd.read_csv(self._dirPath + _fileName + ".csv")
        '''
        if df.empty:
            _data = pd.read_csv(self._dirPath + _fileName + ".csv")
        else:
            _data = df'''
        _data = self.FileProcessing(_data)
        _dataFinal = self.BreakDateColumns(_data,_selectedYear,_selectedMonth)
        
        fig, ax = plt.subplots(figsize=(16,5))
        # Add x-axis and y-axis
        ax.plot(_dataFinal[xAxis],
                _dataFinal[yAxis])
        # Set title and labels for axes
        ax.set(xlabel=xAxis,
               ylabel=yAxis,
               title="Daily Shares Pricing for "+_fileName + ":)")
        
        plt.show()

root = tk.Tk()
root.title("Stock Analysis")
# setting the minimum size of the root window 
root.minsize(800, 200) 
root.configure(background='black')
app = Application(master=root)
app.mainloop()