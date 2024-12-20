import unittest
from globals import SharedState

class TestSharedState(unittest.TestCase):
    def setUp(self):
        self.state = SharedState()

    def test_customer_id_assignment(self):
        # Add first customer
        customer1 = self.state.add_customer(0)
        self.assertEqual(customer1.id, 1)
        
        # Add second customer
        customer2 = self.state.add_customer(1)
        self.assertEqual(customer2.id, 2)
        
        # Remove first customer and verify second customer gets ID 1
        self.state.remove_customer(0)
        self.assertEqual(self.state.waiting_customers[1].id, 1)

    def test_customer_removal(self):
        # Add three customers
        self.state.add_customer(0)  # id: 1
        self.state.add_customer(1)  # id: 2
        self.state.add_customer(2)  # id: 3
        
        # Remove middle customer
        self.state.remove_customer(1)
        
        # Verify IDs are sequential
        self.assertEqual(self.state.waiting_customers[0].id, 1)
        self.assertEqual(self.state.waiting_customers[2].id, 2)

if __name__ == '__main__':
    unittest.main()