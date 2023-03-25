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

# ru/eng date time string
INI_LANG = INI.get(section='main', param='lang')
DT_NOW = dt.datetime.now()

if INI_LANG == 'ru':
    DT_NOW_STRING = DT_NOW.strftime('%d.%m.%Y %H:%M:%S.%f')  # ru date format
else:  # eng
    DT_NOW_STRING = DT_NOW.strftime('%Y.%m.%d %H:%M:%S.%f')  # en date format

print(DT_NOW.strftime('%f')[:4])

# default db collections
DEF_COLS = ['settings', 'items', 'correspondents', 'orders', 'reports']

# Default document names -------------------------------------------------------------------->
# Keys
DEF_DOC_KEYS = ['_id', 'created', 'modified', 'active', 'Name', 'Comment']

# MONGO API --------------------------------------------------------------------------------->

# GENERATORS -------------------------------------------------------------------------------->


def generate_dbname_string():

    """ Generate db name / mask: YYYYMMDD(8)-HHMM(4)-SSMS(4)-BASE(4)-EMAN(4)UUID(8) """

    if INI_LANG == 'ru':
        date = DT_NOW.strftime('%d%m%Y')  # ru date format
    else:
        date = DT_NOW.strftime('%Y%m%d')  # en date format

    hhmm = DT_NOW.strftime('%H%M')  # hour min
    ssms = DT_NOW.strftime('%S%f')[:4]  # secs micro-secs
    uid = str(uuid.getnode())[:8]  # uuid

    return f'{date}-{hhmm}-{ssms}-BASE-EMAN{uid}'


def generate_guid_string(num_string: str):

    """ Convert any string number to guid string with mask:
     '{YYYYMMDD(8)-HHMM(4)-SSMS(4)-UUID(4)-CODE(12)}' """

    add_zero = ''
    prefix = '{'

    if INI_LANG == 'ru':
        date = DT_NOW.strftime('%d%m%Y')  # ru date format
    else:
        date = DT_NOW.strftime('%Y%m%d')  # en date format

    hhmm = DT_NOW.strftime("%H%M")
    ssms = DT_NOW.strftime("%S%f")[:4]
    uid = str(uuid.getnode())[:4]
    postfix = '}'

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

    return f'{prefix}{date}-{hhmm}-{ssms}-{uid}-{code}{postfix}'


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


# DB COLLECTIONS (COLS) & DOCUMENTS (DOCS) BASIC FUNCTIONS (CRUD - create, read, update, delete) ----------->


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


def find_all_docs_in_col(database: object, collection: str):

    """ Find all docs in selected collection / Mongo find() """

    col = database[collection]
    return [doc for doc in col.find()]


def find_first_any_doc_in_col(database: object, collection: str):

    """ Find and return first any document in specified collection """

    col = database[collection]
    return col.find_one()


def find_last_doc_in_col(database: object, collection: str):

    """ Find and return last document in specified collection """

    col = database[collection]
    docs = col.find().sort('_id', -1).limit(1)
    for d in docs:
        return d

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


# eMan DOCUMENT CONSTRUCTOR --------------------------------------------------------------------------------------->

def eman_default_doc(database: object, collection: str):

    """
    Default doc format using for create new docs in empty collection.
    Or in collection where default docs only.
    Or using as base doc when creating doc with extended keys.
    Default keys:
    '_id': int -> read only
    'created': str -> read only
    'modified': str -> read only
    'active': bool -> editable(True, False) from list
    'Name': str -> editable(not empty), user defined
    'Comment': str -> editable(could be empty), user defined
    """

    return {
        DEF_DOC_KEYS[0]:generate_doc_id_num(database=database, collection=collection),  # _id
        DEF_DOC_KEYS[1]:DT_NOW_STRING,  # created
        DEF_DOC_KEYS[2]:DT_NOW_STRING,  # modified
        DEF_DOC_KEYS[3]: True,  # active
        DEF_DOC_KEYS[4]:'New name',  # name
        DEF_DOC_KEYS[5]:''  # comment
    }


def eman_insert_new_doc(database: object, collection: str):

    """  Insert new doc using the same doc-format that is in collection """

    default_doc = eman_default_doc(database=database, collection=collection)

    if not collection:  # if collection is empty insert default doc

        insert_one_doc_to_col(database=database, collection=collection, document=default_doc)

    else:  # if col not empty, take last doc and insert it with 'name':'New name' and other keys

        last_doc_from_col  = find_last_doc_in_col(database=database, collection=collection)

        doc_for_insert = default_doc
        for k,v in last_doc_from_col.items():
            print(k)
            if k not in DEF_DOC_KEYS:
                if v.isdigit():
                    doc_for_insert[k] = 0
                else:
                    doc_for_insert[k] = ''

        print(doc_for_insert)
        insert_one_doc_to_col(database=database, collection=collection, document=doc_for_insert)


def eman_add_new_keyvalue_

# TESTING ------------------------------------------------------------------------------------>

connection = connect_server()

if not INI_DBNAME:
    dbname = generate_dbname_string()
    INI.set(section='base', param='name',data=dbname)
else:
    dbname = INI_DBNAME

db = connect_base(server=connection, dbname=dbname)

items_col = DEF_COLS[1]
doc = eman_default_doc(database=db, collection=items_col)
insert_one_doc_to_col(database=db, collection=items_col, document=doc)
# delete_all_docs_from_col(database=db, collection=items_col)
# insert_one_doc_to_col(database=db, collection=items_col, document=doc)
eman_insert_new_doc(database=db, collection=items_col)

# cur_doc = find_last_doc_in_col(database=db, collection=items_col)
# print(cur_doc.keys())
# print(cur_doc.values())

# d = {}
# d['_id'] = generate_doc_id_num(database=db, collection=items_col)
# d['name'] = 'New name'
# print(d)
#
# for k,v in d.items():
#     print(k)
#     print(v)







