import unittest
from app import app

class Testing(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def testfetchrecords(self):
        response = self.app.get('/api/fetchrecords/1')
        self.assertEqual(response.status_code, 200)

    def testfetchgoals(self):
        response = self.app.get('/api/fetchgoals')
        self.assertEqual(response.status_code, 200)

    def testaddgoals(self):
        response = self.app.get('/api/addgoals')
        self.assertEqual(response.status_code, 201)


if __name__ == '__main__':
    unittest.main()
