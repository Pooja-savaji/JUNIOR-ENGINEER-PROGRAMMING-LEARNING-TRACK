
import unittest
from src.app import add_task

class TestApp(unittest.TestCase):
    def test_empty_task(self):
        with self.assertRaises(ValueError):
            add_task(" ")

if __name__ == "__main__":
    unittest.main()
