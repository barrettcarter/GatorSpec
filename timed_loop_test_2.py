import datetime
from time import sleep
from tkinter import (Tk, Frame, Button, Entry, Label, Message, StringVar)

#global timestep
# global loop_num
# global wait_time
# global loop_ON

dt = datetime

timestep = dt.timedelta(seconds=10)
loop_num = 0
#wait_time = 0
loop_is_ON = False
begin_time = dt.datetime.now()
current_loop_time = 0

system_status = f'System turned on at {dt.datetime.now()}'


def loop_OFF():
    global loop_num
    global loop_is_ON
    global loop_off_time
    global system_status
    #global current_loop_time
    loop_num = 0
    loop_is_ON = False
    #current_loop_time = 0
    loop_off_time = dt.datetime.now()
    print(f'Loop turned OFF at {dt.datetime.now()}')
    system_status.set(f'Loop turned OFF at {loop_off_time}.')
    

def loop_ON():
    global loop_is_ON
    #global current_loop_time
    global loop_num
    loop_num = 0
    loop_is_ON = True
    #current_loop_time = 0
    loop_on_time = dt.datetime.now()
    print(f'Loop turned ON at {dt.datetime.now()}')
    system_status.set(f'Loop turned ON at {loop_on_time}.')
    
def timed_loop():
    
    global loop_num
    global timestep
    global current_loop_time
    global begin_time
    global system_status
    global loop_off_time
    #print(f'loop is on? {loop_is_ON}')
    
    #print(f'begin time is {begin_time}')
    
    Switch = switch_entry.get()
    
    if loop_is_ON and Switch == 'ON':

        #print(f'Loop has been running for {loop_num} cycles')
        
        #print('flushing system (2s)')
        sleep(2)
        system_status.set('flushing system (2s)')
        
        #begin_time = dt.datetime.now()
        #print(f'begin time is {begin_time}')
        
        
        #print(f'end time is {end_time}')
        
        
        
        #print(f'Loop {loop_num} running for {current_loop_time} seconds.')
        system_status.set(f'Loop {loop_num} running for {current_loop_time} seconds.')
        #wait_time = timestep.seconds - time_diff.seconds
        #time.sleep(wait_time)
        if current_loop_time > timestep.seconds:
            loop_num += 1
            print(f'Loop {loop_num-1} has ended. Moving on to Loop {loop_num}')
            print('Performing sample analysis sequence')
            system_status.set(f'sample analyzed at {dt.datetime.now()}')
            current_loop_time = 0
    
    if loop_is_ON==False:
        print(f'Loop off for {current_loop_time} seconds.')
        system_status.set(f'Loop OFF for {current_loop_time} seconds.')
    
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

switch_lab = Label(frame,text ='Virtual Switch')
switch_lab.pack(padx = 2, pady = 2)
 
switch_entry = Entry(frame, width = 20)
switch_entry.insert(0,'OFF')
switch_entry.pack(padx = 5, pady = 5)

system_status = StringVar(value = system_status)

sample_name_msg = Message(frame,text =f'System Status:',textvariable = system_status)
sample_name_msg.pack(padx = 2, pady = 2)

root.update()

root.after(1000,timed_loop)
 
root.mainloop()
