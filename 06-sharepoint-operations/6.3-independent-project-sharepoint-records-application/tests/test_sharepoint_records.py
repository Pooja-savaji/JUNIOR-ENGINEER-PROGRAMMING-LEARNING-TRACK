import unittest
from src.sharepoint_records import SharePointRecords


class TestSharePointRecords(unittest.TestCase):

    def setUp(self):
        self.app = SharePointRecords()

    def test_create(self):
        record = self.app.create({"Name": "Pooja"})
        self.assertEqual(record["Name"], "Pooja")

    def test_update(self):
        self.app.create({"Name": "Pooja"})
        self.app.update(1, {"Name": "Rahul"})
        self.assertEqual(self.app.get(1)["Name"], "Rahul")

    def test_delete(self):
        self.app.create({"Name": "Pooja"})
        self.assertTrue(self.app.delete(1))

    def test_document(self):
        self.app.upload_document("test.pdf", "Certificate")
        self.assertEqual(
            self.app.get_document("test.pdf"),
            "Certificate"
        )


if __name__ == "__main__":
    unittest.main()
