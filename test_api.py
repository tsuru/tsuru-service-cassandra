import os
import unittest
import api


class ApiTestCase(unittest.TestCase):

    def setUp(self):
        self.api = api.app.test_client()

    def test_should_return_201_on_create_instance(self):
        resp = self.api.post("/resources")
        self.assertEqual(resp.status_code, 201)



if __name__ == "__main__":
    unittest.main()