import queue
import time
from tkinter import *
import threading
from dataclasses import dataclass
from typing import Dict
from operator import attrgetter

@dataclass
class Customer:
    id: int
    arrival_time: float
    position: int

class SharedState:
    def __init__(self):
        self.custready = 0
        self.access = 1
        self.noofseats = 4
        self.total_seats = self.noofseats
        self.come = 0
        self._lock = threading.Lock()
        self.waiting_customers: Dict[int, Customer] = {}

    def add_customer(self, position: int) -> Customer:
        with self._lock:
            occupied_ids = set(cust.id for cust in self.waiting_customers.values())
            new_id = 1
            while new_id in occupied_ids:
                new_id += 1
                
            customer = Customer(
                id=new_id,
                arrival_time=time.time(),
                position=position
            )
            self.waiting_customers[position] = customer
            return customer

    def get_next_customer(self) -> tuple[int, Customer]:
        with self._lock:
            if not self.waiting_customers:
                return -1, None
            longest_waiting_pos = min(
                self.waiting_customers.items(),
                key=lambda x: x[1].arrival_time
            )
            return longest_waiting_pos

    def remove_customer(self, position: int) -> None:
        with self._lock:
            if position in self.waiting_customers:
                del self.waiting_customers[position]
                sorted_positions = sorted(self.waiting_customers.keys())
                for i, pos in enumerate(sorted_positions, 1):
                    self.waiting_customers[pos].id = i

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
        gui_queue.put({
            'action': 'update_semaphore',
            'semaphore_type': 'customer',
            'value': state.custready
        })
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
        gui_queue.put({
            'action': 'update_semaphore',
            'semaphore_type': 'customer',
            'value': state.custready
        })
    except Exception as e:
        print(f"Error in wait1: {str(e)}")
        gui_queue.put({'action': 'show_error', 'message': 'An error occurred in wait1.'})

def signal2(s):
    try:
        new_value = state.change_access(s)
        print(f"Signal2: access changed to {new_value}")
        state.access = state.access + 1
        gui_queue.put({
            'action': 'update_semaphore',
            'semaphore_type': 'mutex',
            'value': state.access
        })
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
        gui_queue.put({
            'action': 'update_semaphore',
            'semaphore_type': 'mutex',
            'value': state.access
        })
    except Exception as e:
        print(f"Error in wait2: {str(e)}")
        gui_queue.put({'action': 'show_error', 'message': 'An error occurred in wait2.'})
