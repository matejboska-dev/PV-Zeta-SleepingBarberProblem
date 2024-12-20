import queue
import time
from tkinter import *
import threading
from dataclasses import dataclass
from typing import Dict

@dataclass
class Customer:
    id: int
    arrival_time: float
    position: int

class SharedState:
    def __init__(self):
        self.custready = 0
        self.access = 1
        self.noofseats = 4  # Default value, will be updated from environment
        self.total_seats = self.noofseats
        self.come = 0
        self._lock = threading.Lock()
        self.customer_count = 0  # To generate unique customer IDs
        self.waiting_customers: Dict[int, Customer] = {}  # position -> Customer

    def add_customer(self, position: int) -> Customer:
        with self._lock:
            self.customer_count += 1
            customer = Customer(
                id=self.customer_count,
                arrival_time=time.time(),
                position=position
            )
            self.waiting_customers[position] = customer
            return customer

    def remove_customer(self, position: int) -> None:
        with self._lock:
            if position in self.waiting_customers:
                del self.waiting_customers[position]

    def change_custready(self, value):
        with self._lock:
            self.custready = value
            return self.custready

    def change_access(self, value):
        with self._lock:
            self.access = value
            return self.access

state = SharedState()
gui_queue = queue.Queue()

def signal1(s):
    try:
        new_value = state.change_custready(s)
        print(f"Signal1: custready changed to {new_value}")
        state.custready = state.custready + 1
    except Exception as e:
        print(f"Error in signal1: {str(e)}")
        gui_queue.put({'action': 'show_error', 'message': 'An error occurred in signal1.'})

def wait1(s):
    try:
        cnt = 0
        new_value = state.change_custready(s)
        print(f"Wait1: custready set to {new_value}")
        
        if state.custready == 0:
            print("Barber is Sleeping")
            gui_queue.put({'action': 'update_barber', 'state': 'sleeping'})
        while(state.custready <= 0):
            cnt = 1
        if cnt == 1:
            cnt = 0
            print("Barber Wake Up")
            gui_queue.put({'action': 'update_barber', 'state': 'wakeup'})
            time.sleep(1)
            gui_queue.put({'action': 'update_barber', 'state': 'ready'})
        state.custready = state.custready - 1
    except Exception as e:
        print(f"Error in wait1: {str(e)}")
        gui_queue.put({'action': 'show_error', 'message': 'An error occurred in wait1.'})

def signal2(s):
    try:
        new_value = state.change_access(s)
        print(f"Signal2: access changed to {new_value}")
        state.access = state.access + 1
    except Exception as e:
        print(f"Error in signal2: {str(e)}")
        gui_queue.put({'action': 'show_error', 'message': 'An error occurred in signal2.'})

def wait2(s):
    try:
        new_value = state.change_access(s)
        print(f"Wait2: access set to {new_value}")
        while(state.access <= 0):
            pass
        state.access = state.access - 1
    except Exception as e:
        print(f"Error in wait2: {str(e)}")
        gui_queue.put({'action': 'show_error', 'message': 'An error occurred in wait2.'})