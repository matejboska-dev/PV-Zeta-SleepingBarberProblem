from threading import Thread
import time
from globals import wait1, wait2, signal2, gui_queue, state

class Barber(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True

    def run(self):
        while True:
            try:
                print("Barber state: custready =", state.custready, "access =", state.access)
                wait1(state.custready)
                wait2(state.access)
                
                next_position, next_customer = state.get_next_customer()
                if next_customer:
                    print(f"Serving customer #{next_customer.id} who has been waiting for {time.time() - next_customer.arrival_time:.1f} seconds")
                    state.remove_customer(next_position)
                
                time.sleep(0.2)
                print("Customer Enters into Main Room")
                gui_queue.put({'action': 'update_chairs', 'occupied': max(0, state.total_seats - state.noofseats - 1)})
                time.sleep(1)        
                state.noofseats = state.noofseats + 1
                print("started cutting")
                gui_queue.put({'action': 'update_barber', 'state': 'working'})
                gui_queue.put({
                    'action': 'update_semaphore',
                    'semaphore_type': 'barber',
                    'value': 1
                })
                
                time.sleep(10)
                print("Cutting complete")
                gui_queue.put({'action': 'update_barber', 'state': 'ready'})
                gui_queue.put({
                    'action': 'update_semaphore',
                    'semaphore_type': 'barber',
                    'value': 0
                })
                
                time.sleep(1)
                gui_queue.put({'action': 'update_chairs', 'occupied': max(0, state.total_seats - state.noofseats)})
                signal2(state.access)
            except Exception as e:
                print(f"Error in Barber thread: {str(e)}")
                gui_queue.put({'action': 'show_error', 'message': 'An error occurred in the Barber thread.'})
            time.sleep(0.1)