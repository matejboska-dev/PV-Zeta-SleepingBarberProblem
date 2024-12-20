import math
from tkinter import *
from PIL import ImageTk, Image
import queue
import time
from globals import gui_queue, state

class GUI:
    def __init__(self, root):
        self.root = root
        self.images = {}  # Store all PhotoImage objects
        self.chair_width = 150
        self.chair_spacing = 40
        self.chair_height = 150
        self.vertical_spacing = 50
        self.info_tags = []  # Store tags for customer info text
        self.setup_gui()
        self.root.after(100, self.process_queue)
        self.root.after(1000, self.update_waiting_times)  # Update times every second

    def calculate_room_dimensions(self):
        chairs_per_row = self.calculate_chairs_per_row()
        num_rows = math.ceil(state.total_seats / chairs_per_row)
        
        width = (chairs_per_row * (self.chair_width + self.chair_spacing)) + self.chair_spacing * 3
        height = (num_rows * (self.chair_height + self.vertical_spacing)) + self.vertical_spacing * 2 + 300  # Added extra height
        
        return max(590, width), max(530, height)

    def load_images(self):
        image_files = {
            'bg': 'bg.png',
            'sleeping': 'sleepingbarber.png',
            'wakeup': 'wakeupbarber.png',
            'ready': 'readybarber.png',
            'working': 'workingbarber.png',
            'empty_chair': 'emptychair.png',
            'occupied_chair': 'occupiedchair.png',
            'entering': 'entering.png',
            'leaving': 'leaving.png',
            'nospace': 'nospace.png'
        }
        
        for key, filename in image_files.items():
            if key in ['empty_chair', 'occupied_chair']:
                original = Image.open(filename)
                resized = original.resize((self.chair_width, self.chair_height), Image.Resampling.LANCZOS)
                self.images[key] = ImageTk.PhotoImage(resized)
            else:
                self.images[key] = ImageTk.PhotoImage(Image.open(filename))

    def setup_gui(self):
        self.root.title("Sleeping Barber Problem Solution")
        
        waiting_room_width, waiting_room_height = self.calculate_room_dimensions()
        window_width = waiting_room_width + 1000
        window_height = waiting_room_height + 200
        
        self.root.geometry(f"{window_width}x{window_height}")
        self.c = Canvas(self.root, bg='cyan', height=window_height, width=window_width)
        self.c.pack(expand=YES, fill=BOTH)
        
        self.load_images()
        
        self.c.create_image(0, 0, anchor=NW, image=self.images['bg'])
        
        container_width = waiting_room_width + 800
        self.c.create_rectangle(100, 100, 100 + container_width, 100 + waiting_room_height, fill='white')
        
        self.c.create_rectangle(110, 110, 500, 90 + waiting_room_height, fill='white')
        
        waiting_room_x = 510
        self.c.create_rectangle(waiting_room_x, 110, waiting_room_x + waiting_room_width, 90 + waiting_room_height, fill='white')
        
        entry_door_x = waiting_room_x + waiting_room_width + 10
        self.c.create_rectangle(entry_door_x, 110, entry_door_x + 280, 90 + waiting_room_height, fill='white')
        
        fnt = ('Times', 28, 'bold', 'underline')
        self.c.create_text(500, 50, text="SLEEPING BARBER PROBLEM SOLUTION . . .", font=fnt, fill='BLACK')
        self.c.create_text(300, 150, text="MAIN ROOM", font=fnt, fill='black')
        self.c.create_text(waiting_room_x + waiting_room_width/2, 150, text="WAITING ROOM", font=fnt, fill='black')
        self.c.create_text(entry_door_x + 140, 150, text="ENTRY DOOR", font=fnt, fill='black')
        
        fnt = ('Times', 30, 'bold')
        b1 = Button(self.c, text="ENTER", font=fnt, command=self.button_click)
        b1.place(x=waiting_room_x + waiting_room_width/2 - 100, y=waiting_room_height + 120, width=200, height=70)
        
        self.update_barber_state('sleeping')
        self.update_chairs(0)

    def calculate_chairs_per_row(self):
        if state.total_seats <= 3:
            return state.total_seats
        elif state.total_seats <= 6:
            return 3
        else:
            return 4

    def button_click(self):
        state.come = 1
        print("Button clicked, come =", state.come)

    def update_barber_state(self, state_name):
        image_key = {
            'sleeping': 'sleeping',
            'wakeup': 'wakeup',
            'ready': 'ready',
            'working': 'working'
        }.get(state_name)
        
        if image_key:
            self.c.create_image(170, 230, anchor=NW, image=self.images[image_key])

    def format_waiting_time(self, seconds: float) -> str:
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"

    def update_waiting_times(self):
        """Update the waiting time display for all customers"""
        current_time = time.time()
        
        # Update each customer's waiting time
        for tag in self.info_tags:
            self.c.delete(tag)
        self.info_tags.clear()

        for position, customer in state.waiting_customers.items():
            waiting_time = current_time - customer.arrival_time
            formatted_time = self.format_waiting_time(waiting_time)
            info_text = f"#{customer.id}\n{formatted_time}"
            
            # Calculate position for the text (above the chair)
            chairs_per_row = self.calculate_chairs_per_row()
            row = position // chairs_per_row
            col = position % chairs_per_row
            
            x = 480 + (col * (self.chair_width + self.chair_spacing)) + self.chair_width/2
            y = 250 + (row * (self.chair_height + self.vertical_spacing)) - 30  # Updated y-position
            
            # Create text with shadow for better visibility
            shadow_tag = f"info_shadow_{position}"
            text_tag = f"info_text_{position}"
            
            self.c.create_text(x+1, y+1, text=info_text, fill='black', 
                             font=('Arial', 12, 'bold'), anchor='center',
                             tags=shadow_tag)
            self.c.create_text(x, y, text=info_text, fill='white', 
                             font=('Arial', 12, 'bold'), anchor='center',
                             tags=text_tag)
            
            self.info_tags.extend([shadow_tag, text_tag])

        self.root.after(1000, self.update_waiting_times)

    def update_chairs(self, occupied_count):
        chairs_per_row = self.calculate_chairs_per_row()
        
        start_x = 480
        start_y = 250  # Updated starting y-position
        
        self.c.delete('chair')
        
        # Clear old customer info
        for tag in self.info_tags:
            self.c.delete(tag)
        self.info_tags.clear()
        
        for i in range(state.total_seats):
            row = i // chairs_per_row
            col = i % chairs_per_row
            
            x = start_x + (col * (self.chair_width + self.chair_spacing))
            y = start_y + (row * (self.chair_height + self.vertical_spacing))
            
            if i < occupied_count:
                # Add a new customer if not already tracked
                if i not in state.waiting_customers:
                    state.add_customer(i)
                img = self.images['occupied_chair']
            else:
                # Remove customer if chair becomes empty
                state.remove_customer(i)
                img = self.images['empty_chair']
                
            self.c.create_image(x, y, anchor=NW, image=img, tags='chair')

    def process_queue(self):
        try:
            while True:
                message = gui_queue.get_nowait()
                action = message.get('action')
                if action == 'update_barber':
                    self.update_barber_state(message['state'])
                elif action == 'update_chairs':
                    self.update_chairs(message.get('occupied', 0))
                elif action == 'show_entering':
                    waiting_room_width, _ = self.calculate_room_dimensions()
                    entry_x = 520 + waiting_room_width + 10
                    self.c.create_image(entry_x, 250, anchor=NW, image=self.images['entering'], tags='temp')
                    self.root.after(1000, lambda: self.c.delete('temp'))
                elif action == 'show_nospace':
                    waiting_room_width, _ = self.calculate_room_dimensions()
                    entry_x = 520 + waiting_room_width + 10
                    self.c.create_image(entry_x, 250, anchor=NW, image=self.images['nospace'], tags='temp')
                    self.root.after(500, lambda: self.c.delete('temp'))
                elif action == 'show_leaving':
                    waiting_room_width, _ = self.calculate_room_dimensions()
                    entry_x = 520 + waiting_room_width + 10
                    self.c.create_image(entry_x, 250, anchor=NW, image=self.images['leaving'], tags='temp')
                    self.root.after(1000, lambda: self.c.delete('temp'))
        except queue.Empty:
            pass
        self.root.after(100, self.process_queue)