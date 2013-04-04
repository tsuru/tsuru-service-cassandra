import json
import unittest
import api


class ApiTestCase(unittest.TestCase):

    def setUp(self):
        self.api = api.app.test_client()

    def test_should_return_201_on_create_instance(self):
        resp = self.api.post("/resources")
        self.assertEqual(resp.status_code, 201)

    def test_should_return_201_on_bind_instance(self):
        resp = self.api.post("/resources/my_instance")
        self.assertEqual(resp.status_code, 201)

    def test_should_retuns_a_json_content_type(self):
        resp = self.api.post("/resources/my_instance")
        self.assertEqual(resp.content_type, 'application/json')

    def test_should_return_a_hardcoded_json_on_bind_instance(self):
        resp = self.api.post("/resources/my_instance")
        self.assertEqual(json.loads(resp.data) , {u'SOMEVAR': u'somevalue'})



if __name__ == "__main__":
    unittest.main()