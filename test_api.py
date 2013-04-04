import json
import unittest
import api


class ApiTestCase(unittest.TestCase):

    def setUp(self):
        self.api = api.app.test_client()



class CreateInstanceTestCase(ApiTestCase):
    def setUp(self):
        super(CreateInstanceTestCase, self).setUp()
        self.resp = self.api.post("/resources")

    def test_should_return_201(self):
        self.assertEqual(self.resp.status_code, 201)


class RemoveInstanceTestCase(ApiTestCase):
    def setUp(self):
        super(RemoveInstanceTestCase, self).setUp()
        self.resp = self.api.delete("/resources/my_instance")

    def test_should_return_200(self):
        self.assertEqual(self.resp.status_code, 200)


class BindInstanceTestCase(ApiTestCase):
    def setUp(self):
        super(BindInstanceTestCase, self).setUp()
        self.resp = self.api.post("/resources/my_instance")

    def test_should_return_201(self):
        self.assertEqual(self.resp.status_code, 201)

    def test_should_retuns_a_json_content_type(self):
        self.assertEqual(self.resp.content_type, 'application/json')

    def test_should_return_a_hardcoded_json(self):
        self.assertEqual(json.loads(self.resp.data) , {u'SOMEVAR': u'somevalue'})

class UnbindInstanceTestCase(ApiTestCase):
    def setUp(self):
        super(UnbindInstanceTestCase, self).setUp()
        self.resp = self.api.delete("/resources/my_instance/hostname/my_host")

    def test_should_return_200(self):
        self.assertEqual(self.resp.status_code, 200)




if __name__ == "__main__":
    unittest.main()