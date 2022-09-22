from ini_res import Ini
import datetime as dt
import pymongo

INI_NAME = 'eMan.ini'
LOG_NAME = 'eMan.log'

DB_NAME = 'data'
SETS_COL = 'settings'
ITEMS_COL = 'items'
CORRS_COL = 'corrs'
ORDERS_COL = 'orders'
BILLS_COL = 'bills'


# ini
INI = Ini()
INI.ini_name = INI_NAME
INI.log_name = LOG_NAME


def connect_to_server():

    """ Make client connection to MongoDB Sever """

    # params
    ini_server_name = INI.get(section='server', param='name')
    ini_server_ip = INI.get(section='server', param='ip')
    ini_server_port = INI.get(section='server', param='port')

    # connection string
    ini_mongo_connection_string = f"{ini_server_name}://{ini_server_ip}:{ini_server_port}/"
    return pymongo.MongoClient(ini_mongo_connection_string)


def create_new_base(connection):

    """ Create new eMan base from pattern """

    client = connection
    db = client[DB_NAME]
    # create collections
    sets = db[SETS_COL]
    items = db[ITEMS_COL]
    corrs = db[CORRS_COL]
    orders = db[ORDERS_COL]
    bills = db[BILLS_COL]
    # create docs
    sets_doc = {'lang': 'eng'}
    items_doc = {'name': 'Пирожок с картошкой', 'price': 120.95}
    corrs_doc = {'name': 'Admin', 'role': 'admin', 'type': 'staff'}
    orders_doc = {'data': dt.datetime.now(), 'number': ''}
    bills_doc = {'data': dt.datetime.now(), 'number': ''}

    # insert docs to collections
    sets.insert_one(sets_doc)
    items.insert_one(items_doc)
    corrs.insert_one(corrs_doc)
    orders.insert_one(orders_doc)
    bills.insert_one(bills_doc)


def insert_new_doc(connection, collection, document):

    """ Insert new document to data collection """

    client = connection
    db = client[DB_NAME]
    col = db[collection]
    doc = document
    col.insert_one(doc)





c = connect_to_server()
create_new_base(connection=c)

# doc = {'test': 'test2'}
# insert_new_doc(connection=c, collection='items', document=doc)




