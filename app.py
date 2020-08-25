import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter.ttk import Combobox
import pandas as pd


def import_csv_data():
    global df
    csv_file_path = askopenfilename()
    v.set(csv_file_path)
    df = pd.read_csv(csv_file_path)

def doNothing():
    print("nothing")
    

def DrawGraph():
    _df=df.head(10)
    print(numberChosen.get())
    #figure = Figure(figsize=(8, 5), dpi=100)
    #plot = figure.add_subplot(1, 1, 1)
    #print(df)
    x = _df['DATE']
    y = _df['LTP']
    #plot.plot(x, y, color="blue", marker="x", linestyle="")
    
    fig, ax = plt.subplots(figsize=(10,8))
    lns1 = ax.plot(x,y)
    plt.ylabel('LTP')
    plt.xlabel('Date')

    plt.title('Graph 1')

    plt.legend([lns1],["Bar"], loc="upper right")

    plt.draw()
    plt.show()
    
    #canvas = FigureCanvasTkAgg(figure, root)
    #canvas.get_tk_widget().grid(row=6,column=0,columnspan=3)

root = tk.Tk()
root.title("Stock Market Analysis")
#root.attributes("-fullscreen", True)

tk.Label(root, text='').grid(row=0, column=0)
tk.Label(root, text='File Path').grid(row=1, column=0,columnspan=1)
v = tk.StringVar()
entry = tk.Entry(root, textvariable=v,width=40).grid(row=1, column=1,columnspan=3)
tk.Label(root, text='').grid(row=2, column=0)

tk.Label(root, text='File Name:').grid(row=3, column=0,columnspan=1)
number = tk.StringVar()  
numberChosen = Combobox(root, width = 12, textvariable = number)# Adding Values  
numberChosen['values'] = ("Red", "Blue", "Green")  
numberChosen.grid(column = 1, row = 3,columnspan=1)  
numberChosen.current(0)# Calling Main() 

tk.Label(root, text='').grid(row=4, column=0)

tk.Button(root, text='Browse',command=import_csv_data).grid(row=5, column=0,columnspan=1)
tk.Button(root, text='Close',command=root.destroy).grid(row=5, column=0,columnspan=2)
tk.Button(root, text='Graph 1', command=DrawGraph).grid(row=5, column=1,columnspan=3) 

tk.Label(root, text='').grid(row=6, column=0)
# Call the graph_1 function


#cb.place(x=60, y=50)


#tk.Button(root, text='Graph 2', command=doNothing).grid(row=2, column=1)
#tk.Button(root, text='Graph 3', command=doNothing).grid(row=3, column=2)
#tk.Button(root, text='Graph 4', command=doNothing).grid(row=4, column=3)

root.mainloop()