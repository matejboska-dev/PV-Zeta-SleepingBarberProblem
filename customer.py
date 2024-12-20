from threading import Thread
import time
from globals import signal1, gui_queue, state

class Customer(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
    
    def run(self):
        while True:
            try:
                if state.come == 1:
                    print("Customer detected come signal")
                    print("Current state: noofseats =", state.noofseats, "custready =", state.custready)
                    state.come = 0
                    gui_queue.put({'action': 'show_entering'})
                    time.sleep(1)
                    
                    if state.noofseats > 0:
                        print("Customer Enters into Waiting Room")
                        state.noofseats = state.noofseats - 1
                        signal1(state.custready)
                        gui_queue.put({
                            'action': 'update_semaphore',
                            'semaphore_type': 'customer',
                            'value': state.custready
                        })
                        gui_queue.put({'action': 'update_chairs', 'occupied': state.total_seats - state.noofseats})
                        time.sleep(1)
                    elif state.noofseats == 0:
                        gui_queue.put({
                            'action': 'update_semaphore',
                            'semaphore_type': 'mutex',
                            'value': 0
                        })
                        gui_queue.put({'action': 'show_nospace'})
                        time.sleep(0.5)
                        gui_queue.put({'action': 'show_leaving'})
                        time.sleep(1)
                        gui_queue.put({
                            'action': 'update_semaphore',
                            'semaphore_type': 'mutex',
                            'value': 1
                        })
                        print("Customer Enters But There is No Space, Customer Leaves")
            except Exception as e:
                print(f"Error in Customer thread: {str(e)}")
                gui_queue.put({'action': 'show_error', 'message': 'An error occurred in the Customer thread.'})
            time.sleep(0.1)