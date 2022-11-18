import datetime
from time import sleep
from tkinter import (Tk, Frame, Button, Entry, Label)

#global timestep
# global loop_num
# global wait_time
# global loop_ON

dt = datetime

timestep = dt.timedelta(seconds=5)
loop_num = 0
#wait_time = 0
loop_is_ON = False
begin_time = dt.datetime.now()
current_loop_time = 0

def loop_OFF():
    global loop_num
    global loop_is_ON
    #global current_loop_time
    loop_num = 0
    loop_is_ON = False
    #current_loop_time = 0
    print(f'Loop turned OFF at {dt.datetime.now()}')
    

def loop_ON():
    global loop_is_ON
    #global current_loop_time
    global loop_num
    loop_num = 0
    loop_is_ON = True
    #current_loop_time = 0
    #on_time = dt.datetime.now()
    print(f'Loop turned ON at {dt.datetime.now()}')
    
def timed_loop():
    
    global loop_num
    global timestep
    global current_loop_time
    global begin_time
    #print(f'loop is on? {loop_is_ON}')
    
    #print(f'begin time is {begin_time}')
    
    if loop_is_ON:

        #print(f'Loop has been running for {loop_num} cycles')
        
        print('flushing system (2s)')
        sleep(2)
        
        #begin_time = dt.datetime.now()
        #print(f'begin time is {begin_time}')
        
        
        #print(f'end time is {end_time}')
        
        
        
        print(f'Loop {loop_num} running for {current_loop_time} seconds.')
        #wait_time = timestep.seconds - time_diff.seconds
        #time.sleep(wait_time)
        if current_loop_time > timestep.seconds:
            loop_num += 1
            print(f'Loop {loop_num-1} has ended. Moving on to Loop {loop_num}')
            print('Performing sample analysis sequence')
            current_loop_time = 0
    
    if loop_is_ON==False:
        print(f'Loop off for {current_loop_time} seconds.')
    
    end_time = dt.datetime.now()
    time_diff = end_time - begin_time
    current_loop_time += time_diff.seconds
    begin_time = dt.datetime.now()
    
    root.after(1000,timed_loop)
        

root = Tk()
root.geometry("400x450")
root.title('Timed Loop')
 
frame = Frame(root)
frame.pack()

loop_ON_Button = Button(frame, text = "Loop ON", command = loop_ON)
loop_ON_Button.pack(padx = 5, pady = 5)

loop_OFF_Button = Button(frame, text = "Loop OFF", command = loop_OFF)
loop_OFF_Button.pack(padx = 5, pady = 5)

root.after(1000,timed_loop)
 
root.mainloop()
