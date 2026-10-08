import unittest
from src.app import calculate_total, calculate_average

class TestApp(unittest.TestCase):

    def test_calculate_total(self):
        self.assertEqual(calculate_total(100, 2), 200)

    def test_calculate_average(self):
        self.assertEqual(calculate_average([10, 20]), 15)

if __name__ == "__main__":
    unittest.main()
