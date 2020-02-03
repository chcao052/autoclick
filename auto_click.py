import pyautogui
import time
import tkinter as tk
import threading


class Action:
    def __init__(self, name: str, delay: float):
        self.name, self.delay = name, delay

    def execute(self, verbose=False):
        pass


class MouseAction(Action):
    def __init__(self, name: str, delay: float):
        super().__init__(name, delay)
        if name not in ["left", "middle", "right"]:
            exit("invalid mouse action")

    def execute(self, verbose=False):
        mouse_x, mouse_y = pyautogui.position()
        pyautogui.click(x=mouse_x, y=mouse_y, button=self.name)
        if verbose:
            print("mouse click", self.name, "delay", self.delay)
        time.sleep(self.delay)


class KeyboardAction(Action):
    def __init__(self, name: str, delay: float):
        super().__init__(name, delay)
        if len(name) != 1:
            exit("Invalid keyboard action. Expect 1 key " + name)

    def execute(self, verbose=False):
        mouse_x, mouse_y = pyautogui.position()
        pyautogui.press(self.name, pause=0.1)
        pyautogui.position(mouse_x, mouse_y)
        if verbose:
            print("keyboard", self.name, "delay", self.delay)
        time.sleep(self.delay)


class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack()
        self.mouse_only = False
        self.keys = "ABC"
        self.action_sequence = list()
        self.verbose = True
        self.cps = 8    # Clicks Per Second
        self.is_start = False
        self.is_quit = False
        self.sequence_filename = "auto_click.txt"

        bt_down = tk.Button(self, text="<<", command=self.command_down)
        bt_down.pack(side="left")

        self.cps_label = tk.Label(self, text="%d" % self.cps)
        self.cps_label.pack(side="left")

        bt_up = tk.Button(self, text=">>", command=self.command_up)
        bt_up.pack(side="left")

        self.bt_start = tk.Button(self, text="START", command=self.command_start_stop)
        self.bt_start.pack(side="left")

        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.command_quit)
        self.quit.pack(side="left")

        self.click_thread = threading.Thread(target=self.my_click_thread_function)
        self.click_thread.start()

    def load_auto_click_sequence(self, filename) -> list:
        """
        Support line format:
        m:left:0.1
        m:left
        k: :0.2
        k:ab
        :param filename:
        :return:
        """

        # noinspection PyBroadException
        action_sequence = list()
        with open(filename) as fh:
            for line_num, line in enumerate(fh):
                delay = 1.0 / self.cps  # default delay time
                line = line.strip()
                if line.startswith("#"):
                    continue
                if line.startswith("m:"):
                    arr = line.split(":")
                    if len(arr) > 1 and arr[1] in ["left", "middle", "right"]:
                        if len(arr) > 2:
                            val = arr[2].strip()
                            if len(val):
                                delay = float(arr[2])
                        action_sequence.append(MouseAction(arr[1], delay))
                    else:
                        print("Error at line", line_num, line)
                elif line.startswith("k:"):
                    arr = line.split(":")
                    if len(arr) > 1:
                        if len(arr) > 2:
                            val = arr[2].strip()
                            if len(val):
                                delay = float(arr[2])
                        for key in arr[1]:  # break into individual key
                            action_sequence.append(KeyboardAction(key, delay))
                    else:
                        print("Error at line", line_num, line)
                else:
                    print("Error at line", line_num, line)
        return action_sequence

    def command_quit(self):
        self.is_quit = True
        self.click_thread.join()
        self.master.destroy()

    def command_up(self):

        self.cps = self.cps + 1
        self.set_cps_label()

    def set_cps_label(self):
        self.cps_label.config(text="%d" % self.cps)

    def command_down(self):

        val = self.cps - 1
        if val < 1:
            val = 1
        self.cps = val
        self.set_cps_label()

    def command_start_stop(self):
        self.is_start = not self.is_start

        # top tip show
        if self.is_start:
            self.master.overrideredirect(1)
        else:
            self.master.overrideredirect(0)

        text = "STOP" if self.is_start else "START"
        self.bt_start.config(text=text)

        if self.is_start:
            self.action_sequence = self.load_auto_click_sequence(self.sequence_filename)

    def my_click_thread_function(self):
        was_stop = True
        index = 0
        while True:
            if self.is_quit:
                # print("quit")
                break
            if self.is_start:
                if was_stop:
                    time.sleep(1)       # short delay before starting it
                    was_stop = False
                    index = 0           # reset from the start

                self.action_sequence[index].execute(self.verbose)

                index = (index + 1) % len(self.action_sequence)
            else:
                was_stop = True
                time.sleep(0.4)
                # print("Sleep")


def main():
    root = tk.Tk()
    root.title("CAR Auto clicker")
    # this removes the maximize button
    root.lift()
    root.attributes('-topmost', True)
    # root.resizable(0,0)
    root.attributes("-toolwindow", 1)
    app = Application(master=root)
    app.mainloop()


if __name__ == '__main__':
    main()
