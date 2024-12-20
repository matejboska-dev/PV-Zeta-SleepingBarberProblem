import unittest
from unittest.mock import patch
from threading import Thread
from queue import Queue
from time import sleep

from globals import SharedState, signal1, wait1, signal2, wait2
from barber import Barber
from customer import Customer

class TestBarberShop(unittest.TestCase):
    """
    Unit test class for the Sleeping Barber Problem simulation.

    This class contains test methods to verify the behavior of various components
    in the simulation, including the shared state, barber, and customer classes.
    """

    def setUp(self):
        """
        Set up the test environment before each test method runs.

        This method initializes the shared state, barber, and customer objects
        that will be used in the test methods.
        """
        self.state = SharedState()
        self.barber = Barber()
        self.customer = Customer()

    def test_shared_state_initialization(self):
        """
        Test the initialization of the SharedState object.

        This test verifies that the SharedState object is initialized correctly
        with the expected default values.
        """
        self.assertEqual(self.state.custready, 0)
        self.assertEqual(self.state.access, 1)
        self.assertEqual(self.state.noofseats, 4)
        self.assertEqual(self.state.total_seats, 4)
        self.assertEqual(self.state.come, 0)
        self.assertEqual(self.state.customer_count, 0)
        self.assertEqual(self.state.waiting_customers, {})

    def test_add_customer(self):
        """
        Test the add_customer method of the SharedState object.

        This test ensures that a new customer is added correctly to the waiting list
        and the customer count is incremented.
        """
        customer = self.state.add_customer(0)
        self.assertEqual(self.state.customer_count, 1)
        self.assertEqual(customer.id, 1)
        self.assertEqual(customer.position, 0)
        self.assertIn(0, self.state.waiting_customers)

    def test_remove_customer(self):
        """
        Test the remove_customer method of the SharedState object.

        This test verifies that a customer is removed correctly from the waiting list
        when the remove_customer method is called.
        """
        self.state.add_customer(0)
        self.state.remove_customer(0)
        self.assertEqual(self.state.customer_count, 1)
        self.assertNotIn(0, self.state.waiting_customers)

    def test_change_custready(self):
        """
        Test the change_custready method of the SharedState object.

        This test ensures that the custready attribute is updated correctly
        when the change_custready method is called.
        """
        self.state.change_custready(1)
        self.assertEqual(self.state.custready, 1)

    def test_change_access(self):
        """
        Test the change_access method of the SharedState object.

        This test ensures that the access attribute is updated correctly
        when the change_access method is called.
        """
        self.state.change_access(0)
        self.assertEqual(self.state.access, 0)

    def test_signal1(self):
        """
        Test the signal1 function.

        This test verifies that the custready attribute is incremented correctly
        when the signal1 function is called.
        """
        signal1(0)
        self.assertEqual(self.state.custready, 1)

    def test_wait1(self):
        """
        Test the wait1 function.

        This test verifies that the custready attribute is decremented correctly
        when the wait1 function is called.
        """
        wait1(0)
        self.assertEqual(self.state.custready, -1)

    def test_signal2(self):
        """
        Test the signal2 function.

        This test verifies that the access attribute is incremented correctly
        when the signal2 function is called.
        """
        signal2(0)
        self.assertEqual(self.state.access, 1)

    def test_wait2(self):
        """
        Test the wait2 function.

        This test verifies that the access attribute is decremented correctly
        when the wait2 function is called.
        """
        wait2(0)
        self.assertEqual(self.state.access, -1)

    @patch('barber.time.sleep', return_value=None)
    def test_barber_run(self, mock_sleep):
        """
        Test the run method of the Barber class.

        This test verifies the behavior of the barber thread by mocking the time.sleep function
        to avoid actual delays during testing. It checks that the noofseats and access attributes
        are updated correctly after the barber thread runs.
        """
        self.state.custready = 1
        self.state.access = 1
        self.state.noofseats = 3

        barber_thread = Thread(target=self.barber.run)
        barber_thread.daemon = True
        barber_thread.start()

        sleep(0.5)  # Wait for the barber thread to run

        self.assertEqual(self.state.noofseats, 4)
        self.assertEqual(self.state.access, 1)

    @patch('customer.time.sleep', return_value=None)
    def test_customer_run(self, mock_sleep):
        """
        Test the run method of the Customer class.

        This test verifies the behavior of the customer thread by mocking the time.sleep function
        to avoid actual delays during testing. It checks that the come and noofseats attributes
        are updated correctly after the customer thread runs.
        """
        self.state.come = 1
        self.state.noofseats = 3

        customer_thread = Thread(target=self.customer.run)
        customer_thread.daemon = True
        customer_thread.start()

        sleep(0.5)  # Wait for the customer thread to run

        self.assertEqual(self.state.come, 0)
        self.assertEqual(self.state.noofseats, 2)

if __name__ == '__main__':
    unittest.main()