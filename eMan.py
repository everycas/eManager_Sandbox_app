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

    # Create / select db
    db = connection[DB_NAME]
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


def doc_insert(connection, collection, document):

    """ Insert new document to data collection """

    client = connection
    db = client[DB_NAME]
    col = db[collection]
    doc = document
    col.insert_one(doc)


def to_guid(num_string: str):

    """ Convert any number string to guid_code SH5 """

    zero_add = ''
    guid_mask = '{00000000-0000-0000-0000-'
    postfix = '}'

    if len(num_string) < 12:
        diff = 12 - len(num_string)  # 6
        for _ in range(diff):
            zero_add += '0'
            code = zero_add + num_string
    elif len(num_string) > 12:
        diff = len(num_string) - 12
        code = num_string[diff:]
    else:
        code = num_string

    result = guid_mask + code + postfix
    return result


def dish_doc(guid: str, name: str, group: str, price: float, qnt: float):

    """ Template - newDish """

    dish = {

        'guid': guid,           # dish guid / use to_guid def
        'name': name,           # dish name
        'type': 'Dish',         # item type
        'group': group,         # dish group / parent
        'munit': 'Portion',     # dish measure unit
        'qnt': qnt,             # dish quantity
        'price': price          # dish price

    }

    return dish


c = connect_to_server()
# create_new_base(connection=c)

new_dish = dish_doc(guid='', name='Beaf Steak', group='Meat', price=120.45, qnt=1.0)
doc_insert(connection=c, collection='items', document=new_dish)




