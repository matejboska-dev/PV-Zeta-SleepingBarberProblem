import unittest
from unittest.mock import MagicMock, patch
from tkinter import *
from PIL import ImageTk, Image
import queue
from gui import GUI
from globals import *

class TestGUI(unittest.TestCase):
    @patch('tkinter.Tk')
    @patch('PIL.ImageTk.PhotoImage')
    @patch('PIL.Image.open')
    def setUp(self, mock_image_open, mock_photo_image, mock_tk):
        # Mock Image.open and PhotoImage to avoid loading actual images
        self.mock_image = MagicMock()
        self.mock_image.resize.return_value = self.mock_image
        mock_image_open.return_value = self.mock_image
        mock_photo_image.return_value = MagicMock()

        # Mock Tkinter root window
        self.root = mock_tk()
        self.root.geometry = MagicMock()
        
        # Create mock canvas
        self.canvas = MagicMock()
        self.canvas.create_image = MagicMock()
        self.canvas.create_rectangle = MagicMock()
        self.canvas.create_text = MagicMock()
        self.canvas.delete = MagicMock()
        self.canvas.pack = MagicMock()

        # Setup GUI instance
        with patch('tkinter.Canvas', return_value=self.canvas):
            self.gui = GUI(self.root)
            self.gui.c = self.canvas

    def test_format_waiting_time(self):
        """Test if waiting time is formatted correctly"""
        test_cases = [
            (65, "01:05"),    # More than a minute
            (3600, "60:00"),  # One hour
            (45, "00:45"),    # Less than a minute
            (0, "00:00")      # Zero seconds
        ]
        
        for seconds, expected in test_cases:
            with self.subTest(seconds=seconds):
                result = self.gui.format_waiting_time(seconds)
                self.assertEqual(result, expected)

    @patch('time.time')
    def test_update_chairs(self, mock_time):
        """Test if chairs are updated correctly"""
        mock_time.return_value = 1000.0
        
        with patch('globals.state', create=True) as mock_state:
            mock_state.total_seats = 4
            mock_state.waiting_customers = {}
            
            self.gui.update_chairs(2)
            
            # Verify canvas operations
            self.canvas.delete.assert_called_with('chair')
            # Should see total_seats number of create_image calls
            self.assertTrue(self.canvas.create_image.call_count > 0)

if __name__ == '__main__':
    unittest.main()