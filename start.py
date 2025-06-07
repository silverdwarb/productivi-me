import time
import msvcrt
import sys
import select

class Stopwatch:
    def __init__(self):
        self.start_time = None
        self.elapsed_time = None
        self.isrunning = False

    def start(self):
        if not self.isrunning:
            self.start_time = time.time()
            self.isrunning = True
            print("Stopwatch has started")
        

    def stop(self):
        if self.isrunning:
            self.elapsed_time = time.time() - self.start_time
            self.isrunning = False
            print ("Stopwatch has stopped")

    def reset(self):
        self.elapsed_time = 0
        self.isrunning = False
        print( "Stopwatch has been reset")

    def logwatchtime(self):
        totaltime = self.elapsed_time
        if self.isrunning:
            return self.elapsed_time
        return self.elapsed_time + (time.time() - self.start_time)
        print(f"Total time: {totaltime:.2f} seconds", end="", flush=True)

stopwatch = Stopwatch()

while True:
    command = input("please enter one of the commands ... \nstart\nstop\nreset\nquit\n\n>")
    if (command == "start"):
        stopwatch.start()
    elif (command == "stop"):
        stopwatch.stop()
    elif (command == "reset"):
        stopwatch.reset()
    elif (command == "quit"):
        break
    else:
        print("Invalid command. Please try again.")

    while stopwatch.isrunning:
    # Platform-specific input detection
        if sys.platform == 'win32':
            # Windows: use msvcrt for keyboard input
            if msvcrt.kbhit():
                # Clear the input buffer to avoid leftover keypresses
                while msvcrt.kbhit():
                    msvcrt.getch()
                break
        else:
            # Unix-like (Linux/macOS): use select.select()
            if select.select([sys.stdin], [], [], 0)[0]:
                break

    # Log time every second
    stopwatch.logwatchtime()
    time.sleep(0.1)