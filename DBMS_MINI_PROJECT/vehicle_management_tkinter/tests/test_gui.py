import unittest
from tkinter import Tk
from src.gui.main_window import MainWindow

class TestMainWindow(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.main_window = MainWindow(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_main_window_title(self):
        self.assertEqual(self.main_window.root.title(), "Vehicle Management System")

    def test_main_window_geometry(self):
        self.assertEqual(self.main_window.root.geometry(), "800x600")

    def test_widgets_exist(self):
        self.assertIsNotNone(self.main_window.some_widget)  # Replace with actual widget names
        self.assertIsNotNone(self.main_window.another_widget)  # Replace with actual widget names

    def test_button_functionality(self):
        button = self.main_window.some_button  # Replace with actual button name
        button.invoke()  # Simulate button click
        # Add assertions to check the expected outcome of the button click

if __name__ == "__main__":
    unittest.main()