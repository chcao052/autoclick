import pyautogui
import time
import tkinter as tk
import threading


is_quit = False
is_start = False
cps = 5

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        

    def create_widgets(self):
        self.bt_down = tk.Button(self, text="<<", command=self.command_down)
        self.bt_down.pack(side="left")

        self.cps_label = tk.Label(self, text="%d" %cps)
        self.cps_label.pack(side="left")
        
        self.bt_up = tk.Button(self, text=">>", command=self.command_up)
        self.bt_up.pack(side="left")

        self.bt_start = tk.Button(self, text="START", command=self.command_start_stop)
        self.bt_start.pack(side="left")

        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.command_quit)
        self.quit.pack(side="left")
        
        self.click_thread = threading.Thread(target=self.my_click_function)
        self.click_thread.start()

    def command_quit(self):
        global is_quit
        is_quit = True
        self.click_thread.join()
        self.master.destroy()

    def command_up(self):
        global cps
        cps = cps + 1
        self.set_cps_label()

    def set_cps_label(self):
        global cps
        self.cps_label.config(text="%d" % cps)
        

    def command_down(self):
        global cps
        val = cps - 1
        if val < 1:
            val = 1
        cps = val
        self.set_cps_label()
        
    def command_start_stop(self):
        global is_start
        is_start = not is_start
        if is_start:
            root.overrideredirect(1)
        else:
            root.overrideredirect(0)
        text = "STOP" if is_start else "START"
        self.bt_start.config(text=text)
        
        
    def my_click_function(self):
        global is_quit, is_start, cps
        was_stop = True
        while True:
            if is_quit:
                # print("quit")
                break
            if is_start:
                if was_stop: 
                    time.sleep(1) # short delay before starting it
                    was_stop = False
                moveToX, moveToY = pyautogui.position()
                pyautogui.click(x=moveToX, y=moveToY, button='left')
                delay = 1 / cps
                # print("Click", delay)
                time.sleep(delay)                
            else:
                was_stop = True
                time.sleep(0.4)
                # print("Sleep")

            

root = tk.Tk()

root.title("CAR Auto clicker")
# this removes the maximize button
root.lift()
root.attributes('-topmost', True)
# root.resizable(0,0)
root.attributes("-toolwindow",1)
app = Application(master=root)
app.mainloop()
