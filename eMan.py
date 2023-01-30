from ini_res import Ini
import datetime as dt
import uuid
import pymongo

# ini & log names
INI_NAME = 'eMan.ini'
LOG_NAME = 'eMan.log'

# ini obj
INI = Ini()
INI.ini_name = INI_NAME
INI.log_name = LOG_NAME

# db
INI_DBNAME = INI.get(section='base', param='name')  # dbname from ini
DBNAME = INI_DBNAME

DT_NOW = dt.datetime.now()
DT_STRING = ''.join([char for char in str(dt.datetime.now()) if char.isnumeric()])[: 20]  # 'yyyymmddhhmmssms'

# default db collections
CFG_COL = 'settings'
ITEMS_COL = 'items'
CORRS_COL = 'corrs'
WORK_COL = 'orders'
REP_COL = 'reports'

# MONGO API --------------------------------------------------------------------------------->

# GENERATORS -------------------------------------------------------------------------------->


def generate_dbname(connection: object):

    """ Generate db name / mask: YYYYMMDD-HHMM-SSMS-USER-UUID """

    dbname_yyyymmdd = f'{DT_STRING[:8]}-'
    dbname_hhmmss = f'{DT_STRING[8:14]}-'
    dbname_msmsms = f'{DT_STRING[14:20]}-'
    dbname_uuid = f'{str(uuid.getnode())}'

    return dbname_yyyymmdd + dbname_hhmmss + dbname_msmsms + 'USERDB-' + dbname_uuid


def generate_doc_uid(connection: object, collection: str):

    """ Documents universal id generator """

    db = connection[INI_DBNAME]
    col = db[collection]
    ids = [doc['_id'] for doc in col.find()]

    if ids:
        return max(ids) + 1
    else:
        return 1


def generate_guid(num_string: str):

    """ Convert any number string to guid string / mask: '{YYYYMMDD(8)-HHMM(4)-SSMS(4)-UUID(4)-CODE(12)}' """

    add_zero = ''
    guid_prefix = '{'
    guid_yyyymmdd = f'{DT_STRING[:8]}-'
    guid_hhmm = f'{DT_STRING[8:12]}-'
    guid_ssms = f'{DT_STRING[12:16]}-'
    guid_uuid = f'{str(uuid.getnode())[:4]}-'
    guid_postfix = '}'

    code = ''
    if len(num_string) < 8:
        diff = 8 - len(num_string)  # 6
        for _ in range(diff):
            add_zero += '0'
            code = add_zero + num_string
    elif len(num_string) > 8:
        diff = len(num_string) - 8
        code = num_string[diff:]
    else:
        code = num_string

    result_guid = guid_prefix + guid_yyyymmdd + guid_hhmm + guid_ssms + guid_uuid + code + guid_postfix

    return result_guid


# MONGO SERVER & DB ------------------------------------------------------------------------->


def connect_to_server():

    """ Make client connection to MongoDB Server / MongoClient('connection string') """

    # connection string params
    ini_server_name = INI.get(section='server', param='name')
    ini_server_ip = INI.get(section='server', param='ip')
    ini_server_port = INI.get(section='server', param='port')

    # connection string
    ini_mongo_connection_string = f"{ini_server_name}://{ini_server_ip}:{ini_server_port}/"

    try:
        connection = pymongo.MongoClient(ini_mongo_connection_string)

    # connection error logging
    except Exception as Argument:
        with open(LOG_NAME, "a") as log_file:
            log_file.write(f"\n{DT_NOW}: mongo server connection error. Message:{str(Argument)}")

    else:
        return connection


def create_new_db(connection: object):

    """ Create new eMan db if ini[base]name not specified """

    server = connect_to_server()
    new_dbname = generate_dbname(connection=server)

    if INI_DBNAME == '':
        INI.set(section='base', param='name', data=new_dbname)
        new_db = connection[new_dbname]
    else:
        new_db = connect_to_db(dbname=INI_DBNAME)

    return new_db


def connect_to_db(dbname:str):

    """ Get eMan base from ini """

    dbname = INI_DBNAME
    try:
        if dbname != '':
            return INI.get(section='base', param='name')

    except Exception as Argument:
        with open(LOG_NAME, "a") as log_file:
            log_file.write(f"\n{DT_NOW}: mongo server db selection error. Message:{str(Argument)}")


# DB COLLECTIONS (COLS) & DOCUMENTS (DOCS) ------------------------------------------------->


def insert_one_doc_to_col(connection: object, collection: str, document: dict):

    """ Insert new document to data collection / Mongo insert_one({}) """

    db = connection[INI_DBNAME]
    col = db[collection]
    doc = document
    col.insert_one(doc)


def insert_many_docs_to_col(connection: object, collection: str, docs_list: list):

    """ Insert new documents to data collection / Mongo insert_many([{}, ... {}]) """

    db = connection[INI_DBNAME]
    col = db[collection]
    col.insert_many(docs_list)


def find_docs_in_col(connection: object, collection: str, d_key: str, d_value: str):

    """ Find documents in collection by search request / Mongo find({d_key: d_value})  """

    db = connection[INI_DBNAME]
    col = db[collection]

    return [doc for doc in col.find({d_key: d_value})]


def find_all_docs_in_col(connection: object, collection: str):

    """ Find all docs in selected collection / Mongo find() """

    db = connection[INI_DBNAME]
    col = db[collection]

    return [doc for doc in col.find()]


def del_one_doc_from_col(connection: object, collection: str, d_key: str, d_value: 'str'):

    """ Delete one document in collection / Mongo delete_one({d_key: d_value}) """

    db = connection[INI_DBNAME]
    col = db[collection]
    col.delete_one({d_key: d_value})


def del_many_docs_from_col(connection: object, collection: str, d_key: str, d_value: str):

    """ Delete all docs in collection filtered by search request / Mongo deleteMany({d_key: d_value}) """

    db = connection[INI_DBNAME]
    col = db[collection]
    col.delete_many({d_key: d_value})


def del_all_docs_from_col(connection: object, collection: str):

    """ Delete all documents from selected collection / Mongo drop() """

    db = connection[INI_DBNAME]
    col = db[collection]
    col.drop()


def update_one_doc_in_col(connection: object, collection: str, d_key: str, d_value: str, update: dict):

    """ Update one document in collection / Mongo update_one({d_key: d_value}, {'$set': {update}}) """

    db = connection[INI_DBNAME]
    col = db[collection]
    col.update_one({d_key: d_value}, {'$set': update})


# TESTING ------------------------------------------------------------------------------------>

client = connect_to_server()

SAMPLE_DOC_TO_INSERT = {
        '_id': generate_doc_uid(connection=client, collection=ITEMS_COL),
        'guid': generate_guid(num_string=str(generate_doc_uid(connection=client, collection=ITEMS_COL))),
        'modified': DT_STRING,
        'active': True,
        'type': 'Dish',
        'group': 'Meat',
        'name': 'Meat & Chicken Mix',
        'munit': 'Portion',
        'qnt': 1.0,
        'price': 245.90
    }


SAMPLE_DOC_UPDATE = {
    'modified': DT_STRING,
    'name': 'Fried Chicken and Potatoes',
    'price': 176.90
}


# create_select_base(connection=client)

insert_one_doc_to_col(connection=client, collection=ITEMS_COL, document=SAMPLE_DOC_TO_INSERT)

#  #  insert_many_docs_to_col(connection=client, collection=ITEMS_COL, docs_list=SAMPLE_DOCS_TO_INSERT)

# del_one_doc_from_col(connection=client, collection=ITEMS_COL, d_key='name', d_value='Chicken Fries')

# del_all_docs_from_col(connection=client, collection=ITEMS_COL)

# del_docs_from_col_by_filter(connection=client, collection=ITEMS_COL, f_key='group', f_value='Meat')

# update_one_doc_in_col(connection=client, collection=ITEMS_COL, d_key='_id', d_value=1, update=SAMPLE_DOC_UPDATE)

# print(find_all_docs_in_col(connection=client, collection=ITEMS_COL))

# print(find_docs_in_col(connection=client, collection=ITEMS_COL, d_key='_id', d_value=2))

# uid_generator(connection=client, collection=ITEMS_COL)

print(generate_dbname(connection=client))


