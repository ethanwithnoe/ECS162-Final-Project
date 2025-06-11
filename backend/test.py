import unittest
from app import app
import json

class Testing(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        
        self.testgoal = {
            "Age": 25,
            "Gender": "F",
            "HeightFt": 5,
            "HeightIn": 5,
            "HeightCM": 10,
            "Weight": 130,
            "WeightKG": 10,
            "Activity": "M",
            "BMR": 10,
            "AMR": 10,
            "calories": 10,
            "protein": 10,
            "fat": 10,
            "carbohydrates": 10
        }

        self.testfood = {
            "brand": "test",
            "calories": 100,
            "protein": 100,
            "fat": 100,
            "carbohydrates": 100,
            "description": "test"
        }

    def testfetchrecords(self):
        response = self.app.get('/api/fetchrecords/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('records', data)

    def testfetchgoals(self):
        response = self.app.get('/api/fetchgoals')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(any(key in data for key in ['calories', 'protein', 'fat', 'carbohydrates']))

    def testaddgoals(self):
        response = self.app.post('/api/addgoals',
            json=self.testgoal,
            content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['calories'], self.testgoal['calories'])
        self.assertEqual(data['protein'], self.testgoal['protein'])
        self.assertEqual(data['fat'], self.testgoal['fat'])
        self.assertEqual(data['carbohydrates'], self.testgoal['carbohydrates'])

    def testaddfood(self):
        response = self.app.post('/api/addfood',
            json=self.testfood,
            content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['brand'], self.testgoal['brand'])
        self.assertEqual(data['calories'], self.testgoal['calories'])
        self.assertEqual(data['protein'], self.testgoal['protein'])
        self.assertEqual(data['fat'], self.testgoal['fat'])
        self.assertEqual(data['carbohydrates'], self.testgoal['carbohydrates'])
        self.assertEqual(data['description'], self.testgoal['description'])

    def testgetuserfoods(self):
        response = self.app.get('/api/getuserfoods')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('result', data)

    def testgetuserfoodstd(self):
        response = self.app.get('/api/getuserfoodsTD')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('result', data)

    def testgetuser(self):
        response = self.app.get('/api/getuser')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('result', data)

if __name__ == '__main__':
    unittest.main()
