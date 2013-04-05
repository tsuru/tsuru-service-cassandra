import json
import os
import unittest
from cql import ProgrammingError
from mock import patch, MagicMock, call
import api



class FakeConnection(object):
    def execute(self, xxx):
        return "fake"

class ApiTestCase(unittest.TestCase):



    @classmethod
    def setUpClass(cls):
        super(ApiTestCase, cls).setUpClass()
        os.environ["TSURU_CASSANDRA_SERVER"] = "my-cassandra-host.com"
        os.environ["TSURU_CASSANDRA_PORT"] = "8888"
        reload(api)


    @classmethod
    def tearDownClass(cls):
        super(ApiTestCase, cls).tearDownClass()
        del os.environ["TSURU_CASSANDRA_SERVER"]
        del os.environ["TSURU_CASSANDRA_PORT"]


    def setUp(self):
        self.api = api.app.test_client()



class CreateInstanceTestCase(ApiTestCase):

    @patch("api.connect")
    def setUp(self, connect_mock):
        super(CreateInstanceTestCase, self).setUp()

        self.connect_mock = connect_mock
        self.resp = self.api.post("/resources", data={'name': 'my_app'})

    def test_should_return_204_if_hads_no_keyspace_name(self):
        resp = self.api.post("/resources")
        self.assertEqual(resp.status_code, 204)

    def test_should_return_if_keyspace_is_created_201(self):
        self.assertEqual(self.resp.status_code, 201)

    def test_should_connect_with_cassandra_server(self):
        self.connect_mock.assert_called_once_with(host='my-cassandra-host.com', port='8888')

    def test_should_run_create_keyspace_command(self):
        self.connect_mock.return_value.cursor.return_value.execute.assert_called_once_with(
            "CREATE KEYSPACE my_app WITH strategy_class = 'SimpleStrategy' AND strategy_options:replication_factor=3;"
        )

    @patch("api.connect")
    def test_should_run_an_error_if_anithing_wen_wrong(self, connect_mock):
        def side_effect(**kargs):
            raise ProgrammingError('boom!')
        connect_mock.side_effect = side_effect

        resp = self.api.post("/resources", data={'name': 'my_app'})
        self.assertEqual(resp.status_code, 500)
        self.assertEqual(json.loads(resp.data) , {u'error': u'boom!'})




class RemoveInstanceTestCase(ApiTestCase):
    def setUp(self):
        super(RemoveInstanceTestCase, self).setUp()
        self.connect_mock = patch('api.connect').start()
        self.resp = self.api.delete("/resources/my_instance")

    def test_should_return_200(self):
        self.assertEqual(self.resp.status_code, 200)

    def test_should_connect_with_cassandra_server(self):
        self.connect_mock.assert_called_once_with(host='my-cassandra-host.com', port='8888')

    def test_should_run_delete_keyspace_command(self):
        self.connect_mock().cursor().execute.assert_called_once_with(
            "DROP KEYSPACE my_instance"
        )

    @patch("api.connect")
    def test_should_run_an_error_if_anithing_wen_wrong(self, connect_mock):
        def side_effect(**kargs):
            raise ProgrammingError('boom!')
        connect_mock.side_effect = side_effect

        resp = self.api.post("/resources", data={'name': 'my_app'})
        self.assertEqual(resp.status_code, 500)
        self.assertEqual(json.loads(resp.data), {u'error': u'boom!'})


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


class StatusInstanceTestCase(ApiTestCase):
    def setUp(self):
        super(StatusInstanceTestCase, self).setUp()
        self.resp = self.api.get("/resources/my_instance/status")

    def test_should_return_204(self):
        self.assertEqual(self.resp.status_code, 204)



if __name__ == "__main__":
    unittest.main()