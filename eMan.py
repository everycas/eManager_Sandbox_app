from ini_res import Ini
import datetime as dt
import pymongo

INI_NAME = 'eMan.ini'
LOG_NAME = 'eMan.log'
DT_NOW = dt.datetime.now()

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


def create_or_select_base(connection: object):

    """ Create / select eMan base """

    return connection[DB_NAME]


def insert_one_doc_to_col(connection: object, collection: str, document: dict):

    """ Insert new document to data collection / Mongo insert_one({}) """

    db = connection[DB_NAME]
    col = db[collection]
    doc = document
    col.insert_one(doc)


def insert_many_docs_to_col(connection: object, collection: str, docs_list: list):

    """ Insert new documents to data collection / Mongo insert_many([{}, ... {}]) """

    db = connection[DB_NAME]
    col = db[collection]
    col.insert_many(docs_list)


def find_all_docs_in_col(connection: object, collection: str):

    """ Find all docs in selected collection / Mongo find() """

    db = connection[DB_NAME]
    col = db[collection]

    find_result = col.find()

    return find_result


def del_one_doc_from_col(connection: object, collection: str, d_key: str, d_value: 'str'):

    """ Delete one document in collection / Mongo delete_one({d_key: d_value}) """

    db = connection[DB_NAME]
    col = db[collection]
    col.delete_one({d_key: d_value})


def del_all_docs_from_col(connection: object, collection: str):

    """ Delete all documents from selected collection / Mongo drop() """

    db = connection[DB_NAME]
    col = db[collection]
    col.drop()


def del_many_docs_from_col(connection: object, collection: str, d_key: str, d_value: str):

    """ Delete all docs in collection filtered by search request / Mongo deleteMany({d_key: d_value}) """

    db = connection[DB_NAME]
    col = db[collection]
    col.delete_many({d_key: d_value})


def update_one_doc_in_col(connection: object, collection: str, d_key: str, d_value: str, update: dict):

    """ Update one document in collection / Mongo update_one({d_key: d_value}, {'$set': {update}}) """

    db = connection[DB_NAME]
    col = db[collection]
    col.update_one({d_key: d_value}, {'$set': update})


def update_many_docs_in_col(connection: object, collection: str, d_key: str, d_value: str, update: dict):

    """ Update many documents in collection / Mongo update_many({d_key: d_value}, {'$set': {update}}) """

    db = connection[DB_NAME]
    col = db[collection]
    col.update_one({d_key: d_value}, {'$set': update})


def num_string_to_guid(num_string: str):

    """ Convert any number string to guid string """

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


# TESTS ------------------------------------------------- #

SAMPLE_DOC_ITEM_TO_INSERT = {
    'guid': num_string_to_guid(num_string='1'),
    'type': 'Dish',
    'group': 'Meat',
    'name': 'Beefsteak',
    'munit': 'Portion',
    'qnt': 1.0,
    'price': 120.45
    }

SAMPLE_DOCS_ITEMS_LIST_TO_INSERT = [
    {
        'type': 'Dish',
        'group': 'Meat',
        'name': 'Meat Fries',
        'munit': 'Portion',
        'qnt': 1.0,
        'price': 245.90
    },
    {
        'type': 'Dish',
        'group': 'Chicken',
        'name': 'Chicken Fries',
        'munit': 'Portion',
        'qnt': 1.0,
        'price': 223.99
    }
]

SAMPLE_DOC_ITEM_GUID_UPDATE = {
    'guid': num_string_to_guid(num_string='1234')
}

client = connect_to_server()

# create_select_base(connection=client)

# insert_one_doc_to_col(connection=client, collection=ITEMS_COL, document=SAMPLE_DOC_DISH_ITEM)

# insert_many_docs_to_col(connection=client, collection=ITEMS_COL, docs_list=SAMPLE_DOCS_ITEMS_LIST_TO_INSERT)

# del_one_doc_from_col(connection=client, collection=ITEMS_COL, d_key='name', d_value='Chicken Fries')

# del_all_docs_from_col(connection=client, collection=ITEMS_COL)

# del_docs_from_col_by_filter(connection=client, collection=ITEMS_COL, f_key='group', f_value='Meat')

# update_one_doc_in_col(connection=client, collection=ITEMS_COL, d_key='name', d_value='Meat Fries', update=SAMPLE_DOC_ITEM_GUID_UPDATE)

update_many_docs_in_col(connection=client, collection=ITEMS_COL, d_key='name', d_value='Meat Fries', update=SAMPLE_DOC_ITEM_GUID_UPDATE)


