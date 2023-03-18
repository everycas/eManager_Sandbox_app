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

DT_NOW = dt.datetime.now()
DT_STRING = ''.join([char for char in str(dt.datetime.now()) if char.isnumeric()])[: 20]  # 'yyyymmddhhmmssms'
DT_MODIFIED = f'{DT_STRING[:4]}.{DT_STRING[4:6]}.{DT_STRING[6:8]}-{DT_STRING[8:10]}:{DT_STRING[10:12]}:{DT_STRING[12:14]}'
print(DT_MODIFIED)

# default db collections
CFG_COL = 'settings'
ITEMS_COL = 'items'
CORRS_COL = 'corrs'
WORK_COL = 'orders'
REP_COL = 'reports'

# MONGO API --------------------------------------------------------------------------------->

# GENERATORS -------------------------------------------------------------------------------->


def generate_dbname_string():

    """ Generate db name / mask: YYYYMMDD(8)-HHMM(4)-SSMS(4)-BASE(4)-EMAN(4)UUID(8) """

    dbname_yyyymmdd = f'{DT_STRING[:8]}-'
    dbname_hhmmss = f'{DT_STRING[8:12]}-'
    dbname_msmsms = f'{DT_STRING[12:16]}-'
    dbname_uuid = f'EMAN{str(uuid.getnode())[4:12]}'

    return dbname_yyyymmdd + dbname_hhmmss + dbname_msmsms + 'BASE-' + dbname_uuid


def generate_guid_string(num_string: str):

    """ Convert any string number to guid string with mask:
     '{YYYYMMDD(8)-HHMM(4)-SSMS(4)-UUID(4)-CODE(12)}' """

    add_zero = ''
    guid_prefix = '{'
    guid_yyyymmdd = f'{DT_STRING[:8]}-'
    guid_hhmm = f'{DT_STRING[8:12]}-'
    guid_ssms = f'{DT_STRING[12:16]}-'
    guid_uuid = f'{str(uuid.getnode())[:4]}-'
    guid_postfix = '}'

    code = ''
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

    result_guid = guid_prefix + guid_yyyymmdd + guid_hhmm + guid_ssms + guid_uuid + code + guid_postfix

    return result_guid


def generate_doc_id_num(database: object, collection: str):

    """ Document universal id generator """

    col = database[collection]
    ids = [doc['_id'] for doc in col.find()]

    if ids:
        return max(ids) + 1
    else:
        return 1


# MONGO SERVER & DB ------------------------------------------------------------------------->


def connect_server():

    """ Return client connection to MongoDB Server using ini[server]name,ip,port params """

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
        print(f"Server connection using '{ini_mongo_connection_string}' string is successful.")
        return connection


def connect_base(server: object, dbname: str):

    """ Get eMan base from ini[base]name section. """

    if dbname != '':

        print(f"DB connection with name '{dbname}' is successful.")

        return server[dbname]

    else:
        new_dbname = generate_dbname_string()
        INI.set(section='base', param='name', data=new_dbname)

        print(f"DB connection with name '{dbname}' no or incorrect db specified in ini[base]name section.")

        with open(LOG_NAME, "a") as log_file:
            log_file.write(f"\n{DT_NOW}: no or incorrect db specified in ini[base]name section. "
                           f"Create new or set proper db name.")


# DB COLLECTIONS (COLS) & DOCUMENTS (DOCS) ------------------------------------------------->


def insert_one_doc_to_col(database: object, collection: str, document: dict):

    """ Insert new document to data collection / Mongo insert_one({}) """

    col = database[collection]
    doc = document
    col.insert_one(doc)

    print(f'New document in "{collection}" collection has been created successful.')


def insert_many_docs_to_col(database: object, collection: str, docs_list: list):

    """ Insert new documents to data collection / Mongo insert_many([{}, ... {}]) """

    col = database[collection]
    col.insert_many(docs_list)

    print(f'New documents in "{collection}" collection has been created successful.')


def find_docs_in_col(database: object, collection: str, doc_key: str, doc_value: str):

    """ Find documents in collection by search request / Mongo find({d_key: d_value})  """

    col = database[collection]
    return [doc for doc in col.find({doc_key: doc_value})]


def read_all_docs_in_col(database: object, collection: str):

    """ Find all docs in selected collection / Mongo find() """

    col = database[collection]
    return [doc for doc in col.find()]


def delete_one_doc_from_col(database: object, collection: str, doc_key: str, doc_value: str):

    """ Delete one document in collection / Mongo delete_one({d_key: d_value}) """

    col = database[collection]
    col.delete_one({doc_key: doc_value})

    print(f'Document in "{collection}" collection has been deleted successful.')


def delete_many_docs_from_col(database: object, collection: str, doc_key: str, doc_value: str):

    """ Delete all docs in collection filtered by search request / Mongo deleteMany({d_key: d_value}) """

    col = database[collection]
    col.delete_many({doc_key: doc_value})

    print(f'Documents in "{collection}" collection has been deleted successful.')


def delete_all_docs_from_col(database: object, collection: str):

    """ Delete all documents from selected collection / Mongo drop() """

    col = database[collection]
    col.drop()

    print(f'All documents in "{collection}" collection has been deleted successful.')


def update_one_doc_in_col(database: object, collection: str, doc_key: str, doc_value: str, update: dict):

    """ Update one document in collection / Mongo update_one({d_key: d_value}, {'$set': {update}}) """

    col = database[collection]
    col.update_one({doc_key: doc_value}, {'$set': update})

    print(f'Document in "{collection}" collection has been deleted successful.')


# DOCUMENT CONSTRUCTOR --------------------------------------------------------------------------------------->

def new_default_doc(database: object, collection: str):

    """
    '_id': int -> read only
    'created': str -> read only
    'modified': str -> read only
    'active': bool -> editable(True, False) from list
    'name': str -> editable(not empty)
    'comment': str -> editable(could be empty)
    """

    return {
        '_id':generate_doc_id_num(database=database, collection=collection),
        'created':DT_STRING,
        'modified':DT_MODIFIED,
        'active': True,
        'name':'New name',
        'comment':''
    }


# TESTING ------------------------------------------------------------------------------------>

connection = connect_server()
db = connect_base(server=connection, dbname=INI_DBNAME)
default_doc = new_default_doc(database=db, collection=ITEMS_COL)


delete_all_docs_from_col(database=db, collection=ITEMS_COL)
insert_one_doc_to_col(database=db, collection=ITEMS_COL, document=default_doc)








