import sys

# from bson import ObjectId
from bson import ObjectId
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from functools import wraps
import traceback

'''
    Author: Gupern 周起超
    CreateTime: 2017-05-16
    Description: This is a file for easy manipulate the MongoDB
    
    LastModified: 
        2017-05-24 : change class to func, for easily use
        2017-05-17 : add note params and return
    FunctionNote: 
        renameField(col, _id, oldField, newField): 重命名field
        removeDocById(col, _id): 通过Id移除doc
        findOneById(col, _id): 通过id查找doc
        clientInsurance(func): 装饰器，用于保证client关闭
        cloneField(col, _id, key1, kye2): 克隆key1，到key2，成功返回1，失败返回0
        closeClient(client): 返回None
        insertOneDocument(col, document): 返回inserted_id
        updateOneField: col、_id、key和value，返回1（成功）或者0（失败）,'_id type error'（如果传入的参数有问题）
        getClient: 接收url，port，username和password，若无则设置为默认参数，返回client
        getCol：接收client，db和col，返回col
'''


def get_mongo_client(uri="mongodb://0.0.0.0:27017/", db="matafy"):
    """
    Connect to MongoDB
    """
    try:
        # c = MongoClient("mongodb://upenergy:upenergy@db0.silknets.com:27000/sso")
        # uri = u"mongodb://mongo:mongo@127.0.0.1/sso?authMechanism=SCRAM-SHA-1"
        c = MongoClient(uri)

    except ConnectionFailure as e:
        sys.stderr.write("Could not connect to MongoDB: %s" % e)
        sys.exit(1)

    # Get a Database handle to a database named "mydb"
    dbh = c[db]
    print('connected succeed.')
    print('URI: ' + uri + '  Database: ' + db)
    return dbh


def findOneById(col, _id):
    '''
        :params col, _id: _id can be string or unicode or ObjectId
        :return document: return document or None
        :useage: just call me.
    '''
    if type(_id) == str or type(_id) == unicode:
        _id = ObjectId(_id)
    if type(_id) == ObjectId:
        result = col.find_one({'_id': _id})
        return result
    else:
        print('_id type error')
        return '_id type error'


def clientInsurance(func):
    '''
        mongo连接保险器，进行数据操作时的装饰器
        :params function(*MongoClient): a function which param is MongoClient args
        :return function: a function which wrap in try...except...finally
        :useage: for example:
            @clientInsurance
            def operation(*args):
                # your operation here, e.g.
                client1 = args[0]
                for i in client1[db][col].find():
                    print i
                
            if __name__=='__main__':
                client1 = mongoUtil.fastGetClient('local')
                client2 = mongoUtil.getClient(url, port, username, password)
                client3 = MongoClient(urlString)
                
                # and then it will close your all client automatically
                operation(client1, client2, client3)
    '''

    @wraps(func)
    def insurance(*args, **kwargs):
        try:
            # 为什么方程放这里会执行？
            func(*args, **kwargs)
            print('')
            print('*[INFO]: Congratulation! All operations done.')
        except:
            print('')
            print(traceback.format_exc())
        finally:
            [arg.close() for arg in args]
            print('')
            print('*[INFO]: All clients have already closed.')

    return insurance


def test():
    print('hello, mongo util')


def connect_to_server_quickly(server):
    if server == 17 or server == '17':
        return get_client(url='112.90.89.17', port=27017, username='readWriter', password='readWriter17')
    elif server == 'aliR':
        return get_client(url='120.24.37.232', port=3718, username='root', password='Scrapy123')
    elif server == 'aliW':
        return get_client(url='120.24.37.232', port=3717, username='root', password='Scrapy123')
    elif server == '16' or server==16:
        return get_client(url='112.90.89.16', port=27017, username='myUserAdmin', password='8mwTdy1klnSYepNo')
    elif server == 'aliI':
        return MongoClient("mongodb://root:Scrapy123@dds-wz962ff5b9eb15941.\
        mongodb.rds.aliyuncs.com:3717,dds-wz962ff5b9eb15942.mongodb.rds.aliyuncs\
        .com:3717/admin?replicaSet=mgset-2406913", maxPoolSize=20)

    elif server == 'local':
        return get_client(maxPoolSize=20)
    else:
        print('server no register')
        raw_input()
        return None


def get_client(url='localhost', port=27017, username='', password='', maxPoolSize=20):
    """
    :params: url, port, username, password
    :return: client
    """
    # 先调用标准参数，再调用默认参数
    print('mongoConnecting...')
    if username == '' and password == '':
        try:
            client = MongoClient('mongodb://{}:{}'.format(url, port))
            print('connect success')
            return client
        except ConnectionFailure as e:
            sys.stderr.write("Could not connect to MongoDB: %s" % e)
            sys.exit(1)
    elif username != '' and password != '':
        try:
            client = MongoClient('mongodb://{}:{}@{}:{}'.format(username, password, url, port))
            print('connect success')
            return client
        except ConnectionFailure as e:
            sys.stderr.write("Could not connect to MongoDB: %s" % e)
            sys.exit(1)
    else:
        raise 'Something error'


def get_col(client, db, col):
    """
    :params: client, db, col
    :return: col
    """
    return client[db][col]


def updateOneField(col, _id, key, value):
    '''
    :params: col, _id, key, value
    :return: result (success 1 or fail 0)
    '''
    if type(_id) == str or type(_id) == unicode:
        _id = ObjectId(_id)
    if type(_id) == ObjectId:
        result = col.update({'_id': _id},
                            {'$set':
                                 {key: value}
                             }
                            )
        return result['nModified']
    else:
        return '_id type error'


def insertOneDocument(col, document):
    '''
    :params: col, document
    :return: result.inserted_id(ObjectId)
    '''
    result = col.insert_one(document)
    return result.inserted_id


def closeClient(client):
    '''
    :params: client
    :return: closeResult
    '''
    try:
        client.close()
        return 'client closed'
    except:
        s = sys.exc_info()
        print(s[0], s[1])


def cloneField(col, _id, key1, key2):
    '''
    :params: col, _id, key1, key2
    :return: True or False
    '''
    if type(_id) == str or type(_id) == unicode:
        _id = ObjectId(_id)
    if type(_id) == ObjectId:
        document = col.find_one({'_id': _id})
        value = document[key1]
        result = col.update({'_id': _id},
                            {'$set':
                                 {key2: value}
                             }
                            )
        return result['nModified']
    else:
        return '_id type error'


def renameField(col, _id, oldField, newField):
    '''
    :params: col, _id, oldField, newField 
    :return: new document or False
    '''
    if type(_id) == str or type(_id) == unicode:
        _id = ObjectId(_id)
    if type(_id) == ObjectId:
        # result = col.update({'_id':_id},{'$rename':{field1,field2}})
        dic = col.find_one({'_id': _id})
        valueOfField = dic.get(oldField)
        if valueOfField is None:
            print('renameField no such old field')
            return False
        del dic[oldField]
        dic[newField] = valueOfField
        result = col.find_one_and_replace({'_id': _id}, dic, return_document=True)
        print('renameField success\nnew doc is {}'.format(result))
        return result
    else:
        print('renameField _id type error')
        return False


def removeDocById(col, _id):
    '''
    :params: col, _id
    :return: 1 or 0
    '''
    if type(_id) == str or type(_id) == unicode:
        _id = ObjectId(_id)
    if type(_id) == ObjectId:
        result = col.delete_many({'_id': _id})
        return result.deleted_count
    else:
        print('remove _id type error')
        return 0


if __name__ == '__main__':
    client = fastGetClient('aliWriter')
    col = get_col(client, 'silkweb-production', 'guide')
    result = removeDocById(col, '58537075f1d300535160d0e6')
    print(result)
