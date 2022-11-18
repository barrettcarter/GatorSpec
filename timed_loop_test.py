import datetime as dt
import time
from tkinter import (Tk, Frame, Button, Entry, Label)

global timestep
global loop_num

timestep = dt.timedelta(seconds=5)
loop_num = 0

def timed_loop(ON):
    global loop_num
    global timestep
    
    if ON == False:
        print('Loop is OFF')
        #return
#     else:
#     
#         while ON==True:
# 
#             loop_num += 1
#             
#             begin_time = dt.datetime.now()
#             print(f'begin time is {begin_time}')
#             
#             end_time = dt.datetime.now()
#             print(f'end time is {end_time}')
#             
#             time_diff = end_time - begin_time
#             wait_time = timestep.seconds - time_diff.seconds
#             time.sleep(wait_time)
#             print(f'Loop number {loop_num} ended at {dt.datetime.now()}')
            
    while ON==True:

        loop_num += 1
        
        begin_time = dt.datetime.now()
        print(f'begin time is {begin_time}')
        
        end_time = dt.datetime.now()
        print(f'end time is {end_time}')
        
        time_diff = end_time - begin_time
        wait_time = timestep.seconds - time_diff.seconds
        time.sleep(wait_time)
        print(f'Loop number {loop_num} ended at {dt.datetime.now()}')

root = Tk()
root.geometry("400x450")
root.title('Timed Loop')
 
frame = Frame(root)
frame.pack()

loop_ON_Button = Button(frame, text = "Loop ON", command = lambda: timed_loop(ON=True))
loop_ON_Button.pack(padx = 5, pady = 5)

loop_OFF_Button = Button(frame, text = "Loop OFF", command = lambda: timed_loop(ON=False))
loop_OFF_Button.pack(padx = 5, pady = 5)
 
root.mainloop()
