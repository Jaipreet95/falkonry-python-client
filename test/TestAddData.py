import os
import time as timepkg
import unittest
import random
import xmlrunner
from falkonryclient.helper.utils import exceptionResponseHandler
host  = os.environ['FALKONRY_HOST_URL']  # host url
token = os.environ['FALKONRY_TOKEN']     # auth token


def check_data_ingestion(self, tracker):
    tracker_obj = None
    for i in range(0, 12):
        tracker_obj = self.fclient.get_status(tracker['__$id'])
        if tracker_obj['status'] == 'FAILED' or tracker_obj['status'] == 'ERROR':
            self.assertEqual(0, 1, 'Cannot add input data to datastream')
        if tracker_obj['status'] == 'COMPLETED' or tracker_obj['status'] == 'SUCCESS':
            break
        timepkg.sleep(5)

    if tracker_obj['status'] == 'FAILED' or tracker_obj['status'] == 'PENDING':
        self.assertEqual(0, 1, 'Cannot add input data to datastream')


class TestAddData(unittest.TestCase):

    def setUp(self):
        self.fclient = FClient(host=host, token=token, options=None)
        self.created_datastreams = []
        pass

    # Add narrow input data (json format) to multi entity Datastream
    def test_add_data_json_mutli(self):

        # creating datastream
        datastream = Schemas.Datastream()
        datastream.set_name('Motor Health' + str(random.random()))

        datasource = Schemas.Datasource()
        field = Schemas.Field()
        time = Schemas.Time()
        signal = Schemas.Signal()

        time.set_zone("GMT")
        time.set_identifier("time")
        time.set_format("YYYY-MM-DD HH:mm:ss")
        signal.set_signalIdentifier("signal")
        signal.set_valueIdentifier("value")
        field.set_signal(signal)
        datasource.set_type("STANDALONE")
        field.set_time(time)
        field.set_entityIdentifier('car')
        datastream.set_datasource(datasource)
        datastream.set_field(field)

        try:
            datastreamResponse = self.fclient.create_datastream(datastream)
            self.created_datastreams.append(datastreamResponse.get_id())
            try:
                data = '{"time" : "2016-03-01 01:01:01", "signal" : "current", "value" : 12.4, "car" : "unit1"}'
                options = {'streaming': False,
                           'hasMoreData': False,
                           'timeFormat': time.get_format(),
                           'timeZone': time.get_zone(),
                           'timeIdentifier': time.get_identifier(),
                           'signalIdentifier': 'signal',
                           'valueIdentifier': 'value',
                           'entityIdentifier': 'car'}

                # adding data to the created datastream
                response = self.fclient.add_input_data(datastreamResponse.get_id(), 'json', options, data)
                self.assertNotEqual(response['__$id'], None, 'Cannot add input data to datastream')

                # checking if data got ingested
                check_data_ingestion(self, response)

            except Exception as e:
                print(exceptionResponseHandler(e))
                self.assertEqual(0, 1, 'Cannot add input data to datastream')
        except Exception as e:
            print(exceptionResponseHandler(e))
            self.assertEqual(0, 1, 'Cannot create datastream')

    # Add narrow input data (csv format) to single entity to Datastream
    def test_add_data_csv_single(self):

        # creating datastream
        datastream = Schemas.Datastream()
        datastream.set_name('Motor Health' + str(random.random()))

        datasource = Schemas.Datasource()
        field = Schemas.Field()
        time = Schemas.Time()
        signal = Schemas.Signal()
        signal.set_valueIdentifier("value")
        signal.set_signalIdentifier("signal")
        time.set_zone("GMT")
        time.set_identifier("time")
        time.set_format("iso_8601")

        field.set_signal(signal)
        datasource.set_type("STANDALONE")
        field.set_time(time)
        datastream.set_datasource(datasource)
        datastream.set_field(field)

        try:
            datastreamResponse = self.fclient.create_datastream(datastream)
            self.created_datastreams.append(datastreamResponse.get_id())
            try:
                # input data has timeformat different than the one set  while creating datastream
                data = "time, signal, value " + "\n" + "2016-03-01 01:01:01, signal1, 3.4" + "\n" + "2016-03-01 01:01:01, signal2, 1.4"
                options = {'streaming': False,
                           'hasMoreData': False,
                           'timeFormat': "YYYY-MM-DD HH:mm:ss",
                           'timeZone': time.get_zone(),
                           'timeIdentifier': time.get_identifier()}
                response = self.fclient.add_input_data(datastreamResponse.get_id(), 'csv', options, data)
                self.assertNotEqual(response['__$id'], None, 'Cannot add input data to datastream')

                # checking if data got ingested
                check_data_ingestion(self, response)

            except Exception as e:
                print(exceptionResponseHandler(e))
                self.assertEqual(0, 1, 'Cannot add input data to datastream')
        except Exception as e:
            print(exceptionResponseHandler(e))
            self.assertEqual(0, 1, 'Cannot create datastream')

    # Add wide input data (json format) to single entity Datastream
    def test_add_data_json_single(self):

        # creating datastream
        datastream = Schemas.Datastream()
        datastream.set_name('Motor Health' + str(random.random()))

        datasource = Schemas.Datasource()
        field = Schemas.Field()
        time = Schemas.Time()
        signal = Schemas.Signal()

        time.set_zone("GMT")
        time.set_identifier("time")
        time.set_format("YYYY-MM-DD HH:mm:ss")
        field.set_signal(signal)
        datasource.set_type("STANDALONE")
        field.set_time(time)
        field.set_entityName('machine')
        datastream.set_datasource(datasource)
        datastream.set_field(field)

        try:
            datastreamResponse = self.fclient.create_datastream(datastream)
            self.created_datastreams.append(datastreamResponse.get_id())
            try:
                # adding data to datastream
                data = '{"time" :"2016-03-01 01:01:01", "current" : 12.4, "vibration" : 3.4, "state" : "On"}'
                options = {'streaming': False,
                           'hasMoreData': False,
                           'timeFormat': time.get_format(),
                           'timeZone': time.get_zone(),
                           'timeIdentifier': time.get_identifier(),
                           'entityName': 'machine'}
                response = self.fclient.add_input_data(datastreamResponse.get_id(), 'json', options, data)
                self.assertNotEqual(response['__$id'], None, 'Cannot add input data to datastream')

                # checking if data got ingested
                check_data_ingestion(self, response)

            except Exception as e:
                print(exceptionResponseHandler(e))
                self.assertEqual(0, 1, 'Cannot add input data to datastream')
        except Exception as e:
            print(exceptionResponseHandler(e))
            self.assertEqual(0, 1, 'Cannot create datastream')

    # Add wide input data (csv format) to multi entity Datastream
    def test_add_data_csv_multi(self):

        # creating datastream
        datastream = Schemas.Datastream()
        datastream.set_name('Motor Health' + str(random.random()))

        datasource = Schemas.Datasource()
        field = Schemas.Field()
        time = Schemas.Time()
        signal = Schemas.Signal()
        time.set_zone("GMT")
        time.set_identifier("time")
        time.set_format("YYYY-MM-DD HH:mm:ss")
        field.set_signal(signal)
        datasource.set_type("STANDALONE")
        field.set_time(time)
        field.set_entityIdentifier('car')
        datastream.set_datasource(datasource)
        datastream.set_field(field)

        try:
            datastreamResponse = self.fclient.create_datastream(datastream)
            self.created_datastreams.append(datastreamResponse.get_id())
            try:
                data = "time,current,vibrarion,state,car" + "\n" + "2016-03-01 01:01:01,12.4,3.4,on,car1" + "\n" + "2016-03-01 01:01:01,31.2,1.4,off,car1" + "\n" + "2016-03-01 01:01:01,24,3.2,on,car2" + "\n" + "2016-03-01 01:01:01,31,3.4,off,car2"
                options = {'streaming': False,
                           'hasMoreData': False,
                           'timeFormat': time.get_format(),
                           'timeZone': time.get_zone(),
                           'timeIdentifier': time.get_identifier(),
                           'entityIdentifier': 'car'}
                response = self.fclient.add_input_data(datastreamResponse.get_id(), 'csv', options, data)
                self.assertNotEqual(response['__$id'], None, 'Cannot add input data to datastream')

                # checking if data got ingested
                check_data_ingestion(self, response)

            except Exception as e:
                print(exceptionResponseHandler(e))
                self.assertEqual(0, 1, 'Cannot add input data to datastream')
        except Exception as e:
            print(exceptionResponseHandler(e))
            self.assertEqual(0, 1, 'Cannot create datastream')

    # Cannot add data due to missing time Identifer
    def test_add_data_csv_multi_miss_time_identifier(self):

        # creating datastream
        datastream = Schemas.Datastream()
        datastream.set_name('Motor Health' + str(random.random()))

        datasource = Schemas.Datasource()
        field = Schemas.Field()
        time = Schemas.Time()
        signal = Schemas.Signal()
        time.set_zone("GMT")
        time.set_identifier("time")
        time.set_format("YYYY-MM-DD HH:mm:ss")
        field.set_signal(signal)
        datasource.set_type("STANDALONE")
        field.set_time(time)
        field.set_entityIdentifier('car')
        datastream.set_datasource(datasource)
        datastream.set_field(field)

        try:
            datastreamResponse = self.fclient.create_datastream(datastream)
            self.created_datastreams.append(datastreamResponse.get_id())
            try:
                data = "time,current,vibrarion,state,car" + "\n" + "2016-03-01 01:01:01,12.4,3.4,on,car1" + "\n" + "2016-03-01 01:01:01,31.2,1.4,off,car1" + "\n" + "2016-03-01 01:01:01,24,3.2,on,car2" + "\n" + "2016-03-01 01:01:01,31,3.4,off,car2"
                options = {'streaming': False,
                           'hasMoreData': False,
                           'timeFormat': time.get_format(),
                           'timeZone': time.get_zone(),
                           'entityIdentifier': 'car'}
                response = self.fclient.add_input_data(datastreamResponse.get_id(), 'csv', options, data)
                self.assertEqual(0, 1, 'Missing time identifer error not caught')

                # checking if data got ingested
                check_data_ingestion(self, response)

            except Exception as e:
                # Printing only for debugging purposes
                print("\nResponse :", exceptionResponseHandler(e))
                self.assertEqual(exceptionResponseHandler(e), "Missing time identifier.", 'Missing time identifer error not caught')
        except Exception as e:
            print(exceptionResponseHandler(e))
            self.assertEqual(0, 1, 'Cannot create datastream')

    # Cannot add data due to missing time zone
    def test_add_data_csv_multi_miss_time_zone(self):

        # creating datastream
        datastream = Schemas.Datastream()
        datastream.set_name('Motor Health' + str(random.random()))

        datasource = Schemas.Datasource()
        field = Schemas.Field()
        time = Schemas.Time()
        signal = Schemas.Signal()
        time.set_zone("GMT")
        time.set_identifier("time")
        time.set_format("YYYY-MM-DD HH:mm:ss")
        field.set_signal(signal)
        datasource.set_type("STANDALONE")
        field.set_time(time)
        field.set_entityIdentifier('car')
        datastream.set_datasource(datasource)
        datastream.set_field(field)

        try:
            datastreamResponse = self.fclient.create_datastream(datastream)
            self.created_datastreams.append(datastreamResponse.get_id())
            try:
                data = "time,current,vibrarion,state,car" + "\n" + "2016-03-01 01:01:01,12.4,3.4,on,car1" + "\n" + "2016-03-01 01:01:01,31.2,1.4,off,car1" + "\n" + "2016-03-01 01:01:01,24,3.2,on,car2" + "\n" + "2016-03-01 01:01:01,31,3.4,off,car2"
                options = {'streaming': False,
                           'hasMoreData': False,
                           'timeFormat': time.get_format(),
                           'timeIdentifier': time.get_identifier(),
                           'entityIdentifier': 'car'}
                response = self.fclient.add_input_data(datastreamResponse.get_id(), 'csv', options, data)
                self.assertEqual(0, 1, 'Missing time zone error not caught')

                # checking if data got ingested
                check_data_ingestion(self, response)

            except Exception as e:
                # (b'{"message":"Missing time zone."}',)
                print("\nResponse :",exceptionResponseHandler(e))
                self.assertEqual(exceptionResponseHandler(e), "Missing time zone.", 'Missing time zone error not caught')
        except Exception as e:
            print(e.args)
            self.assertEqual(0, 1, 'Cannot create datastream')

    # Cannot add data due to missing time format
    def test_add_data_csv_multi_miss_time_format(self):

        # creating datastream
        datastream = Schemas.Datastream()
        datastream.set_name('Motor Health' + str(random.random()))

        datasource = Schemas.Datasource()
        field = Schemas.Field()
        time = Schemas.Time()
        signal = Schemas.Signal()
        time.set_zone("GMT")
        time.set_identifier("time")
        time.set_format("YYYY-MM-DD HH:mm:ss")
        field.set_signal(signal)
        datasource.set_type("STANDALONE")
        field.set_time(time)
        field.set_entityIdentifier('car')
        datastream.set_datasource(datasource)
        datastream.set_field(field)

        try:
            datastreamResponse = self.fclient.create_datastream(datastream)
            self.created_datastreams.append(datastreamResponse.get_id())
            try:
                data = "time,current,vibrarion,state,car" + "\n" + "2016-03-01 01:01:01,12.4,3.4,on,car1" + "\n" + "2016-03-01 01:01:01,31.2,1.4,off,car1" + "\n" + "2016-03-01 01:01:01,24,3.2,on,car2" + "\n" + "2016-03-01 01:01:01,31,3.4,off,car2"
                options = {'streaming': False,
                           'hasMoreData': False,
                           'timeZone': time.get_zone(),
                           'timeIdentifier': time.get_identifier(),
                           'entityIdentifier': 'car'}
                response = self.fclient.add_input_data(datastreamResponse.get_id(), 'csv', options, data)
                self.assertEqual(0, 1, 'Missing time format error not caught')

                # checking if data got ingested
                check_data_ingestion(self, response)

            except Exception as e:
                # Printing only for debugging purposes
                print('\nResponse :',exceptionResponseHandler(e))
                self.assertEqual(exceptionResponseHandler(e), "Missing time format.", 'Missing time format error not caught')
        except Exception as e:
            print(e)
            self.assertEqual(0, 1, 'Cannot create datastream')

    # Add live input data (json format) to Datastream (Used for live monitoring)
    @unittest.skip("Skipping streaming data ingestion")
    # Streaming data can only be sent to datastream if datastream is live. So make sure that datastream is live first
    def test_add_data_streaming_json(self):

        datastreamId = 'datstream-id'  # id of the datasream which is live
        try:
            data = "time, tag, value " + "\n" + "2016-03-01 01:01:01, signal1_entity1, 3.4" + "\n" + "2016-03-01 01:01:01, signal2_entity1, 1.4"
            options = {'streaming': True, 'hasMoreData':False}
            response = self.fclient.add_input_data(datastreamId, 'json', options, data)
            self.assertNotEqual(response, 'Data Submitted Successfully', 'Cannot add historical input data to datastream')
        except Exception as e:
            # if response is "{"message":"Datastream is not live, streaming data cannot be accepted."}" Please turn on datastream first then add streaming data
            print(e.args)
            self.assertEqual(0, 1, 'Cannot add input data to datastream')

    # Add live input data (csv format) to Datastream (Used for live monitoring)
    @unittest.skip("Skipping streaming data ingestion")
    # Streaming data can only be sent to datastream of datastream is live. So make sure that datastream is live first
    def test_add_data_streaming_csv(self):

        datastreamId = 'datstream-id'  # id of the datasream which is live
        try:
            data = '{"time" :"2016-03-01 01:01:01", "current" : 12.4, "vibration" : 3.4, "state" : "On"}'
            options = {'streaming': True, 'hasMoreData':False}
            response = self.fclient.add_input_data(datastreamId, 'json', options, data)
            self.assertNotEqual(response, 'Data Submitted Successfully', 'Cannot add historical input data to datastream')
        except Exception as e:
            # if response is "{"message":"Datastream is not live, streaming data cannot be accepted."}" Please turn on datastream first then add streaming data
            print(e.args)
            self.assertEqual(0, 1, 'Cannot add input data to datastream')

    # Add narrow input data (csv format) with batch identifier to multi thing Datastream
    def test_add_narrow_multi_thing_data_with_batch(self):

        # creating datastream
        datastream = Schemas.Datastream()
        datastream.set_name('Motor Health' + str(random.random()))

        datasource = Schemas.Datasource()
        field = Schemas.Field()
        time = Schemas.Time()
        signal = Schemas.Signal()

        time.set_zone("GMT")
        time.set_identifier("time")
        time.set_format("millis")
        signal.set_signalIdentifier("signal")
        signal.set_valueIdentifier("value")
        field.set_signal(signal)
        datasource.set_type("STANDALONE")
        field.set_time(time)
        field.set_entityIdentifier('unit')
        field.set_batchIdentifier('batchId')
        datastream.set_datasource(datasource)
        datastream.set_field(field)

        try:
            datastreamResponse = self.fclient.create_datastream(datastream)
            self.created_datastreams.append(datastreamResponse.get_id())
            try:

                # adding data to datastream
                data = 'time,batchId,unit,signal,value\n' \
                       '1,batch_1,unit1,signal1,9.95\n' \
                       '2,batch_1,unit1,signal1,4.45\n' \
                       '3,batch_2,unit1,signal1,1.45\n' \
                       '4,batch_2,unit1,signal1,8.45\n' \
                       '5,batch_2,unit1,signal1,2.45\n' \
                       '1,batch_1,unit1,signal2,19.95\n' \
                       '2,batch_1,unit1,signal2,14.45\n' \
                       '3,batch_2,unit1,signal2,10.45\n' \
                       '4,batch_2,unit1,signal2,18.45\n' \
                       '5,batch_2,unit1,signal2,12.45\n' \
                       '1,batch_1,unit1,signal3,39.95\n' \
                       '2,batch_1,unit1,signal3,34.45\n' \
                       '3,batch_2,unit1,signal3,30.45\n' \
                       '4,batch_2,unit1,signal3,38.45\n' \
                       '5,batch_2,unit1,signal3,32.45\n'
                options = {
                    'streaming': False,
                    'hasMoreData': False
                }
                response = self.fclient.add_input_data(datastreamResponse.get_id(), 'csv', options, data)
                self.assertNotEqual(response['__$id'], None, 'Cannot add input data to datastream')

                # checking if data got ingested
                check_data_ingestion(self, response)

            except Exception as e:
                print(exceptionResponseHandler(e))
                self.assertEqual(0, 1, 'Cannot add input data to datastream')
        except Exception as e:
            print(exceptionResponseHandler(e))
            self.assertEqual(0, 1, 'Cannot create datastream')

    # Add narrow input data (json format) with batch identifier to single thing Datastream
    def test_add_narrow_single_thing_data_with_batch(self):

        # creating datastream
        datastream = Schemas.Datastream()
        datastream.set_name('Motor Health' + str(random.random()))

        datasource = Schemas.Datasource()
        field = Schemas.Field()
        time = Schemas.Time()
        signal = Schemas.Signal()

        time.set_zone("GMT")
        time.set_identifier("time")
        time.set_format("millis")
        signal.set_signalIdentifier("inputs")
        signal.set_valueIdentifier("val")
        field.set_signal(signal)
        datasource.set_type("STANDALONE")
        field.set_time(time)
        field.set_batchIdentifier('batches')
        datastream.set_datasource(datasource)
        datastream.set_field(field)

        try:
            datastreamResponse = self.fclient.create_datastream(datastream)
            self.created_datastreams.append(datastreamResponse.get_id())
            try:

                # adding data to datastream
                data = '{"time": 1,"batchId": "batch_1","signal": "signal1","value": 9.95}\n' \
                       '{"time": 2,"batchId": "batch_1","signal": "signal1","value": 4.45}\n' \
                       '{"time": 3,"batchId": "batch_2","signal": "signal1","value": 1.45}\n' \
                       '{"time": 4,"batchId": "batch_2","signal": "signal1","value": 8.45}\n' \
                       '{"time": 5,"batchId": "batch_2","signal": "signal1","value": 2.45}'
                options = {
                    'streaming': False,
                    'hasMoreData': False,
                    'timeFormat': time.get_format(),
                    'timeZone': time.get_zone(),
                    'timeIdentifier': time.get_identifier(),
                    'signalIdentifier': 'signal',
                    'valueIdentifier': 'value',
                    'batchIdentifier': 'batchId'
                }
                response = self.fclient.add_input_data(datastreamResponse.get_id(), 'json', options, data)
                self.assertNotEqual(response['__$id'], None, 'Cannot add input data to datastream')

                # checking if data got ingested
                check_data_ingestion(self, response)

            except Exception as e:
                print(exceptionResponseHandler(e))
                self.assertEqual(0, 1, 'Cannot add input data to datastream')
        except Exception as e:
            print(exceptionResponseHandler(e))
            self.assertEqual(0, 1, 'Cannot create datastream')

    # Add wide input data (csv format) with batch identifier to multi thing Datastream
    def test_add_wide_multi_thing_data_with_batch(self):

        # creating datastream
        datastream = Schemas.Datastream()
        datastream.set_name('Motor Health' + str(random.random()))

        datasource = Schemas.Datasource()
        field = Schemas.Field()
        time = Schemas.Time()
        signal = Schemas.Signal()
        time.set_zone("GMT")
        time.set_identifier("time")
        time.set_format("millis")
        field.set_signal(signal)
        datasource.set_type("STANDALONE")
        field.set_time(time)
        field.set_entityIdentifier('unit')
        field.set_batchIdentifier('batchId')
        datastream.set_datasource(datasource)
        datastream.set_field(field)

        try:
            datastreamResponse = self.fclient.create_datastream(datastream)
            self.created_datastreams.append(datastreamResponse.get_id())
            try:
                data = 'time,batchId,unit,signal1,signal2,signal3\n' \
                       '1,batch_1,unit1,9.95,19.95,39.95\n' \
                       '2,batch_1,unit1,4.45,14.45,34.45\n' \
                       '3,batch_2,unit1,1.45,10.45,30.45\n' \
                       '4,batch_2,unit1,8.45,18.45,38.45\n' \
                       '5,batch_2,unit1,2.45,12.45,32.45'
                options = {
                    'streaming': False,
                    'hasMoreData': False
                }
                response = self.fclient.add_input_data(datastreamResponse.get_id(), 'csv', options, data)
                self.assertNotEqual(response['__$id'], None, 'Cannot add input data to datastream')

                # checking if data got ingested
                check_data_ingestion(self, response)

            except Exception as e:
                print(exceptionResponseHandler(e))
                self.assertEqual(0, 1, 'Cannot add input data to datastream')
        except Exception as e:
            print(exceptionResponseHandler(e))
            self.assertEqual(0, 1, 'Cannot create datastream')

    # Add wide input data (json format) with batch identifier to single thing Datastream
    def test_add_wide_single_thing_data_with_batch(self):

        # creating datastream
        datastream = Schemas.Datastream()
        datastream.set_name('Motor Health' + str(random.random()))

        datasource = Schemas.Datasource()
        field = Schemas.Field()
        time = Schemas.Time()
        signal = Schemas.Signal()
        time.set_zone("GMT")
        time.set_identifier("time")
        time.set_format("millis")
        field.set_signal(signal)
        datasource.set_type("STANDALONE")
        field.set_time(time)
        field.set_batchIdentifier('batches')
        datastream.set_datasource(datasource)
        datastream.set_field(field)

        try:
            datastreamResponse = self.fclient.create_datastream(datastream)
            self.created_datastreams.append(datastreamResponse.get_id())
            try:

                # adding data to datastream
                data = '{"time": 1,"batchId": "batch_1","signal1": 9.95,"signal2": 19.95,"signal3": 39.95}\n' \
                       '{"time": 2,"batchId": "batch_1","signal1": 4.45,"signal2": 14.45,"signal3": 34.45}\n' \
                       '{"time": 3,"batchId": "batch_2","signal1": 1.45,"signal2": 10.45,"signal3": 30.45}\n' \
                       '{"time": 4,"batchId": "batch_2","signal1": 8.45,"signal2": 18.45,"signal3": 38.45}\n' \
                       '{"time": 5,"batchId": "batch_2","signal1": 2.45,"signal2": 12.45,"signal3": 32.45}'
                options = {
                    'streaming': False,
                    'hasMoreData': False,
                    'timeFormat': time.get_format(),
                    'timeZone': time.get_zone(),
                    'timeIdentifier': time.get_identifier(),
                    'batchIdentifier': 'batchId'
                }
                response = self.fclient.add_input_data(datastreamResponse.get_id(), 'json', options, data)
                self.assertNotEqual(response['__$id'], None, 'Cannot add input data to datastream')

                # checking if data got ingested
                check_data_ingestion(self, response)

            except Exception as e:
                print(exceptionResponseHandler(e))
                self.assertEqual(0, 1, 'Cannot add input data to datastream')
        except Exception as e:
            print(exceptionResponseHandler(e))
            self.assertEqual(0, 1, 'Cannot create datastream')

    def tearDown(self):  # teardown
        for ds in self.created_datastreams:
            try:
                self.fclient.delete_datastream(ds)
            except Exception as e:
                print(exceptionResponseHandler(e))
    pass

if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append(
            path.dirname(
                path.dirname(
                    path.abspath(__file__)
                )
            )
        )
        from falkonryclient import schemas as Schemas
        from falkonryclient import client as FClient
    else:
        from ..falkonryclient import schemas as Schemas
        from ..falkonryclient import client as FClient
    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output='out'),
        failfast=False, buffer=False, catchbreak=False)
else:
    from falkonryclient import schemas as Schemas
    from falkonryclient import client as FClient
