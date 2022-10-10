from ini_res import Ini
import datetime as dt
import pymongo
import uuid


class Mongoman:

    """ Main working functionality eMan with MongoDB """

    def __init__(self):

        self.ini = Ini()
        self.ini.log_name = 'eMan.log'
        self.ini.ini_name = 'eMan.ini'

        self.dts = ''.join([char for char in str(dt.datetime.now()) if char.isnumeric()])[:20]  # yyyymmddhhmmssmsmsms

    # Service actions ---------------------------------------------------------

    @staticmethod
    def guid_gen():

        """ GUID generation / using uuid.uuid5() """

        code = str(uuid.uuid5(uuid.NAMESPACE_DNS, "GUID"))
        return '{' + code + '}'

    def num_to_guid(self, num_string: str, is_numeric: bool):

        """ Convert any number string to guid string / if is_numeric False = mask: '{UUID5[:-13]-CODE(12)}' """

        # if not is_numeric
        uuid5 = f'{str(uuid.uuid5(uuid.NAMESPACE_DNS, "GUID"))[:-13]}-'
        # if is_numeric
        dt_code = f'{self.dts[:8]}-{self.dts[8:12]}-{self.dts[12:16]}-{self.dts[16:20]}-'

        add_zero = ''
        if len(num_string) < 12:
            diff = 12 - len(num_string)
            for _ in range(diff):
                add_zero += '0'
                code = add_zero + num_string
        elif len(num_string) > 12:
            diff = len(num_string) - 12
            code = num_string[diff:]
        else:
            code = num_string

        if is_numeric:
            return '{' + dt_code + code + '}'
        else:
            return '{' + uuid5 + code + '}'

    @staticmethod
    def doc_id_gen(connection: object, dbname: str, collection: str):

        """ Mongo documents id generator """

        db = connection[dbname]
        col = db[collection]
        ids = [doc['_id'] for doc in col.find()]
        if ids:
            return max(ids) + 1
        else:
            return 1

    # MongoDB actions ---------------------------------------------------------

    def server_connect(self):

        """ Make client connection to MongoDB Sever / MongoClient('connection string') """

        # connection string params
        ini_server_name = self.ini.get(section='server', param='name')
        ini_server_ip = self.ini.get(section='server', param='ip')
        ini_server_port = self.ini.get(section='server', param='port')

        # connection string
        ini_mongo_connection_string = f"{ini_server_name}://{ini_server_ip}:{ini_server_port}/"

        return pymongo.MongoClient(ini_mongo_connection_string)

    def create_new_base(self, connection: object):

        """ Create / select eMan base """

        def dbname_gen():
            """ Generate db name GUID / mask: 'YYYYMMDD-HHMM-SSMS-eMan-UUID5[-12:]' """

            code = f'{self.dts[:8]}-{self.dts[8:12]}-{self.dts[12:16]}-eMan-{str(uuid.uuid5(uuid.NAMESPACE_DNS, "GUID"))[-12:]}'
            return '{' + code + '}'

        dbname = dbname_gen()
        return connection[dbname]

