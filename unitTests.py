import os, unittest
import server

class STOTVServerTestCase(unittest.TestCase):

    def setUp(self):
        self.app=server.app.test_client()


#    def tearDown(self):

    def test1_db_setup(self):
        server.db.create_all();
        device=server.Device(123456789012345,"Test1","Donald Trump","123 Where st","New York City, New York 69483")
        server.db.session.add(device)
        server.db.session.commit()

    def test2_endpoint_recovery(self):
        rv = self.app.get('/api/v1/found/123456789012345')
        assert b'Donald Trump' in rv.data

    def test3_endpoint_rockBlock(self):
        rv = self.app.post('/api/v1/send',data=dict(imei=123456789012345,momsn=1,transmit_time="12-16-2016 16:00:00",iridium_latitude="41.310824",iridium_longitude="-67.148437",iridium_cep=3,data=""))
        assert b'OK' in rv.data

    def test4_endpoint_location_all(self):
        rv  = self.app.get('/api/v1/location')
        assert b'Test1' in rv.data

    def test5_endpoint_location_one(self):
        rv  = self.app.get('/api/v1/location/1')
        assert b'Test1' in rv.data




if __name__ == '__main__':
    unittest.main()
