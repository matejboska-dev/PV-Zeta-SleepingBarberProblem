from tkinter import *
import os
from gui import GUI
from barber import Barber
from customer import Customer
from globals import state

def main():
    # Set the number of seats from environment variable
    state.noofseats = int(os.environ.get('WAITING_ROOM_CHAIRS', 4))
    state.total_seats = state.noofseats

    root = Tk()
    gui = GUI(root)
    
    b = Barber()
    c = Customer()
    
    b.start()
    c.start()
    
    root.mainloop()

if __name__ == "__main__":
    main()