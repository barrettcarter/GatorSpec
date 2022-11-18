import matplotlib.pyplot as plt
from tkinter import (Tk, Frame, Button, Entry, Label)

#### Testing

def plot_1():
    
    x = plot_1_x_entry.get()
    x = x.split(sep=',')
    for i in range(len(x)):
        x[i]=float(x[i])
    
    y = plot_1_y_entry.get()
    y = y.split(sep=',')
    for i in range(len(y)):
        y[i]=float(y[i])
    
    plt.figure(num=1,clear = True)
    plt.title('Plot 1')
    plt.plot(x,y)
    plt.show(block=False)
    
def plot_2():
    
    x = plot_2_x_entry.get()
    x = x.split(sep=',')
    for i in range(len(x)):
        x[i]=float(x[i])
    
    y = plot_2_y_entry.get()
    y = y.split(sep=',')
    for i in range(len(y)):
        y[i]=float(y[i])
    
    plt.figure(num=2,clear = True)
    plt.title('Plot 2')
    plt.plot(x,y)
    plt.show(block=False)

## make GUI

root = Tk()
root.geometry("400x450")
root.title('Live Plots')
 
frame = Frame(root)
frame.pack()

plot_1_x_lab = Label(frame,text ='Plot 1 X-Values')
plot_1_x_lab.pack(padx = 2, pady = 2)
 
plot_1_x_entry = Entry(frame, width = 20)
plot_1_x_entry.insert(0,'1,2')
plot_1_x_entry.pack(padx = 5, pady = 5)

plot_1_y_lab = Label(frame,text ='Plot 1 Y-Values')
plot_1_y_lab.pack(padx = 2, pady = 2)
 
plot_1_y_entry = Entry(frame, width = 20)
plot_1_y_entry.insert(0,'3,4')
plot_1_y_entry.pack(padx = 5, pady = 5)

plot_1_Button = Button(frame, text = "Make Plot 1", command = plot_1)
plot_1_Button.pack(padx = 5, pady = 5)

plot_2_x_lab = Label(frame,text ='Plot 2 X-Values')
plot_2_x_lab.pack(padx = 2, pady = 2)
 
plot_2_x_entry = Entry(frame, width = 20)
plot_2_x_entry.insert(0,'10,20')
plot_2_x_entry.pack(padx = 5, pady = 5)

plot_2_y_lab = Label(frame,text ='Plot 2 Y-Values')
plot_2_y_lab.pack(padx = 2, pady = 2)
 
plot_2_y_entry = Entry(frame, width = 20)
plot_2_y_entry.insert(0,'30,40')
plot_2_y_entry.pack(padx = 5, pady = 5)

plot_2_Button = Button(frame, text = "Make Plot 2", command = plot_2)
plot_2_Button.pack(padx = 5, pady = 5)

root.mainloop()