import unittest
from unittest.mock import patch
from threading import Thread
from queue import Queue
from time import sleep

from globals import SharedState, gui_queue
from barber import Barber
from customer import Customer

class TestBarberShopAdvanced(unittest.TestCase):
    """
    Advanced unit test class for the Sleeping Barber Problem simulation.

    This class contains additional test methods to verify the behavior of the simulation
    under various scenarios, such as multiple customers and GUI interactions.
    """

    def setUp(self):
        """
        Set up the test environment before each test method runs.

        This method initializes the shared state, barber, customer, and GUI queue objects
        that will be used in the test methods.
        """
        self.state = SharedState()
        self.barber = Barber()
        self.customer = Customer()
        self.gui_queue = gui_queue

    def test_multiple_customers(self):
        """
        Test the simulation with multiple customers.

        This test verifies that the simulation can handle multiple customers correctly,
        ensuring that the waiting list and seat availability are updated accurately.
        """
        num_customers = 3
        for i in range(num_customers):
            self.state.add_customer(i)
        self.assertEqual(self.state.customer_count, num_customers)
        self.assertEqual(len(self.state.waiting_customers), num_customers)
        self.assertEqual(self.state.noofseats, self.state.total_seats - num_customers)

    def test_customer_leaves_when_no_seats(self):
        """
        Test the scenario when a customer leaves due to no available seats.

        This test verifies that when all seats are occupied and a new customer arrives,
        the customer leaves without being added to the waiting list.
        """
        self.state.noofseats = 0
        self.state.come = 1

        customer_thread = Thread(target=self.customer.run)
        customer_thread.daemon = True
        customer_thread.start()

        sleep(0.5)  # Wait for the customer thread to run

        self.assertEqual(self.state.come, 0)
        self.assertEqual(self.state.noofseats, 0)
        self.assertEqual(self.state.customer_count, 0)

    @patch('barber.gui_queue.put')
    def test_barber_gui_interactions(self, mock_gui_queue_put):
        """
        Test the barber's interactions with the GUI.

        This test verifies that the barber sends the correct messages to the GUI queue
        during different stages of the simulation, such as when the barber is sleeping,
        cutting hair, or when a customer enters the main room.
        """
        self.state.custready = 0
        self.state.access = 1
        self.state.noofseats = 3

        barber_thread = Thread(target=self.barber.run)
        barber_thread.daemon = True
        barber_thread.start()

        sleep(0.5)  # Wait for the barber thread to run

        mock_gui_queue_put.assert_any_call({'action': 'update_barber', 'state': 'sleeping'})
        mock_gui_queue_put.assert_any_call({'action': 'update_chairs', 'occupied': 1})
        mock_gui_queue_put.assert_any_call({'action': 'update_barber', 'state': 'working'})
        mock_gui_queue_put.assert_any_call({'action': 'update_barber', 'state': 'ready'})

    @patch('customer.gui_queue.put')
    def test_customer_gui_interactions(self, mock_gui_queue_put):
        """
        Test the customer's interactions with the GUI.

        This test verifies that the customer sends the correct messages to the GUI queue
        during different stages of the simulation, such as when the customer enters the
        waiting room or leaves due to no available seats.
        """
        self.state.come = 1
        self.state.noofseats = 1

        customer_thread = Thread(target=self.customer.run)
        customer_thread.daemon = True
        customer_thread.start()

        sleep(0.5)  # Wait for the customer thread to run

        mock_gui_queue_put.assert_any_call({'action': 'show_entering'})
        mock_gui_queue_put.assert_any_call({'action': 'update_chairs', 'occupied': 1})

        self.state.come = 1
        self.state.noofseats = 0

        customer_thread = Thread(target=self.customer.run)
        customer_thread.daemon = True
        customer_thread.start()

        sleep(0.5)  # Wait for the customer thread to run

        mock_gui_queue_put.assert_any_call({'action': 'show_nospace'})
        mock_gui_queue_put.assert_any_call({'action': 'show_leaving'})

if __name__ == '__main__':
    unittest.main()