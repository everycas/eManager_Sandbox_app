from ini_res import Ini
import datetime as dt
import pymongo

INI_NAME = 'eMan.ini'
LOG_NAME = 'eMan.log'

DB_NAME = 'USER-10000001-DB'  # every new user (owner / admin) will get own new base
SETS_COL = 'settings'
ITEMS_COL = 'items'
CORRS_COL = 'corrs'
ORDERS_COL = 'orders'
BILLS_COL = 'bills'

# ini obj
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


def create_select_base(connection):

    """ Create / select eMan base """

    return connection[DB_NAME]


def new_doc_insert(connection, collection: str, document: dict):

    """ Insert new document to data collection """

    db = connection[DB_NAME]
    col = db[collection]
    doc = document
    col.insert_one(doc)


def find_sort_docs(connection, collection: str, search_request: str):

    """ Find all docs in selected collection that is fits by search request """

    pass


def to_guid(num_string: str):

    """ Convert any string number to guid string """

    add_zero = ''
    guid_prefix = '{00000000-0000-0000-0000-'
    guid_postfix = '}'

    if len(num_string) < 12:
        diff = 12 - len(num_string)  # 6
        for _ in range(diff):
            add_zero += '0'
            code = add_zero + num_string
    elif len(num_string) > 12:
        diff = len(num_string) - 12
        code = num_string[diff:]
    else:
        code = num_string

    result_guid = guid_prefix + code + guid_postfix

    return result_guid


SAMPLE_DOC_DISH_ITEM = {
    'guid': to_guid(num_string='1'),
    'type': 'Dish',
    'group': 'Meat',
    'name': 'Beefsteak',
    'munit': 'Portion',
    'qnt': 1.0,
    'price': 120.45
    }

client = connect_to_server()

create_select_base(connection=client)

new_doc_insert(connection=client, collection=ITEMS_COL, document=SAMPLE_DOC_DISH_ITEM)




