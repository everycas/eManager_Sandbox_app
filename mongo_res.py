from ini_res import Ini
import datetime as dt
import pymongo
import uuid

# Global
INI_NAME = 'eMan.ini'
LOG_NAME = 'eMan.log'
DT_NOW = dt.datetime.now()
DT_STRING = ''.join([char for char in str(dt.datetime.now()) if char.isnumeric()])[: 20]  # 'yyyymmddhhmmssmsmsms(20)'

# Objects
INI = Ini()

# GUID SAMPLE: {20221010-1437-0632-1134-000000000012}


def generate_dbname():

    """ Generate db name GUID / mask: 'YYYYMMDD-HHMM-SSMS-eMan-UUID1[-12:]' """

    return f'{DT_STRING[:8]}-{DT_STRING[8:12]}-{DT_STRING[12:16]}-eMan-{str(uuid.uuid1())[-12:]}'


def generate_id(connection: object, dbname: str, collection: str):

    """ Documents id generator """

    db = connection[dbname]
    col = db[collection]
    ids = [doc['_id'] for doc in col.find()]

    if ids:
        return max(ids) + 1
    else:
        return 1


def guid_generator(num_string: str):

    """ Convert any number string to guid string / mask: '{YYYYMMDD(8)-HHMM(4)-SSMS(4)-UUID(4)-CODE(12)}' """

    add_zero = ''
    guid_prefix = '{'
    guid_yyyymmdd = f'{DT_STRING[:8]}-'
    guid_hhmm = f'{DT_STRING[8:12]}-'
    guid_ssms = f'{DT_STRING[12:16]}-'
    guid_uuid = f'{str(uuid.getnode())[:4]}-'
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

    result_guid = guid_prefix + guid_yyyymmdd + guid_hhmm + guid_ssms + guid_uuid + code + guid_postfix

    return result_guid


print(generate_dbname())

